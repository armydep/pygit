from registry import register
from repo import Repository
from util.command_utils import find_by_path, get_top_commit
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
    # 1. work dir vs staging area
    print("1. Changes not staged for commit. (Work dir vs staging area check)")
    for wfe in work_file_entries:
        if wfe not in index_entries:
            index_entry = find_by_path(index_entries, wfe.path)
            if index_entry:
                print(f"\tModified: {index_entry.path}")
            else:
                print(f"\tUntracked (new): {wfe.path}")
            changes_found = True

    for ie in index_entries:
        if ie not in work_file_entries:
            wd_entry = find_by_path(work_file_entries, ie.path)
            if not wd_entry:
                print(f"\tDeleted: {ie.path}")
                changes_found = True
    if not changes_found:
        print("\tNo changes")

    # 2. staging area vs latest commit
    print("2. Changes to be commited. (Staging area vs latest commit check)")

    prev_commit_index_path = get_top_commit(repository)
    if prev_commit_index_path:
        changes_found = False
        prev_index_entries = FileUtil.parse_index_file_lines(prev_commit_index_path)
        for pie in prev_index_entries:
            if pie not in index_entries:
                index_entry = find_by_path(index_entries, pie.path)
                if index_entry:
                    print(f"\tmodified: {index_entry.path}")
                else:
                    print(f"\tdeleted: {pie.path}")
                changes_found = True

        for ie in index_entries:
            if ie not in prev_index_entries:
                pv_entry = find_by_path(prev_index_entries, ie.path)
                if not pv_entry:
                    print(f"\tnew file: {ie.path}")
                    changes_found = True
        if not changes_found:
            print(f"\tNothing to commit")
    else:
        if index_entries:
            print("\tChanges to be committed (from staging area). No commits yet")
            for ie in index_entries:
                print(f"\t\t{ie.path}")
        else:
            print("\tNo commits yet. Nothing in staged area and nothing to commit")
