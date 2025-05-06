import os


def get_storage_root() -> str:
    return os.path.join(get_work_dir(), storage_dir())


def get_index_file_path() -> str:
    return os.path.join(get_storage_root(), index())


def get_refs_heads_path() -> str:
    return os.path.join(get_storage_root(), refs(), heads())


def get_objects_path() -> str:
    return os.path.join(get_storage_root(), objects())


def get_head_path() -> str:
    return os.path.join(get_storage_root(), head())


def get_work_dir() -> str:
    return os.path.join("/tmp", "pygit", "work_dir")


def get_default_branch_ref() -> str:
    return "ref: " + os.path.join(refs(), heads(), default_branch())


def convert_file_to_work_dir_path(file: str) -> str:
    return os.path.join(get_work_dir(), file)


def head() -> str:
    return "HEAD"


def refs() -> str:
    return "refs"


def heads() -> str:
    return "heads"


def default_branch() -> str:
    return "main"


def index() -> str:
    return "index"


def storage_dir() -> str:
    return ".pygit"


def objects() -> str:
    return "objects"
