# commands/add_command.py

from typing import Optional
from util.command_utils import find_by_path
from util.file_util import FileUtil, IndexEntry
from registry import register
from repo import Repository
import os
import traceback


@register("add")
def add_command(args):
    print(f"[add] Validating args size: {len(args)} [{' '.join(args)}]")

    repository = Repository()
    work_dir = repository.work_dir()
    print(f"[add] Working dir: {work_dir}")
    storage_dir = repository.storage_dir()
    storage_full_path = os.path.join(work_dir, storage_dir)

    if not FileUtil.is_dir_exist(storage_full_path):
        print("Not a git repository. Missing .git directory")
        return

    if args[0] == ".":
        print("[add] Handling: add . (add all changes)")
        index_file_path = os.path.join(storage_full_path, "index")
        index_entries = FileUtil.parse_index_file_lines(index_file_path)
        all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
        work_file_entries = FileUtil.transform_paths_to_entries(all_working_files)

        untracked_set = set()
        for ie in index_entries:
            if ie not in work_file_entries:
                untracked_set.add(ie)
        for wfe in work_file_entries:
            if wfe not in index_entries:
                untracked_set.add(wfe)

        untracked_path_set = {f.path[len(work_dir) + 1 :] for f in untracked_set}

        for rel_path in untracked_path_set:
            print(f"[add] Untracked set entry: {rel_path}")
            add_single_file(repository, rel_path)
    else:
        add_single_file(repository, args[0])


def add_single_file(repository, target_file):
    print("[add] Adding single file...")
    try:
        work_dir = repository.work_dir()
        storage_dir = repository.storage_dir()
        storage_full_path = os.path.join(work_dir, storage_dir)
        file_path = os.path.join(work_dir, target_file)
        index_file_path = os.path.join(storage_full_path, "index")

        if not FileUtil.is_dir_exist(storage_full_path):
            print("Not a git repository. Missing .git directory")
            return

        index_entries = FileUtil.parse_index_file_lines(index_file_path)
        is_target_exist_in_work_dir = FileUtil.is_file_exist(file_path)
        index_entry = find_by_path(index_entries, file_path)

        if index_entry:
            print("[add] File already tracked (in index)")
            if is_target_exist_in_work_dir:
                target_index_entry = FileUtil.build_index_entry(file_path)
                if target_index_entry.sha1 == index_entry.sha1 and target_index_entry.size == index_entry.size:
                    print("[add] File unchanged; already staged.")
                else:
                    print("[add] File modified; updating staging area.")
                    index_entry.size = target_index_entry.size
                    index_entry.sha1 = target_index_entry.sha1
                    index_entry.mod_time = target_index_entry.mod_time
                    FileUtil.update_index_file(index_file_path, index_entries)
                    path_in_objects = os.path.join(storage_full_path, "objects", target_file)
                    FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
            else:
                print("[add] File deleted; removing from index.")
                index_entries = remove_entry_by_path(index_entries, file_path)
                FileUtil.update_index_file(index_file_path, index_entries)
                path_in_objects = os.path.join(storage_full_path, "objects", target_file)
                os.remove(path_in_objects)
        else:
            if is_target_exist_in_work_dir:
                print("[add] New file found; adding to index.")
                target_index_entry = FileUtil.build_index_entry(file_path)
                index_entries.append(target_index_entry)
                FileUtil.update_index_file(index_file_path, index_entries)
                path_in_objects = os.path.join(storage_full_path, "objects", target_file)
                FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
            else:
                print("[add] File not found in working directory or index. Skipping.")

    except Exception as e:
        print(f"[add] Add failed: {e}")
        traceback.print_exc()
        return -1


def remove_entry_by_path(entries: list[IndexEntry], path: str) -> list[IndexEntry]:
    return [e for e in entries if e.path != path]
