from .command import Command
from util.file_util import FileUtil
import os


class StatusCommand(Command):
    def validate(self) -> None:
        print("Im status command validation")

    def exec(self) -> None:
        print("Im status command exec")
        work_dir = self.repository.work_dir()
        # print(f"working dir: {work_dir}")
        storage_dir = self.repository.storage_dir()
        all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
        for f in all_working_files:
            print(f">{f}")
        index_file = "index"
        storage_full_path = os.path.join(work_dir, storage_dir)
        index_file_path = os.path.join(storage_full_path, index_file)
        all_indexed_files = FileUtil.read_lines_from_file(index_file_path)
        for f in all_indexed_files:
            print(f">>{f}")        
            