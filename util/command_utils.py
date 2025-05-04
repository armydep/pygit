def find_by_path(entries, path):
    for entry in entries:
        if entry.path == path:
            return entry
    return None
