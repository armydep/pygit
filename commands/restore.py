from commands.commit import head_equals_to_index
from index_entry import IndexEntry
from registry import register
from repo import flat_tree_to_index, get_active_branch_head_flat_tree_object, get_index_entries, overwrite_index_file


@register("restore")
def restore_command(args, stgaded):
    print(f"[restore] staged:{stgaded}")
    index_entries: list[IndexEntry] = get_index_entries()
    flat_head_tree: list[dict[str, str]] = get_active_branch_head_flat_tree_object()
    if flat_head_tree:
        if not head_equals_to_index(flat_head_tree, index_entries):
            head_index_entries = flat_tree_to_index(flat_head_tree)
            overwrite_index_file(head_index_entries)
            print(f"[restore] done")
        else:
            print(f"[restore] Nothing to restore. Head no changed")
    else:
        if index_entries:
            print(f"[restore] staged:{stgaded}")
            overwrite_index_file([])
        else:
            print(f"[restore] Nothing to restore. No head, no index/staging")
