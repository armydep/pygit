import os
from registry import register
from repo import Repository
from util.command_utils import get_active_branch, list_branches
from util.file_util import FileUtil


@register("branch")
def branch_command(args, stgaded):
    """Lists all branches.
    If second args exist and valid and such branch not already exists then creates a new branch.
    Stays on current branch
    Args: branch name. Optional
    Returns: nothing
    """
    repository = Repository()
    branches: list[str] = list_branches(repository)
    if len(args) == 1 and is_valid_identifier(args[0]) and args[0] not in branches:
        branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches(), args[0])
        FileUtil.create_dir_if_not_exist(branch_path)
        branch_obj_path = os.path.join(branch_path, repository.objects())
        FileUtil.create_dir_if_not_exist(branch_obj_path)
        branch_head_path = os.path.join(branch_path, repository.head())
        FileUtil.write_lines_to_file(branch_head_path, "")
        branches.append(args[0])
        print("Created")

    print(f"[branch]")
    active_branch = get_active_branch(repository)
    for b in branches:
        if active_branch == b:
            print(f"\t{b} *")
        else:
            print(f"\t{b}")


def is_valid_identifier(s1: str) -> bool:
    return bool(s1) and s1.isalnum() and not s1[0].isdigit()
