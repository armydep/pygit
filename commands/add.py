from util.file_util import FileUtil, IndexEntry
from .command import Command
from typing import Optional
import os
import traceback


class AddCommand(Command):
    def validate(self) -> None:
        print(f"Im add command validation. args size: {len(self.args)}:[{' '.join(self.args)}]")

    def exec(self) -> None:
        print("Im add command exec")
        try:
            work_dir = self.repository.work_dir()
            print(f"working dir: {work_dir}")
            storage_dir = self.repository.storage_dir()
            storage_full_path = os.path.join(work_dir, storage_dir)
            target_file = self.args[0]
            file_path = os.path.join(work_dir, target_file)

            if not FileUtil.is_dir_exist(storage_full_path):
                print("The work dir is not a git repository. missing .git directory")
                return

            if not FileUtil.is_file_exist(file_path):
                print(f"Specified file does not exists {file_path}")
                return

            target_index_entry = FileUtil.build_index_entry(file_path)
            print(f"Index entry:{target_index_entry}")
            objects_dir = "objects"
            index_file = "index"
            index_file_path = os.path.join(storage_full_path, index_file)
            index_entries = FileUtil.parse_index_file_lines(index_file_path)

            index_entry = self._find_index_entry_by_path(index_entries, target_index_entry.path)
            if index_entry:
                print("Yes it is")
                if (target_index_entry.mod_time == index_entry.mod_time) or (
                    target_index_entry.sha1 == index_entry.sha1 and target_index_entry.size == index_entry.size
                ):
                    print("The file is already staged. No changes")
                else:
                    print("Exist in stage but modified. Replacing")
                    index_entry.size = target_index_entry.size
                    index_entry.sha1 = target_index_entry.sha1
                    index_entry.mod_time = target_index_entry.mod_time
                    FileUtil.update_index_file(index_file_path, index_entries)
                    path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)                
                    FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))                    
            else:
                print("no it is not")
                index_entries.append(target_index_entry)
                FileUtil.update_index_file(index_file_path, index_entries)
                path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)                
                FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))

        except Exception as e:
            print(f"add failed. {e}")
            traceback.print_exc()
            return -1

    @staticmethod
    def _index_contains_entry(index_entries: list[IndexEntry], entry: IndexEntry) -> bool:
        return any(itent.path and itent.path == entry.path for itent in index_entries)

    @staticmethod
    def _find_index_entry_by_path(entries: list[IndexEntry], target_path: str) -> Optional[IndexEntry]:
        for entry in entries:
            if entry.path == target_path:
                return entry
        return None  # Not found
