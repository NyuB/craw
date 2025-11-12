import os
import subprocess
import sys
from typing import Callable
from random import randint
from hashlib import md5


class Powershell:
    def __init__(self, workdir: str, env: dict[str, str]):
        """
        Parameters:
            env(dict[str,str]): environment variables
            variables(dict[str,str]): variables set as prelude to the powershell. Will be accessible as `$var`, compared to `$env:var` for env variables
        """
        self.init_ipc_(workdir, env)

    def send_line_(self, line: str) -> None:
        print(line, file=self.outfile)
        self.outfile.flush()

    def receive_line_(self) -> str:
        """
        Read a line from the underlying shell output, not including the line terminator
        """
        return self.infile.readline().strip("\r\n")

    def exit(self) -> None:
        self.send_line_("exit")
        self.child.wait()

    def init_ipc_(self, workdir: str, env: dict[str, str]):
        # Source - https://stackoverflow.com/a/54066021
        # Posted by Ondrej K., modified by community. See post 'Timeline' for change history
        # Retrieved 2025-11-08, License - CC BY-SA 4.0

        (child_read, parent_write) = os.pipe()
        (parent_read, child_write) = os.pipe()
        self.child = subprocess.Popen(
            ["powershell", "/NoLogo"],
            stdin=child_read,
            stdout=child_write,
            stderr=child_write,
            cwd=workdir,
            env=env,
        )
        self.outfile = os.fdopen(parent_write, "w", buffering=1)
        self.infile = os.fdopen(parent_read)


class Cram:
    def __init__(self, shell: Powershell, variables: dict[str, str]):
        self.shell = shell
        # discard shell prelude
        mark = self.mark_("")
        self.receive_until_mark_(mark)

        # Set variables
        for k, v in variables.items():
            self.shell.send_line_(f'${k}="{v}"')

        mark = self.mark_("")
        self.receive_until_mark_(mark)

    def send(self, cmd: str) -> list[str]:
        self.shell.send_line_(cmd)
        self.receive_skip_()
        mark = self.mark_(cmd)
        return self.receive_until_mark_(mark)

    def __call__(self, cmd: str) -> list[str]:
        return self.send(cmd)

    # Private stuff

    watermark_count_ = randint(0, 2**31)

    def mark_(self, cmd: str) -> str:
        mark = self.watermark_(cmd)
        self.shell.send_line_(f'echo "{mark}"')
        return mark

    def receive_until_mark_(self, mark: str) -> list[str]:
        result: list[str] = []
        line = self.shell.receive_line_()
        while line != mark:
            # do not include our marking machinery in user visible output
            if mark not in line:
                result.append(line)
            line = self.shell.receive_line_()
        return result

    def watermark_(self, cmd: str) -> str:
        self.watermark_count_ += 1
        h = md5(str(self.watermark_count_).encode())
        h.update(cmd.encode())
        return f"<CRAM> {h.hexdigest()}"

    def receive_skip_(self) -> None:
        _ = self.shell.receive_line_()


def test(test_lines: list[str], exec: Callable[[str], list[str]]) -> list[str]:
    """
    Runs cram-like test on test_lines and returns the actual output lines

    Uses `exec` to execute the command lines in test_lines
    """
    result: list[str] = []
    for test_line in test_lines:
        if not test_line.startswith("  "):  # comment line
            result.append(test_line)
        elif test_line.startswith("  $ "):  # command line
            result.append(test_line)
            output = exec(test_line.removeprefix("  $ "))
            result.extend(map(lambda l: f"  {l}", output))

    return result


def make_temp_dir(prefix: str) -> str:
    os.makedirs(f"{prefix}/.cram", exist_ok=True)

    uuid = randint(0, 2**31)
    while os.path.exists(f"{prefix}/.cram/{uuid}"):
        uuid = randint(0, 2**31)

    temp_dir = f"{prefix}/.cram/{uuid}"
    os.mkdir(temp_dir)
    return temp_dir


# TODO support full cram options parsing
class Options:
    interactive: bool = False
    yes: bool = False

    def promote(self) -> bool:
        return self.interactive and self.yes

    def parse(self, args: list[str]) -> list[str]:
        """
        Returns: the given arguments with options filtered out
        """
        ret: list[str] = []
        for i, arg in enumerate(args):
            if arg == "--interactive" or arg == "-i":
                self.interactive = True
            elif arg == "--yes" or arg == "-y":
                self.yes = True
            elif arg == "--promote":
                self.yes = True
                self.interactive = True
            elif arg == "--":
                ret.extend(args[i + 1 :])
                break
            else:
                ret.append(arg)

        return ret


bom_prefix = (b"\xef\xbb\xbf").decode("utf-8")


def run_test(options: Options, test_file: str) -> None:
    temp_dir = make_temp_dir(".")
    env: dict[str, str] = {k: v for k, v in os.environ.items()}
    cram_special_variables: dict[str, str] = {"TESTDIR": str(os.path.abspath("."))}
    env.update(cram_special_variables)
    cram = Cram(Powershell(workdir=temp_dir, env=env), variables=cram_special_variables)

    with open(test_file, "r", encoding="utf-8") as fin:
        lines = fin.read().replace(bom_prefix, "").replace("\r\n", "\n").split("\n")
        output = test(lines, cram)

    output_file = (
        test_file if options.promote() else f"{test_file.removesuffix(".t")}.err"
    )
    with open(output_file, "w", encoding="utf-8", newline="\n") as fout:
        fout.write("\n".join(output))


def main(options: Options, test_files: list[str]) -> None:
    for test_file in test_files:
        run_test(options, test_file)


if __name__ == "__main__":
    options = Options()
    args = options.parse(sys.argv[1:])
    main(options, args[0:])
