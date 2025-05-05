import os

from repo import Repository
from util.file_util import FileUtil, IndexEntry
from collections import Counter


def find_by_path(entries, path):
    for entry in entries:
        if entry.path == path:
            return entry
    return None


def get_head_objects_path(repository: Repository) -> str:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, repository.head()
    )
    head = FileUtil.read_file_content(branch_head_path)
    if head:
        head_objects_path = os.path.join(
            repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, head, repository.objects()
        )
        return head_objects_path
    else:
        return None


def get_top_commit(repository: Repository) -> str:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, repository.head()
    )
    head = FileUtil.read_file_content(branch_head_path)
    if head:
        commit_index_path = os.path.join(
            repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, head, repository.index()
        )
        return commit_index_path
    else:
        return None


def get_index_path(repository: Repository) -> str:
    return os.path.join(repository.work_dir(), repository.storage_dir(), repository.index())


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


def get_active_branch(repository: Repository) -> list[str]:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    return FileUtil.read_file_content(active_branch_path)


def update_active_branch(repository: Repository, branch: str) -> None:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    FileUtil.overwrite_file(active_branch_path, branch)


def get_head_index_entries(repository: Repository) -> list[IndexEntry]:
    head_index_path = get_top_commit(repository)
    return FileUtil.parse_index_file_lines(head_index_path)


def is_exist_prev_commits(repository: Repository) -> bool:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    branch_head_path = os.path.join(
        repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, repository.head()
    )
    head: str = FileUtil.read_file_content(branch_head_path)
    return head != ""
