from commands.commit import head_equals_to_index
from index_entry import IndexEntry
from registry import register
from repo import (
    build_branch_ref,
    convert_file_to_work_dir_path,
    copy_object_to_work_dir,
    delete_work_dir_file,
    flat_tree_to_index,
    get_active_branch_name,
    get_active_branch_head_flat_tree_object,
    get_head_flat_tree_object_by_branch,
    get_index_entries,
    list_branches,
    overwrite_index_file,
    update_head_ref_to_branch,
)


@register("switch")
def switch_command(args, stgaded):
    print(f"[switch] {len(args)}")
    if len(args) != 1:
        print(f"Invalid command. Provide a branch name")
        return

    switch_to = args[0]
    active_branch = get_active_branch_name()

    # 1
    if switch_to == active_branch:
        print(f"No switch required. Already on: {active_branch}")
        return
    # 2
    branches: list[str] = list_branches()
    if switch_to not in branches:
        print(f"Specified branch does not exist: {switch_to}")
        return

    if are_they_ucnommitted_changes():
        print(f"There are uncommitted changes on current branch. Commit or unstage before switching")
        return

    switch(switch_to)


def switch(switch_to: str) -> None:
    flat_head_tree: list[dict[str, str]] = get_head_flat_tree_object_by_branch(switch_to)
    index_entries: list[IndexEntry] = get_index_entries()
    for entry in index_entries:
        delete_work_dir_file(entry.path)

    for blob in flat_head_tree:
        dest_abs_path = convert_file_to_work_dir_path(blob.get("name"))
        copy_object_to_work_dir(dest_abs_path, blob.get("hash"))

    next_index_entries = flat_tree_to_index(flat_head_tree)
    overwrite_index_file(next_index_entries)
    update_head_ref_to_branch(build_branch_ref(switch_to))


def are_they_ucnommitted_changes() -> bool:
    flat_head_tree: list[dict[str, str]] = get_active_branch_head_flat_tree_object()
    index_entries: list[IndexEntry] = get_index_entries()
    return not head_equals_to_index(flat_head_tree, index_entries)
