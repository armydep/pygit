#!/usr/bin/env python3

import argparse
from dispatcher import dispatch


def main():
    parser = argparse.ArgumentParser(description="pygit CLI")
    parser.add_argument("items", nargs="+", help="Command and arguments")
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    dispatch(args.items, staged=args.staged)


if __name__ == "__main__":
    main()
