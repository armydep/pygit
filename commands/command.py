from abc import ABC, abstractmethod
from typing import Optional

from repo import Repository
from util.file_util import IndexEntry


class Command(ABC):
    def __init__(self, tokens: list[str]):
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

    @staticmethod
    def _find_index_entry_by_path(entries: list[IndexEntry], target_path: str) -> Optional[IndexEntry]:
        for entry in entries:
            if entry.path == target_path:
                return entry
        return None  