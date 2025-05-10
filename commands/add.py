import os
from registry import register
from repo import build_index_entry, convert_file_to_work_dir_path, get_index_file_path, get_path_in_objects, get_storage_root
from util.command_utils import find_by_path
from util.file_util import FileUtil, IndexEntry
import traceback


@register("add")
def add_single_file(args, staged) -> None:
    try:
        print(f"add single file: {args[0]}")
        target_file = convert_file_to_work_dir_path(args[0])
        storage_full_path = get_storage_root()
        if not FileUtil.is_dir_exist(storage_full_path):
            print("The work dir is not a git repository. Missing .git directory")
            return
        print(f"Add 1 file: {target_file}")
        index_file_path = get_index_file_path()
        print(f"Add 2 index path: {index_file_path}")
        is_target_exist_in_work_dir = FileUtil.is_file_exist(target_file)
        print(f"Add 3 is file :{target_file} exist in word dir: {is_target_exist_in_work_dir}")
        if FileUtil.is_file_exist(index_file_path):
            index_entries = FileUtil.parse_index_file_lines(index_file_path)
            entry_from_index = find_by_path(index_entries, args[0])
            if is_target_exist_in_work_dir:
                target_index_entry = build_index_entry(target_file)
                print(f"Target file index entry: {target_index_entry}")
                if entry_from_index:  # entry in index and in work dir. check if it equals or modified
                    if target_index_entry == entry_from_index:
                        print(f"Target file already staged. Not modified. Nothing to add: {args[0]}")
                    else:
                        entry_from_index.mod_time = target_index_entry.mod_time
                        entry_from_index.stage_num = target_index_entry.stage_num
                        entry_from_index.sha1 = target_index_entry.sha1
                        entry_from_index.size = target_index_entry.size
                        FileUtil.update_index_file(index_file_path, index_entries)
                        path_in_objects = get_path_in_objects(target_index_entry.sha1)
                        FileUtil.add_file_to_objects(target_file, path_in_objects)
                        print(f"Target file modified. Updated in stage: {args[0]}")
                else:  # file not in staging. exists in work dir. add to staging
                    index_entries.append(target_index_entry)
                    FileUtil.update_index_file(index_file_path, index_entries)
                    path_in_objects = get_path_in_objects(target_index_entry.sha1)
                    FileUtil.add_file_to_objects(target_file, path_in_objects)
                    print(f"New file added to stage {args[0]}. Path in objects: {path_in_objects}")
            else:  # target not in work dir. index exists. Remove from staging the file that removed from work dir
                if entry_from_index:
                    index_entries = _remove_entry_by_path(index_entries, args[0])
                    FileUtil.update_index_file(index_file_path, index_entries)
                    print(f"File deletion staged {args[0]}")
                else:
                    print("Nothing to add. File does not exist in working directory nor in staging")
        else:  # no index file yet
            if is_target_exist_in_work_dir:
                target_index_entry = build_index_entry(target_file)
                FileUtil.update_index_file(index_file_path, [target_index_entry])
                path_in_objects = get_path_in_objects(target_index_entry.sha1)
                FileUtil.add_file_to_objects(target_file, path_in_objects)
                print(f"Added new index entry: {target_index_entry}")
            else:
                print("Nothing to add. File does not exist in working directory nor in index")
    except Exception as e:
        print(f"add failed. {e}")
        traceback.print_exc()
        return -1


def _remove_entry_by_path(entries: list[IndexEntry], path: str) -> list[IndexEntry]:
    return [e for e in entries if e.path != path]
