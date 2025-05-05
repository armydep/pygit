import shutil
from registry import register
from repo import Repository
from util.command_utils import (
    compare_index_sets,
    get_active_branch,
    get_branch_objects_path,
    get_head_index_entries,
    get_head_objects_path,
    get_index_entries,
    get_index_path,
    get_index_path_by_branch,
    get_objects_path,
    is_exist_prev_commits,
    list_branches,
    update_active_branch,
)
from util.file_util import FileUtil, IndexEntry


@register("switch")
def switch_command(args, stgaded):
    repository = Repository()
    print(f"[switch] {len(args)}")
    if len(args) != 1:
        print(f"Invalid command. Provide a branch name")
        return

    switch_to = args[0]
    active_branch = get_active_branch(repository)

    # 1
    if switch_to == active_branch:
        print(f"No switch required. Already on: {active_branch}")
        return
    # 2
    branches: list[str] = list_branches(repository)
    if switch_to not in branches:
        print(f"Specified branch does not exist: {switch_to}")
        return

    # 3 check if state allows switch. if there are no uncommitted changes
    index_entries = get_index_entries(repository)
    if not is_exist_prev_commits(repository):
        print("Ok to switch. no commits yet")
        switch(switch_to, repository)
    else:
        head_index_entries = get_head_index_entries(repository)
        if compare_index_sets(index_entries, head_index_entries):
            print(f"There are staged changes. Commit changes / restore / stash before switching to another branch")
        else:
            switch(switch_to, repository)


def switch(switch_to: str, repository: Repository) -> None:
    # 4 update index
    # FileUtil.overwrite_file()
    index_path = get_index_path(repository)
    switch_to_index_path = get_index_path_by_branch(switch_to, repository)
    print(f"Ok branch index: {switch_to_index_path}. index_path: {index_path}")
    if not switch_to_index_path:
        FileUtil.update_index_file(index_path, [])
    else:
        shutil.copy2(switch_to_index_path, index_path)
    # 5 update objects
    index_objects_path = get_objects_path(repository)
    switch_to_objects_path = get_branch_objects_path(switch_to, repository)
    print(f"Copy objects from: {switch_to_objects_path}, to: {index_objects_path}")
    FileUtil.clear_dir(index_objects_path)
    if switch_to_objects_path:
        FileUtil.copy_dir_contents(switch_to_objects_path, index_objects_path)
    # # 6 update active branch
    # 7 update work dir
    FileUtil.delete_all_except(repository.work_dir(), repository.storage_dir())
    FileUtil.copy_dir_contents(index_objects_path, repository.work_dir())
    update_active_branch(repository, switch_to)
    print(f"Switched to: {switch_to}")
