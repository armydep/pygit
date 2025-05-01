from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    def __init__(self, tokens: List[str]):
        self.args = tokens

    def execute(self):
        self.validate()
        self.exec()

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def exec(self):
        pass    