from repo import (
    build_default_branch_ref,
    get_objects_path,
    get_refs_heads_path,
    get_storage_root,
    get_work_dir,
    update_head_ref_to_branch,
)
from util.file_util import FileUtil
from registry import register
import traceback


"""
.git
    HEAD - refs/heads/main
    index - empty
    refs
        heads
    objects
"""


@register("init")
def init_command(args, staged):
    try:
        # 1 create .git
        storage_root = get_storage_root()
        FileUtil.create_dir_if_not_exist(storage_root)

        # 3 create refs/heads/ empty //<main branch>
        refs_heads_path = get_refs_heads_path()
        FileUtil.create_dir_if_not_exist(refs_heads_path)

        # 4 create objects
        FileUtil.create_dir_if_not_exist(get_objects_path())

        # 5 create HEAD - refs/heads/<main br>
        update_head_ref_to_branch(build_default_branch_ref())

        print(f"init done. root: {get_work_dir()}")

    except Exception as e:
        print(f"init failed. {e}")
        traceback.print_exc()
        return -1
