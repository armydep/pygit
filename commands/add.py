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


            objects_dir = "objects"
            index_file = "index"
            index_file_path = os.path.join(storage_full_path, index_file)
            index_entries = FileUtil.parse_index_file_lines(index_file_path)

            # if not FileUtil.is_file_exist(file_path):
            #     print(f"Specified file does not exists {file_path}. Will be removed from index if it were there")
            #     return
            
            is_target_exist_in_work_dir = FileUtil.is_file_exist(file_path)

            index_entry = self._find_index_entry_by_path(index_entries, file_path)
            if index_entry:
                print("The file required to add to tracking is found in index (will be added/removed depend on modified or not in work_dir)")
                if is_target_exist_in_work_dir:
                    target_index_entry = FileUtil.build_index_entry(file_path)
                    print(f"Target Index entry:{target_index_entry}")
                    # todo: replace by target.equals to index
                    if target_index_entry.sha1 == index_entry.sha1 and target_index_entry.size == index_entry.size:
                        print("The file is already staged and wasnt changed since that moment. No add required")
                    else:
                        print("Exist in stage but modified. Replacing")
                        index_entry.size = target_index_entry.size
                        index_entry.sha1 = target_index_entry.sha1
                        index_entry.mod_time = target_index_entry.mod_time
                        FileUtil.update_index_file(index_file_path, index_entries)
                        path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)
                        FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
                else:
                    print("The file was in index and now removed from the workd_dir. Removing from index")
                    index_entries = self._remove_entry_by_path(index_entries, file_path)
                    FileUtil.update_index_file(index_file_path, index_entries)
                    path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)
                    os.remove(path_in_objects)

            else:
                if is_target_exist_in_work_dir:
                    print("The file required to add to tracking is in work_dir and NOT found in index. Adding to index")
                    index_entries.append(target_index_entry)
                    FileUtil.update_index_file(index_file_path, index_entries)
                    path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)
                    FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
                else:
                    print("The target file is not in work_dir, NOR in index. Nothing to add")

        except Exception as e:
            print(f"add failed. {e}")
            traceback.print_exc()
            return -1

    # @staticmethod
    # def _index_contains_entry(index_entries: list[IndexEntry], entry: IndexEntry) -> bool:
    #     return any(itent.path and itent.path == entry.path for itent in index_entries)

    @staticmethod
    def _find_index_entry_by_path(entries: list[IndexEntry], target_path: str) -> Optional[IndexEntry]:
        for entry in entries:
            if entry.path == target_path:
                return entry
        return None  # Not found

    # todo: move into IndexEntry
    @staticmethod
    def _remove_entry_by_path(entries: list[IndexEntry], path: str) -> list[IndexEntry]:
        return [e for e in entries if e.path != path]
