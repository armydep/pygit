from registry import register
from repo import (
    build_index_entry,
    convert_file_to_work_dir_path,
    find_by_path,
    get_all_work_files,
    get_index_entries,
    get_index_file_path,
    get_path_in_objects,
    get_storage_root,
    get_work_dir,
    overwrite_index_file,
)
from util.file_util import FileUtil, IndexEntry
import traceback


@register("add")
def add_command(args, staged):

    if not FileUtil.is_dir_exist(get_storage_root()):
        print("The work dir is not a git repository. Missing .git directory")
        return
    if args[0] == ".":
        index_entries: list[IndexEntry] = get_index_entries()
        work_file_entries = get_all_work_files()
        untracked_set = set()
        for ie in index_entries:
            if ie not in work_file_entries:
                untracked_set.add(ie)
        for wfe in work_file_entries:
            if wfe not in index_entries:
                untracked_set.add(wfe)
        untracked_path_set = set()
        # abs_path = "/tmp/pygit/repo_work_dir_root/"
        for f in untracked_set:
            # rel_path = f.path[len(get_work_dir()) + 1 :]
            # print(f"Add. orig: {f.path}. result: {rel_path}")
            # untracked_path_set.add(rel_path)
            untracked_path_set.add(f.path)
        for f in untracked_path_set:
            print(f"Untracked set entry: {f}")
            add_single_file(f)
    else:
        add_single_file(args[0])


def add_single_file(file_path) -> None:
    try:
        print(f"add single file: {file_path}")
        target_file = convert_file_to_work_dir_path(file_path)
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
            entry_from_index = find_by_path(index_entries, file_path)
            if is_target_exist_in_work_dir:
                target_index_entry = build_index_entry(target_file)
                print(f"Target file index entry: {target_index_entry}")
                if entry_from_index:  # entry in index and in work dir. check if it equals or modified
                    if target_index_entry == entry_from_index:
                        print(f"Target file already staged. Not modified. Nothing to add: {file_path}")
                    else:
                        entry_from_index.mod_time = target_index_entry.mod_time
                        entry_from_index.stage_num = target_index_entry.stage_num
                        entry_from_index.sha1 = target_index_entry.sha1
                        entry_from_index.size = target_index_entry.size
                        overwrite_index_file(index_entries)
                        path_in_objects = get_path_in_objects(target_index_entry.sha1)
                        FileUtil.add_file_to_objects(target_file, path_in_objects)
                        print(f"Target file modified. Updated in stage: {file_path}")
                else:  # file not in staging. exists in work dir. add to staging
                    index_entries.append(target_index_entry)
                    overwrite_index_file(index_entries)
                    path_in_objects = get_path_in_objects(target_index_entry.sha1)
                    FileUtil.add_file_to_objects(target_file, path_in_objects)
                    print(f"New file added to stage {file_path}. Path in objects: {path_in_objects}")
            else:  # target not in work dir. index exists. Remove from staging the file that removed from work dir
                if entry_from_index:
                    index_entries = _remove_entry_by_path(index_entries, file_path)
                    overwrite_index_file(index_entries)
                    print(f"File deletion staged {file_path}")
                else:
                    print("Nothing to add. File does not exist in working directory nor in staging")
        else:  # no index file yet
            if is_target_exist_in_work_dir:
                target_index_entry = build_index_entry(target_file)
                overwrite_index_file([target_index_entry])
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
