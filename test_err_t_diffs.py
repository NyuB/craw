import os
import sys


def main(t_files: list[str]):
    error = False
    for t_file in t_files:
        err_file = t_file.replace(".t", ".err")
        err_code = os.system(
            f"git --no-pager diff -p --no-index -- {t_file} {err_file}"
        )
        if err_code != 0:
            error = True
    if error:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
