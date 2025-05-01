from .command import Command
from typing import List


class CommitCommand(Command):
    def validate(self) -> None:
        print("Im commit command validation. args: " + "_".join(self.args))

    def exec(self) -> None:
        print("Im commit command exec")        