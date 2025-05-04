from registry import register
from repo import Repository
from util.command_utils import find_by_path
from util.file_util import FileUtil, IndexEntry
import os
import traceback


@register("add")
def add_command(args, staged):
    print("Im add command exec")
    repository = Repository()
    work_dir = repository.work_dir()
    print(f"working dir: {work_dir}")
    storage_dir = repository.storage_dir()
    storage_full_path = os.path.join(work_dir, storage_dir)

    if not FileUtil.is_dir_exist(storage_full_path):
        print("The work dir is not a git repository. missing .git directory")
        return

    if args[0] == ".":
        print("'add .' All untracked changes will be added")
        index_file = "index"
        storage_dir = repository.storage_dir()
        storage_full_path = os.path.join(work_dir, storage_dir)
        index_file_path = os.path.join(storage_full_path, index_file)
        index_entries = FileUtil.parse_index_file_lines(index_file_path)
        all_working_files = FileUtil.list_all_files_rec(work_dir, storage_dir)
        work_file_entries = FileUtil.transform_paths_to_entries(all_working_files)
        # for f in work_file_entries:
        #     print(f"Work dir entry: {f}")
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
            # f.path
            rel_path = f.path[len(work_dir) + 1 :]
            untracked_path_set.add(rel_path)

        for f in untracked_path_set:
            print(f"Untracked set entry: {f}")
            add_single_file(f)
    else:
        add_single_file(args[0])


def add_single_file(target_file) -> None:
    print("Im add single file command")
    try:
        repository = Repository()
        work_dir = repository.work_dir()
        print(f"working dir: {work_dir}")
        storage_dir = repository.storage_dir()
        storage_full_path = os.path.join(work_dir, storage_dir)
        file_path = os.path.join(work_dir, target_file)

        if not FileUtil.is_dir_exist(storage_full_path):
            print("The work dir is not a git repository. missing .git directory")
            return

        objects_dir = "objects"
        index_file = "index"
        index_file_path = os.path.join(storage_full_path, index_file)
        index_file_path = os.path.join(storage_full_path, index_file)
        index_entries = FileUtil.parse_index_file_lines(index_file_path)

        is_target_exist_in_work_dir = FileUtil.is_file_exist(file_path)

        index_entry = find_by_path(index_entries, file_path)
        if index_entry:
            print(
                "The file required to add to tracking is found in index (will be added/removed depend on modified or not in work_dir)"
            )
            if is_target_exist_in_work_dir:
                target_index_entry = FileUtil.build_index_entry(file_path)
                print(f"Target Index entry:{target_index_entry}")
                # todo: replace by target.equals to index
                if target_index_entry.sha1 == index_entry.sha1 and target_index_entry.size == index_entry.size:
                    print("The file is already staged and wasnt changed since that moment. No add required")
                else:
                    print("Exist in stage but modified. Replacing")
                    index_entry.size = target_index_entry.size
                    index_entry.sha1 = target_index_entry.sha1
                    index_entry.mod_time = target_index_entry.mod_time
                    FileUtil.update_index_file(index_file_path, index_entries)
                    path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)
                    FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
            else:
                print("The file was in index and now removed from the workd_dir. Removing from index")
                index_entries = _remove_entry_by_path(index_entries, file_path)
                FileUtil.update_index_file(index_file_path, index_entries)
                path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)
                os.remove(path_in_objects)

        else:
            if is_target_exist_in_work_dir:
                print("The file required to add to tracking is in work_dir and NOT found in index. Adding to index")
                target_index_entry = FileUtil.build_index_entry(file_path)
                index_entries.append(target_index_entry)
                FileUtil.update_index_file(index_file_path, index_entries)
                path_in_objects = os.path.join(storage_full_path, objects_dir, target_file)
                FileUtil.add_file_to_objects(file_path, os.path.dirname(path_in_objects))
            else:
                print("The target file is not in work_dir, NOR in index. Nothing to add")

    except Exception as e:
        print(f"add failed. {e}")
        traceback.print_exc()
        return -1


def _remove_entry_by_path(entries: list[IndexEntry], path: str) -> list[IndexEntry]:
    return [e for e in entries if e.path != path]
