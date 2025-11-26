import difflib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from hashlib import md5
from random import randint
from typing import Callable, Protocol


class ShellProtocol(Protocol):
    def send_line(self, line: str) -> None:
        raise NotImplementedError()

    def receive_line(self) -> str:
        raise NotImplementedError()

    def skip_send_echo(self) -> None:
        """
        Call this immediately after send_line to avoid receiving echos of the sent command.

        **Warning**: Do not call this if there is still pending receptions, since those will be skipped instead of the intended echo

        **Note**: The fact that this is implemention-defined and not just a call to `receive_line()` is a hack while investigating a weird additional line endings sent by cmd.exe after each command
        """
        raise NotImplementedError()


class WithInterProcessCommunication:
    def __init__(
        self, command: list[str], workdir: str, env: dict[str, str], newline: str
    ):
        """
        Parameters:
            env(dict[str,str]): environment variables
        """
        self.init_ipc(command, workdir, env, newline)

    def init_ipc(
        self, command: list[str], workdir: str, env: dict[str, str], newline: str
    ):
        # Source - https://stackoverflow.com/a/54066021
        # Posted by Ondrej K., modified by community. See post 'Timeline' for change history
        # Retrieved 2025-11-08, License - CC BY-SA 4.0

        (child_read, parent_write) = os.pipe()
        (parent_read, child_write) = os.pipe()
        self.child = subprocess.Popen(
            command,
            stdin=child_read,
            stdout=child_write,
            stderr=child_write,
            cwd=workdir,
            env=env,
        )
        self.outfile = os.fdopen(parent_write, "w", buffering=1)
        self.infile = os.fdopen(parent_read, newline=newline)


class Powershell(WithInterProcessCommunication):
    def __init__(self, workdir: str, env: dict[str, str]):
        """
        Parameters:
            env(dict[str,str]): environment variables
        """
        WithInterProcessCommunication.__init__(
            self, ["powershell", "/NoLogo"], workdir, env, "\n"
        )

    def send_line(self, line: str) -> None:
        print(line, file=self.outfile)
        self.outfile.flush()

    def receive_line(self) -> str:
        return self.infile.readline().strip("\r\n")

    def skip_send_echo(self) -> None:
        _ = self.receive_line()

    def exit(self) -> None:
        self.send_line("exit")
        self.child.wait()


class Cmd(WithInterProcessCommunication):
    def __init__(self, workdir: str, env: dict[str, str]):
        """
        Parameters:
            env(dict[str,str]): environment variables
        """
        WithInterProcessCommunication.__init__(self, ["cmd"], workdir, env, "\r\n")

    def send_line(self, line: str) -> None:
        escaped = line.replace('"', '"') if line.startswith("echo") else line

        print(escaped, file=self.outfile)
        self.outfile.flush()

    def receive_line(self) -> str:
        res = self.infile.readline().strip("\r\n")
        return res

    def skip_send_echo(self) -> None:
        _ = self.receive_line()
        _ = self.receive_line()

    def exit(self) -> None:
        self.send_line("exit")
        self.child.wait()


class Cram:
    def __init__(self, shell: ShellProtocol, variables: dict[str, str]):
        self.shell = shell
        # discard shell prelude
        mark = self.mark_("")
        self.receive_until_mark_(mark)

        # set variables, which differs from env variables in powershell
        for k, v in variables.items():
            self.shell.send_line(f'${k}="{v}"')

        mark = self.mark_("")
        self.receive_until_mark_(mark)

    def send(self, command: str) -> list[str]:
        """
        Send a command to the underlying shell
        Returns: the line sent in response to the command by the shell
        """
        self.shell.send_line(command)
        self.shell.skip_send_echo()
        mark = self.mark_(command)
        return self.receive_until_mark_(mark)

    def __call__(self, cmd: str) -> list[str]:
        return self.send(cmd)

    # Private stuff

    watermark_count_ = randint(0, 2**31)

    def mark_(self, command: str) -> str:
        """
        Echoes a hash of the given `command` to the underlying shell, later used to detect when the command completes
        Returns: the echoed hash
        """
        mark = self.watermark_(command)
        self.shell.send_line(f"echo {mark}")
        return mark

    def receive_until_mark_(self, mark: str) -> list[str]:
        """
        Read lines repeatedly, waiting for the given `mark` to be echoed by the underlying shell.
        All lines containing `mark` will be ignored, effectively ignoring the echo of the `mark`
        Returns: the lines received before `mark`
        """
        result: list[str] = []
        line = self.shell.receive_line()
        while line != mark:
            # do not include our marking machinery in user visible output
            if mark not in line:
                result.append(line)
            line = self.shell.receive_line()
        return result

    def watermark_(self, command: str) -> str:
        """
        Returns: a hash that can be used to uniquely identify the given `command`
        """
        self.watermark_count_ += 1
        h = md5(str(self.watermark_count_).encode())
        h.update(command.encode())
        h.update("CRAM".encode())
        return f"{h.hexdigest()}"


@dataclass
class TestResult:
    expected: list[str]
    actual: list[str]

    def diff(self, file_t, file_err):
        return [
            l.strip("\r\n")
            for l in difflib.unified_diff(
                self.actual, self.expected, fromfile=file_err, tofile=file_t
            )
        ]

    def success(self):
        return self.expected == self.actual


def test(test_lines: list[str], exec: Callable[[str], list[str]]) -> TestResult:
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

    return TestResult(expected=test_lines, actual=result)


def make_temp_dir(prefix: str) -> str:
    os.makedirs(f"{prefix}/.cram", exist_ok=True)

    uuid = randint(0, 2**31)
    while os.path.exists(f"{prefix}/.cram/{uuid}"):
        uuid = randint(0, 2**31)

    temp_dir = f"{prefix}/.cram/{uuid}"
    os.mkdir(temp_dir)
    return os.path.abspath(temp_dir)


# TODO (feature parity) support full cram option set
# TODO (feature parity) support loading from .cramrc file
# TODO (feature parity) support loading from CRAM env variable
# TODO support specifying options in the .t file
class Options:
    interactive: bool = False
    yes: bool = False
    keep_tmpdir: bool = False
    shell: type[Powershell] | type[Cmd] = Powershell

    def promote(self) -> bool:
        return self.interactive and self.yes

    def parse(self, args: list[str]) -> list[str]:
        """
        Parse options among the given `args` and update `self` accordingly
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
            elif arg == "--keep-tmpdir":
                self.keep_tmpdir = True
            elif arg == "--shell=powershell":
                self.shell = Powershell
            elif arg == "--shell=cmd":
                self.shell = Cmd
            elif arg == "--":
                ret.extend(args[i + 1 :])
                break
            else:
                ret.append(arg)

        return ret


bom_prefix = (b"\xef\xbb\xbf").decode("utf-8")


def err_file(test_file: str) -> str:
    return test_file.removesuffix(".t") + ".err"


def run_test(options: Options, test_file: str) -> TestResult:
    temp_dir = make_temp_dir(".")
    env: dict[str, str] = {k: v for k, v in os.environ.items()}
    cram_special_variables: dict[str, str] = {
        # Paths
        "TESTDIR": os.path.abspath(os.path.dirname(test_file)),
        "TMPDIR": temp_dir,
        "TEMP": temp_dir,
        "TMP": temp_dir,
        "CRAMTMP": temp_dir,
        "TESTFILE": os.path.basename(test_file),
        "TESTSHELL": "powershell.exe",
        # Misc
        "CDPATH": "",
        "COLUMNS": "80",
        "GREP_OPTIONS": "",
        "LANGUAGE": "C",
        "LANG": "C",
        "LC_ALL": "C",
        "TZ": "GMT",
    }
    env.update(cram_special_variables)
    shell = options.shell(workdir=temp_dir, env=env)
    try:
        cram = Cram(shell, variables=cram_special_variables)

        # TODO support non-utf-8 encodings
        with open(test_file, "r", encoding="utf-8") as fin:
            lines = fin.read().replace(bom_prefix, "").replace("\r\n", "\n").split("\n")
            test_result = test(lines, cram)

        output_file = test_file if options.promote() else err_file(test_file)
        with open(output_file, "w", encoding="utf-8", newline="\n") as fout:
            fout.write("\n".join(test_result.actual))
        return test_result
    finally:
        shell.exit()
        if not options.keep_tmpdir:
            shutil.rmtree(temp_dir)


def main(options: Options, test_files: list[str]) -> None:
    failures: list[tuple[str, TestResult]] = []
    for test_file in test_files:
        result = run_test(options, test_file)
        if result.success():
            print(".", end="")
        else:
            failures.append((os.path.basename(test_file), result))
            print("!", end="")
    print("")
    if len(failures) > 0:
        for test_file, result in failures:
            print(*result.diff(err_file(test_file), test_file), sep="\n")
        exit(1)


if __name__ == "__main__":
    options = Options()
    args = options.parse(sys.argv[1:])
    main(options, args[0:])
