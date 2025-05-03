from util.file_util import FileUtil
from .command import Command
import os
import traceback


class InitCommand(Command):
    def validate(self) -> None:
        print(f"Im init command validation. args size: {len(self.args)}")

    def exec(self) -> None:
        print("Im init command exec")
        try:
            work_dir = self.repository.work_dir()
            print(f"working dir: {work_dir}")
            storage_dir = self.repository.storage_dir()
            storage_full_path = os.path.join(work_dir, storage_dir)
            # 1
            FileUtil.create_dir_if_not_exist(storage_full_path)
            print(f"storage created ok: {storage_full_path}")
            # 2 create branches
            branches_dir_name = "branches"
            branches_dir = os.path.join(storage_full_path, branches_dir_name)
            FileUtil.create_dir_if_not_exist(branches_dir)
            # 3 create default branch under branches
            default_branch = "main"
            default_branche_dir = os.path.join(branches_dir, default_branch)
            FileUtil.create_dir_if_not_exist(default_branche_dir)
            # 4
            head_file = "HEAD"
            index_file_path = os.path.join(default_branche_dir, head_file)
            FileUtil.write_lines_to_file(index_file_path, "")
            # 5 create active branch
            active_branch_file = "active_branch"
            active_branch_file_dir = os.path.join(storage_full_path, active_branch_file)
            FileUtil.create_file_and_write(active_branch_file_dir, default_branch + "\n")
            # 6 create list of working files
            #all_files = FileUtil.list_all_files(work_dir, storage_dir)
            # 7 create index file
            index_file = "index"
            index_file_path = os.path.join(storage_full_path, index_file)
            FileUtil.write_lines_to_file(index_file_path, "")
            # FileUtil.write_lines_to_file(index_file_path, all_files)
            # 8 for all file in list of files in working dir
            #       add file to active / default / current branch
            objects_dir = "objects"
            objects_dir_path = os.path.join(storage_full_path, objects_dir)
            FileUtil.create_dir_if_not_exist(objects_dir_path)
            # files_list = FileUtil.list_dir_non_recursive_with_exclude(work_dir, storage_dir)
            # for f in files_list:
            #     FileUtil.copy_to_directory(f, objects_dir_path)

        except Exception as e:
            print(f"init failed. {e}")
            traceback.print_exc()
            return -1
