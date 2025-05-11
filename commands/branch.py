from registry import register
from repo import create_head_commit_ref_for_branch, get_active_branch_name, get_head_hash, list_branches


@register("branch")
def branch_command(args, stgaded):
    """Lists all branches.
    If second args exist and valid and such branch not already exists then creates a new branch.
    Stays on current branch
    Args: branch name. Optional
    Returns: nothing
    """
    branches: list[str] = list_branches()
    if not branches:
        print("[branch] No commits yet. No branches")
        return
    active_branch = get_active_branch_name()
    if len(args) == 1:
        if is_valid_branch_name(args[0]) and args[0] not in branches:
            head_hash = get_head_hash()
            create_head_commit_ref_for_branch(head_hash, args[0])
            print(f"[branch] Created. head hash: {head_hash}")
        else:
            print(f"[branch] Invalid branch name: {args[0]}")
        return

    print(f"[branch]")
    for b in branches:
        if active_branch == b:
            print(f"\t{b} *")
        else:
            print(f"\t{b}")


def is_valid_branch_name(arg: str) -> bool:
    return bool(arg) and arg.isalnum() and not arg[0].isdigit() and len(arg) > 2
