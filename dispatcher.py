from registry import COMMANDS

from commands import init
from commands import add
from commands import commit
from commands import status
from commands import branch
from commands import switch
from commands import restore

# from commands import merge


def dispatch(args, staged=False):
    if not args:
        print("No command given")
        return
    cmd = args[0]
    if cmd in COMMANDS:
        command = COMMANDS[cmd]
        command(args[1:], staged)
    else:
        print(f"Unknown command: {cmd}")
