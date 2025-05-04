import os
from repo import Repository
from util.file_util import FileUtil


def find_by_path(entries, path):
    for entry in entries:
        if entry.path == path:
            return entry
    return None


def get_top_commit(repository: Repository) -> str:
    active_branch_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.active_branch())
    active_branch = FileUtil.read_file_content(active_branch_path)
    branch_head_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, repository.head())
    head = FileUtil.read_file_content(branch_head_path)
    if head :
        commit_index_path = os.path.join(repository.work_dir(), repository.storage_dir(), repository.branches(), active_branch, head, repository.index())
        return commit_index_path
    else:            
        return None
