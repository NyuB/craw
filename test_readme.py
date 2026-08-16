"""
Documentation maintenance script, checking that the usage documented in README.md is correct, i.e. that it corresponds to the tested one.
"""

import sys


def sublist(sub: list[str], l: list[str]) -> bool:
    if len(sub) > len(l):
        return False
    for i in range(len(l) - len(sub) + 1):
        if l[i : i + len(sub)] == sub:
            return True
    return False


def read_lines(file: str) -> list[str]:
    with open(file, "r", encoding="utf8") as f:
        return f.read().replace("\r\n", "\n").split("\n")


def main(readme: str, tests: list[str]):
    readme_lines = read_lines(readme)
    usages: list[list[str]] = []
    usage: list[str] = []
    in_usage = False
    for l in readme_lines:
        if l == "```cram":
            assert not in_usage
            in_usage = True
        elif l == "```" and in_usage:
            in_usage = False
            usages.append(usage)
            usage = []
        elif in_usage:
            usage.append(l)
    assert not in_usage
    assert usages != []

    all_usages_found = True
    for usage in usages:
        usage_found = False
        for test in tests:
            test_lines = read_lines(test)
            if sublist(usage, test_lines):
                usage_found = True
                break
        all_usages_found = all_usages_found and usage_found

        if not usage_found:
            prefix_len = 3
            prefix = usage[:prefix_len]
            print(
                f"Usage not found in any of the given tests, please update the documentation or add a corresponding test. Here are the first {prefix_len} lines of the involved usage:"
            )
            print(">>>")
            print(*prefix, sep="\n")
            print("<<<")
    if not all_usages_found:
        print(f"Some usage sections in {readme} have no matching test !")
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <readme.md> [<test.t>...]")
        print(
            f"    Check if each of readme.md usage sections corresponds to a section in one of [test.t ...]"
        )
        exit(2)
    main(sys.argv[1], sys.argv[2:])
