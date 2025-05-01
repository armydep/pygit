from .command import Command
from typing import List


class InitCommand(Command):
    def validate(self) -> None:
        print("Im init command validation")

    def exec(self) -> None:
        print("Im init command exec")
        