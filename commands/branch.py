import os
from registry import register
from repo import Repository
from util.command_utils import at_least_one_commit_exist, get_active_branch, get_head, list_branches
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
        head = get_head(repository)
        if head:  # at_least_one_commit_exist
            parent = ""
            branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches(), args[0])
            FileUtil.create_dir_if_not_exist(branch_path)
            # created /wd/.storage/branches/new branch

            branch_head_path = os.path.join(branch_path, repository.head())
            # current head >  /wd/.storage/branches/new branch/parent
            FileUtil.write_lines_to_file(branch_head_path, parent)
            branches.append(args[0])
            print("Created")
        else:
            print("Create at least one commit before creating a new branch")

    print(f"[branch]")
    active_branch = get_active_branch(repository)
    for b in branches:
        if active_branch == b:
            print(f"\t{b} *")
        else:
            print(f"\t{b}")


def is_valid_identifier(s1: str) -> bool:
    return bool(s1) and s1.isalnum() and not s1[0].isdigit()
