from commands.command import Command
from commands.init_command import InitCommand
from commands.status_command import StatusCommand
from commands.commit_command import CommitCommand
from commands.add import AddCommand


class Dispatcher:
    @staticmethod
    def dispatch(tokens: list[str]) -> Command:
        if tokens[0] == "init":
            return InitCommand(tokens[1:])
        elif tokens[0] == "status":
            return StatusCommand(tokens[1:])
        elif tokens[0] == "add":
            return AddCommand(tokens[1:])
        elif tokens[0] == "commit":
            return CommitCommand(tokens[1:])
        return None
