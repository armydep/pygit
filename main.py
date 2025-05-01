#!/usr/bin/env python3

from dispatcher import Dispatcher
# import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Example CLI app")
    # parser.add_argument("command", help="Your command")
    # parser.add_argument("--greeting", default="HelloG", help="Greeting word")
    parser.add_argument("items", nargs='+', help="List of items")
    args = parser.parse_args()
    # print(f"{args.greeting}, {args.name}!")
    # print(f"{args.command}")
    # for item in args.items:
    #     print(f"- {item}")

    command = Dispatcher.dispatch(args.items)    
    command.execute()

if __name__ == "__main__":
    main()    