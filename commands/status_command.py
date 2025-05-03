from .command import Command
from util.file_util import FileUtil
import os


class StatusCommand(Command):
    def validate(self) -> None:
        print("Im status command validation")

    def exec(self) -> None:
        print("Im status command exec")
        work_dir = self.repository.work_dir()
        storage_dir = self.repository.storage_dir()
        all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
        # for f in all_working_files:
        #     print(f">{f}")
        index_file = "index"
        storage_full_path = os.path.join(work_dir, storage_dir)
        index_file_path = os.path.join(storage_full_path, index_file)
        all_indexed_files = FileUtil.read_lines_from_file(index_file_path)
        # for f in all_indexed_files:
        #     print(f">>{f}")

        # index_file = "index"
        # storage_dir = self.repository.storage_dir()
        # storage_full_path = os.path.join(work_dir, storage_dir)
        index_file_path = os.path.join(storage_full_path, index_file)
        index_entries = FileUtil.parse_index_file_lines(index_file_path)
        # for ie in index_entries:
        #     print(f"Indexed: {ie}")
        # print("-----------")
        all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
        work_file_entries = FileUtil.transform_paths_to_entries(all_working_files)
        # for wfe in work_file_entries:
        #     print(f"Work dir file: {wfe}")
        # modified_set = set()
        for wfe in work_file_entries:
            if wfe not in index_entries:
                index_entry = self._find_index_entry_by_path(index_entries, wfe.path)
                if index_entry:
                    print(f"Modified: {index_entry.path}")
                    # modified_set.add(index_entry.path)
                else:
                    print(f"Untracked (new): {wfe.path}")

        for ie in index_entries:
            if ie not in work_file_entries:
                wd_entry = self._find_index_entry_by_path(work_file_entries, ie.path)
                if not wd_entry:
                    print(f"Deleted: {ie.path}")
