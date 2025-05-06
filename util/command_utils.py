import os

from repo import Repository
from util.file_util import FileUtil, IndexEntry
from collections import Counter


def find_by_path(entries, path):
    for entry in entries:
        if entry.path == path:
            return entry
    return None


# branches/active_branch/top_commit/objects path
def get_head_objects_path(repository: Repository) -> str:
    head = get_head(repository)
    if head:
        head_objects_path = os.path.join(
            repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, head, repository.objects()
        )
        return head_objects_path
    else:
        return None

# read content of branches/active_branch/HEAD that is top commit
def get_head(repository: Repository) -> str:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, repository.head()
    )
    head = FileUtil.read_file_content(branch_head_path)
    return head

# to fix
def get_branch_objects_path(branch: str, repository: Repository) -> str:
    # return os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches(), branch, repository.objects())
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), branch, repository.head()
    )
    if os.path.isfile(branch_head_path):
        branch_head = FileUtil.read_file_content(branch_head_path)
        if branch_head:
            return os.path.join(
                repository.work_dir(), repository.storage_dir(), repository.branches(), branch, branch_head, repository.objects()
            )
        else:
            print(f"No branch head content(empty2): {branch_head}. path: {branch_head_path}")
            return ""
    else:
        print(f"No branch head path(2): {branch_head_path}")
        return ""

# change to / Add - get_branch_index_path

def get_head_commit_index_path(repository: Repository) -> str:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    return get_branch_head_commit_index_path(active_branch, repository)

def get_branch_head_commit_index_path(branch: str, repository: Repository) -> str:
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), branch, repository.head()
    )
    head_commit = FileUtil.read_file_content(branch_head_path)
    if head_commit:
        # parent_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches(), branch, repository.parent_branch())
        # if os.path.isfile(parent_branch_path):
        #     print("")
        commit_index_path = os.path.join(
            repository.work_dir(), repository.storage_dir(), repository.branches(), branch, head_commit, repository.index()
        )
        return commit_index_path
    # No commits yet
    else:
        print(f"No commits yet on {branch_head_path}")
        return None
    
def get_index_path(repository: Repository) -> str:
    return os.path.join(repository.work_dir(), repository.storage_dir(), repository.index())

# to fix . same as get_branch_head_commit_index_path
def get_index_path_by_branch(branch: str, repository: Repository) -> str:
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), branch, repository.head()
    )
    if os.path.isfile(branch_head_path):
        branch_head = FileUtil.read_file_content(branch_head_path)
        if branch_head:
            return os.path.join(
                repository.work_dir(), repository.storage_dir(), repository.branches(), branch, branch_head, repository.index()
            )
        else:
            print(f"No branch head content(empty): {branch_head}. path: {branch_head_path}")
            return ""
    else:
        print(f"No branch head path: {branch_head_path}")
        return ""


def get_index_entries(repository: Repository) -> list[IndexEntry]:
    index_file_path = get_index_path(repository)
    index_entries = FileUtil.parse_index_file_lines(index_file_path)
    return index_entries


def get_objects_path(repository: Repository) -> str:
    return os.path.join(repository.work_dir(), repository.storage_dir(), repository.objects())


def compare_index_sets(first: list[IndexEntry], second: list[IndexEntry]) -> bool:
    return Counter(first) != Counter(second)


def list_branches(repository: Repository) -> list[str]:
    branches_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches())
    return [entry.name for entry in os.scandir(branches_path) if entry.is_dir()]


def get_active_branch(repository: Repository) -> str:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    return FileUtil.read_file_content(active_branch_path)


def update_active_branch(repository: Repository, branch: str) -> None:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    FileUtil.overwrite_file(active_branch_path, branch)


def get_head_index_entries(repository: Repository) -> list[IndexEntry]:
    head_index_path = get_head_commit_index_path(repository)
    return FileUtil.parse_index_file_lines(head_index_path)


def is_exist_prev_commits(repository: Repository) -> bool:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, repository.head()
    )
    head: str = FileUtil.read_file_content(branch_head_path)
    return head != ""


# def at_least_one_commit_exist(repository: Repository) -> bool:
#     return get_head_objects_path(repository) == ""
