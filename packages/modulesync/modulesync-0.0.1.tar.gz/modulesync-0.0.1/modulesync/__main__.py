from modulesync import sync
import sys
import os


class InvalidParams(Exception):
    pass


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        changed_dir = args[0]
        source_dir = os.getcwd()

    elif len(args) == 2:
        changed_dir = args[0]
        source_dir = args[1]
    else:
        raise InvalidParams

    sync(source_dir, changed_dir)


if __name__ == "__main__":
    main()
