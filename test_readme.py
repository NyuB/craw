"""
Documentation maintenance script, checking that the usage documented in README.md is correct, i.e. that it corresponds to the tested one.
"""

import sys

def sublist(sub, l)->bool:
    if len(sub) > len(l):
        return False
    for i in range(len(l) - len(sub) + 1):
        if l[i:i + len(sub)] == sub:
            return True
    return False
        

def main(readme: str, test: str):
    with open(readme, 'r', encoding="utf8") as f:
        lines = f.read().replace("\r\n", "\n").split("\n")
        usage: list[str] = []
        in_usage = False
        for l in lines:
            if l == "```cram":
                in_usage = True
            elif l == "```":
                in_usage = False
                break
            elif in_usage:
                usage.append(l)
        assert usage != []
    with open(test, 'r', encoding="utf8") as f:
        lines = f.read().replace("\r\n", "\n").split("\n")
        if sublist(usage, lines):
            exit(0)
        else:
            print("README usage differs from the tested one, please update the README.md usage section from test.t")
            exit(1)
            
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <readme.md> <test.t>")
        print(f"    Check if readme.md usage section corresponds line by one to a section of test.t")
        exit(2)
    main(sys.argv[1], sys.argv[2])