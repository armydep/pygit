from repo import Repository
from util.file_util import FileUtil, IndexEntry
import os
import time
from collections import Counter
from registry import register


@register("commit")
def commit_command(args):
    print("[commit] Validation: " + "_".join(args))

    repo = Repository()
    WORK_DIR = repo.work_dir()
    print(f"working dir: {WORK_DIR}")
    STORAGE_DIR = repo.storage_dir()
    storage_full_path = os.path.join(WORK_DIR, STORAGE_DIR)

    if not FileUtil.is_dir_exist(storage_full_path):
        print("The work dir is not a git repository. missing .git directory")
        return

    # objects_dir = "objects"
    index_file = "index"
    index_file_path = os.path.join(storage_full_path, index_file)
    index_entries = FileUtil.parse_index_file_lines(index_file_path)

    active_branch_file = "active_branch"
    active_branch_file_path = os.path.join(storage_full_path, active_branch_file)
    active_branch = FileUtil.read_file_content(active_branch_file_path)
    print(f"Active branch: {active_branch}")

    branches_dir_name = "branches"
    head_file = "HEAD"
    active_branch_head_path = os.path.join(storage_full_path, branches_dir_name, active_branch, head_file)
    head = FileUtil.read_file_content(active_branch_head_path)
    print(f"Active branch head: {head}")

    branch_root = os.path.join(storage_full_path, branches_dir_name, active_branch)
    print(f"curr branch root:{branch_root}")

    if not index_entries and not head:
        print("Nothing to commit. No commits yet happen. Nothing staged and no prev commits(empty repo). (case-0)")
        return

    #
    # 1. no staging no commits                       -> 0 1 - nothing to commit
    # 2. there is a staging and there are no commits -> commit-0 2 / commit all as is first commit
    # 3. there is commit                             -> commit-2 / commit only if there is a diff / ??? nothing to commit / create new commit with empty repo space

    # no such case
    # 4. there is commit and there is a staging      -> commit-2 / commit only if there is a diff between staging and last commit
    #
    # if exist at least one commit
    # else
    # if index is different from last commit
    #
    # if index_entries:

    # No commits yet happen. First commit. Will be check if there are staged files by diff index against last commit
    if not head:
        print("Commit all. First commit. (case-1)")
        commit_name = str(time.time_ns())
        commit_path = os.path.join(branch_root, commit_name, "objects")
        os.makedirs(commit_path)
        FileUtil.overwrite_file(active_branch_head_path, commit_name)
        print(f"Commit created: {commit_path}")

        objects_dir = "objects"
        path_in_objects = os.path.join(storage_full_path, objects_dir)
        print(f"Copy objects from {path_in_objects} -> {commit_path}")
        FileUtil.copy_dir_contents(path_in_objects, commit_path)
        FileUtil.copy_to_directory(index_file_path, os.path.join(branch_root, commit_name))

        return

    # There were commits.
    # Now we should detect if there are staged files since last commit
    commit_index_path = os.path.join(branch_root, head, "index")
    print(f"There are prev commits. Lets diff. head commit file: {commit_index_path}")
    # commit_index_content = FileUtil.read_file_content(commit_st)
    # print(f"Commit index: {commit_index_content}")
    commit_index_entries = FileUtil.parse_index_file_lines(commit_index_path)

    if _index_entries_diff(index_entries, commit_index_entries):
        print(f"There are staged changes. Commiting")

        commit_name = str(time.time_ns())
        commit_path = os.path.join(branch_root, commit_name, "objects")
        print(f"Creating a commit dir: {commit_path}")
        os.makedirs(commit_path)

        FileUtil.overwrite_file(active_branch_head_path, commit_name)
        # print(f"Commit created: {commit_path}")
        objects_dir = "objects"
        path_in_objects = os.path.join(storage_full_path, objects_dir)
        print(f"Copy objects from {path_in_objects} -> {commit_path}")
        FileUtil.copy_dir_contents(path_in_objects, commit_path)
        FileUtil.copy_to_directory(index_file_path, os.path.join(branch_root, commit_name))
        # add reference to parent commit
        # commit_index_path = os.path.join(branch_root, head, "index")
        commit_parent_path = os.path.join(branch_root, commit_name, "parent")
        print(f"Parent commit: {commit_parent_path}")
        FileUtil.overwrite_file(commit_parent_path, head)
    else:
        print(f"No staged changes since last commit, index - {commit_index_path}. Nothing to commit")


def _index_entries_diff(index_entries: list[IndexEntry], commit_index_entries: list[IndexEntry]) -> bool:
    return Counter(index_entries) != Counter(commit_index_entries)
