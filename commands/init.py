from util.file_util import FileUtil
from registry import register
import os
import traceback
from repo import Repository


@register("init")
def init_command(args, staged):
    try:
        repo = Repository()
        # 1
        storage_full_path = os.path.join(repo.work_dir(), repo.storage_dir())
        FileUtil.create_dir_if_not_exist(storage_full_path)
        # 2 create branches
        branches_dir = os.path.join(storage_full_path, repo.branches())
        FileUtil.create_dir_if_not_exist(branches_dir)
        # 3 create default branch under branches
        default_branche_dir = os.path.join(branches_dir, repo.default_branch())
        FileUtil.create_dir_if_not_exist(default_branche_dir)
        # 4
        head_path = os.path.join(default_branche_dir, repo.head())
        FileUtil.write_lines_to_file(head_path, "")
        # FileUtil.create_dir_if_not_exist(os.path.join(default_branche_dir, repo.objects()))

        # 5 create active branch
        active_branch_file_path = os.path.join(storage_full_path, repo.active_branch())
        FileUtil.create_file_and_write(active_branch_file_path, repo.default_branch() + "\n")

        index_file_path = os.path.join(storage_full_path, repo.index())
        FileUtil.write_lines_to_file(index_file_path, "")
        objects_dir_path = os.path.join(storage_full_path, repo.objects())
        FileUtil.create_dir_if_not_exist(objects_dir_path)
        print(f"init done. root: {repo.work_dir()}")
    except Exception as e:
        print(f"init failed. {e}")
        traceback.print_exc()
        return -1
