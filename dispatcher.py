from registry import COMMANDS

from commands import status_command  
from commands import add
from commands import commit_command
from commands import init_command
from commands import restore


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
