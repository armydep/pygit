from abc import ABC, abstractmethod
from typing import List

from repo import Repository


class Command(ABC):
    def __init__(self, tokens: List[str]):
        self.args = tokens
        self.repository = Repository()

    def execute(self):
        self.validate()
        self.exec()

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def exec(self):
        pass    