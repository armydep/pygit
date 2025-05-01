from .command import Command
from typing import List


class StatusCommand(Command):
    def validate(self) -> None:
        print("Im status command validation")

    def exec(self) -> None:
        print("Im status command exec")