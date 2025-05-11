from collections import Counter
from commands.commit import head_equals_to_index, index_tree_found_in_flat_tree_object
from index_entry import IndexEntry
from registry import register
from repo import find_by_path, get_all_work_files, get_active_branch_head_flat_tree_object, get_index_entries, get_storage_root
from util.file_util import FileUtil


@register("status")
def status_command(args, staged):
    if not FileUtil.is_dir_exist(get_storage_root()):
        print("The work dir is not a git repository. Missing .git directory")
        return
    work_file_entries: list[IndexEntry] = get_all_work_files()
    print(f"All work files size:{len(work_file_entries)}")
    index_entries: list[IndexEntry] = get_index_entries()
    print(f"Index entries size:{len(index_entries)}. Are sets differs: {compare_index_sets(index_entries, work_file_entries)}")
    # 1. work dir vs staging area
    print("1. Changes to be staged. (Work dir vs staging area check)")
    if not compare_index_sets(index_entries, work_file_entries):
        print("\tNo changes to be staged")
    else:
        for wfe in work_file_entries:
            if wfe not in index_entries:
                index_entry = find_by_path(index_entries, wfe.path)
                if index_entry:
                    print(f"\tModified: {index_entry.path}")
                else:
                    print(f"\tUntracked: {wfe.path}")

        for ie in index_entries:
            if ie not in work_file_entries:
                wd_entry = find_by_path(work_file_entries, ie.path)
                if not wd_entry:
                    print(f"\tDeleted: {ie.path}")

    # 2. staging area vs head commit
    print("2. Changes to be commited. (Staging area vs latest commit check)")
    flat_head_tree: list[dict[str, str]] = get_active_branch_head_flat_tree_object()
    if flat_head_tree:
        if head_equals_to_index(flat_head_tree, index_entries):
            print(f"\tNothing to commit")
        else:
            for blob in flat_head_tree:
                entry = find_by_path(index_entries, blob.get("name"))
                if entry:
                    if entry.sha1 != blob.get("hash"):
                        print(f"\tmodified: {index_entry.path}")
                else:
                    print(f"\tdeleted: {blob.get("name")}")

            for entry in index_entries:
                if not index_tree_found_in_flat_tree_object(entry, flat_head_tree):
                    blob = find_by_path_in_flat_tree(flat_head_tree, entry.path)
                    if not blob:
                        print(f"\tnew file: {entry.path}")

    else:
        if index_entries:
            print("\tChanges to be committed (from staging area). No commits yet")
            for ie in index_entries:
                print(f"\t\t{ie.path}")
        else:
            print("\tNo commits yet. Nothing in staged area and nothing to commit")


def find_by_path_in_flat_tree(flat_tree: list[dict[str, str]], name: str) -> dict[str, str]:
    return next((blob for blob in flat_tree if blob.get("name") == name), None)


def compare_index_sets(first: list[IndexEntry], second: list[IndexEntry]) -> bool:
    return Counter(first) != Counter(second)
