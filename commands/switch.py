from commands.commit import head_equals_to_index
from index_entry import IndexEntry
from registry import register
from repo import (
    build_branch_ref,
    build_index_entry,
    copy_object_to_work_dir,
    delete_work_dir_file,
    get_active_branch_name,
    get_active_branch_head_flat_tree_object,
    get_head_flat_tree_object_by_branch,
    get_index_entries,
    list_branches,
    overwrite_index_file,
    update_head_ref_to_branch,
)
from util.file_util import FileUtil


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
    # 2. update index
    flat_head_tree: list[dict[str, str]] = get_head_flat_tree_object_by_branch(switch_to)
    # index_entries: list[IndexEntry] = convert_flat_tree_to_index(flat_head_tree)
    # overwrite_index_file(index_entries)
    # 3 update work dir
    # get_all_work_files
    index_entries: list[IndexEntry] = get_index_entries()
    for entry in index_entries:
        delete_work_dir_file(entry.path)
    next_index_entries = []
    for blob in flat_head_tree:
        abs_path = copy_object_to_work_dir(blob.get("name"), blob.get("hash"))
        entry: IndexEntry = build_index_entry(abs_path)
        next_index_entries.append(entry)
    overwrite_index_file(next_index_entries)
    # 1
    update_head_ref_to_branch(build_branch_ref(switch_to))


def are_they_ucnommitted_changes() -> bool:
    flat_head_tree: list[dict[str, str]] = get_active_branch_head_flat_tree_object()
    index_entries: list[IndexEntry] = get_index_entries()
    return not head_equals_to_index(flat_head_tree, index_entries)
