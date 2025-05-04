#!/usr/bin/env python3

import argparse
from dispatcher import dispatch


def main():
    parser = argparse.ArgumentParser(description="pygit CLI")
    parser.add_argument("items", nargs="+", help="Command and arguments")
    args = parser.parse_args()

    dispatch(args.items)


if __name__ == "__main__":
    main()
