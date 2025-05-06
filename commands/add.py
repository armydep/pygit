import os
from registry import register
from repo import convert_file_to_work_dir_path, get_index_file_path, get_storage_root
from util.command_utils import find_by_path
from util.file_util import FileUtil, IndexEntry
import traceback


# @register("add")
# def add_command(args, staged):
#     print("Im add command exec")
#     repository = Repository()
#     storage_full_path = os.path.join(repository.work_dir(), repository.storage_dir())
#     if not FileUtil.is_dir_exist(storage_full_path):
#         print("The work dir is not a git repository. missing .git directory")
#         return

#     if args[0] == ".":
#         print("'add .' All untracked changes will be added")
#         storage_full_path = os.path.join(repository.work_dir(), repository.storage_dir())
#         index_file_path = os.path.join(storage_full_path, repository.index())
#         index_entries = FileUtil.parse_index_file_lines(index_file_path)
#         all_working_files = FileUtil.list_all_files_rec(repository.work_dir(), repository.storage_dir())
#         work_file_entries = FileUtil.transform_paths_to_entries(all_working_files)
#         untracked_set = set()
#         for ie in index_entries:
#             if ie not in work_file_entries:
#                 untracked_set.add(ie)
#         for wfe in work_file_entries:
#             if wfe not in index_entries:
#                 untracked_set.add(wfe)
#         untracked_path_set = set()
#         # abs_path = "/tmp/pygit/repo_work_dir_root/"
#         for f in untracked_set:
#             rel_path = f.path[len(repository.work_dir()) + 1 :]
#             untracked_path_set.add(rel_path)

#         for f in untracked_path_set:
#             print(f"Untracked set entry: {f}")
#             add_single_file(f)
#     else:
#         add_single_file(args[0])


@register("add")
def add_single_file(args, staged) -> None:
    try:
        print(f"add single file: {args[0]}")
        target_file = convert_file_to_work_dir_path(args[0])
        storage_full_path = get_storage_root()
        if not FileUtil.is_dir_exist(storage_full_path):
            print("The work dir is not a git repository. missing .git directory")
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
                target_index_entry = FileUtil.build_index_entry(target_file, args[0])
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
                        print(f"Target file modified. Updated in stage: {args[0]}")
                else:  # file not in staging. exists in work dir. add to staging
                    index_entries.append(target_index_entry)
                    FileUtil.update_index_file(index_file_path, index_entries)
                    print(f"New file added to stage {args[0]}")
            else:  # target not in work dir. index exists. Remove from staging the file that removed from work dir
                if entry_from_index:
                    index_entries = _remove_entry_by_path(index_entries, args[0])
                    FileUtil.update_index_file(index_file_path, index_entries)
                    print(f"File deletion staged {args[0]}")
                else:
                    print("Nothing to add. File does not exist in working directory nor in staging")
        else:  # no index file yet
            if is_target_exist_in_work_dir:
                target_index_entry = FileUtil.build_index_entry(target_file, args[0])
                FileUtil.update_index_file(index_file_path, [target_index_entry])
                print(f"Adding new index entry: {target_index_entry}")
            else:
                print("Nothing to add. File does not exist in working directory nor in index")
    except Exception as e:
        print(f"add failed. {e}")
        traceback.print_exc()
        return -1


def _remove_entry_by_path(entries: list[IndexEntry], path: str) -> list[IndexEntry]:
    return [e for e in entries if e.path != path]


# index_entries = FileUtil.parse_index_file_lines(index_file_path)
# index_entry = find_by_path(index_entries, file_path)
# if index_entry:
#     print("The file found in index (will be added/removed depend on modified or not in work_dir)")
#     if is_target_exist_in_work_dir:
#         target_index_entry = FileUtil.build_index_entry(file_path)
#         print(f"Target Index entry:{target_index_entry}")
#         if target_index_entry == index_entry:
#             print("The file is already staged and wasnt changed since that moment. No add required")
#         else:
#             print("Exist in stage but modified. Replacing")
#             index_entry.size = target_index_entry.size
#             index_entry.sha1 = target_index_entry.sha1
#             index_entry.mod_time = target_index_entry.mod_time
#             FileUtil.update_index_file(index_file_path, index_entries)
#             path_in_objects = os.path.join(storage_full_path, repository.objects(), target_file)
#             FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
#     else:
#         print("The file was in index and now removed from the workd_dir. Removing from index")
#         index_entries = _remove_entry_by_path(index_entries, file_path)
#         FileUtil.update_index_file(index_file_path, index_entries)
#         path_in_objects = os.path.join(storage_full_path, repository.objects(), target_file)
#         os.remove(path_in_objects)
# # the file not in staged area
# else:
#     if is_target_exist_in_work_dir:
#         print("The file required to add to tracking is in work_dir and NOT found in index. Adding to index")
#         target_index_entry = FileUtil.build_index_entry(file_path)
#         index_entries.append(target_index_entry)
#         FileUtil.update_index_file(index_file_path, index_entries)
#         path_in_objects = os.path.join(storage_full_path, repository.objects(), target_file)
#         FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
#     else:
#         print("The target file is not in work_dir, NOR in index. Nothing to add")
