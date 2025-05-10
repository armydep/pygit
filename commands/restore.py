from registry import register


@register("restore")
def restore_command(args, stgaded):
    repository = Repository()
    print(f"[restore] staged:{stgaded}")
    index_entries: list[IndexEntry] = get_index_entries(repository)
    prev_commit_index_path = get_head_commit_index_path(repository)
    if prev_commit_index_path:
        prev_index_entries = FileUtil.parse_index_file_lines(prev_commit_index_path)
        if compare_index_sets(index_entries, prev_index_entries):
            over_write_index_file(prev_index_entries)
            objects_path = get_objects_path(repository)
            FileUtil.clear_dir(objects_path)
            head_objects_path = get_head_objects_path(repository)
            FileUtil.copy_dir_contents(head_objects_path, objects_path)
            print(f"[restore] done")
        else:
            print(f"[restore] Nothing to restore. Head no changed")
    else:
        if index_entries:
            print(f"[restore] staged:{stgaded}")
            over_write_index_file(prev_index_entries, [])
            objects_path = get_objects_path(repository)
            FileUtil.clear_dir(objects_path)
        else:
            print(f"[restore] Nothing to restore. No head, no staging")
