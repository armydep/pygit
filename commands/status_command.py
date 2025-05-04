from registry import register
from repo import Repository
from util.command_utils import find_by_path
from util.file_util import FileUtil
import os


@register("status")
def status_command(args):
    repository = Repository()
    work_dir = repository.work_dir()
    storage_dir = repository.storage_dir()
    all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
    index_file = "index"
    storage_full_path = os.path.join(work_dir, storage_dir)
    index_file_path = os.path.join(storage_full_path, index_file)
    index_file_path = os.path.join(storage_full_path, index_file)
    index_entries = FileUtil.parse_index_file_lines(index_file_path)
    all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
    work_file_entries = FileUtil.transform_paths_to_entries(all_working_files)
    changes_found = False
    for wfe in work_file_entries:
        if wfe not in index_entries:
            index_entry = find_by_path(index_entries, wfe.path)
            if index_entry:
                print(f"Modified: {index_entry.path}")
                changes_found = True
            else:
                print(f"Untracked (new): {wfe.path}")
                changes_found = True

    for ie in index_entries:
        if ie not in work_file_entries:
            wd_entry = find_by_path(work_file_entries, ie.path)
            if not wd_entry:
                print(f"Deleted: {ie.path}")
                changes_found = True

    if not changes_found:
        print("No changes")
