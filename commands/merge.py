from registry import register
from repo import Repository
from util.command_utils import get_index_entries, get_top_commit
from util.file_util import IndexEntry


@register("merge")
def merge_command(args, stgaded):
    repository = Repository()
    print(f"[merge]")
    index_entries: list[IndexEntry] = get_index_entries(repository)
    prev_commit_index_path = get_top_commit(repository)
