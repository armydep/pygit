from registry import register
from repo import Repository
from util.command_utils import get_active_branch, list_branches


@register("branch")
def branch_command(args, stgaded):
    repository = Repository()
    print(f"[branch]")
    branches: list[str] = list_branches(repository)
    active_branch = get_active_branch(repository)
    for b in branches:
        if active_branch == b:
            print(f"\t{b} *")
        else:
            print(f"\t{b}")
