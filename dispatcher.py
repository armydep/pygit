from registry import COMMANDS

from commands import status_command  
from commands import add
from commands import commit_command
from commands import init_command


def dispatch(args):
    if not args:
        print("No command given")
        return
    cmd = args[0]
    if cmd in COMMANDS:
        command = COMMANDS[cmd]
        command(args[1:])
    else:
        print(f"Unknown command: {cmd}")
