from util.file_util import FileUtil
from registry import register
import os
import traceback
from repo import Repository

@register("init")
def init_command(args):
    print("Im init command exec")
    try:
        repo = Repository()
        work_dir = repo.work_dir()
        print(f"working dir: {work_dir}")
        storage_dir = repo.storage_dir()
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
        index_file = "index"
        index_file_path = os.path.join(storage_full_path, index_file)
        FileUtil.write_lines_to_file(index_file_path, "")
        objects_dir = "objects"
        objects_dir_path = os.path.join(storage_full_path, objects_dir)
        FileUtil.create_dir_if_not_exist(objects_dir_path)

    except Exception as e:
        print(f"init failed. {e}")
        traceback.print_exc()
        return -1
