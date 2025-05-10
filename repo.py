import os
from pathlib import Path

from index_entry import IndexEntry
from model.commit_object import CommitObject
from util.file_util import FileUtil


def get_storage_root() -> str:
    return os.path.join(get_work_dir(), storage_dir())


def get_index_file_path() -> str:
    return os.path.join(get_storage_root(), index())


def get_refs_heads_path() -> str:
    return os.path.join(get_storage_root(), refs(), heads())


def get_objects_path() -> str:
    return os.path.join(get_storage_root(), objects())


def get_head_file_path() -> str:
    return os.path.join(get_storage_root(), head())


def get_work_dir() -> str:
    return os.getcwd()


def build_default_branch_ref() -> str:
    return build_branch_ref(default_branch())


def build_branch_ref(branch: str) -> str:
    return "ref: " + os.path.join(refs(), heads(), branch)


def convert_file_to_work_dir_path(file: str) -> str:
    return os.path.join(get_work_dir(), file)


def get_path_in_objects(sha1: str) -> str:
    return os.path.join(get_storage_root(), objects(), sha1[0:2], sha1[2:])


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


def get_active_branch_name() -> str:
    active_branch_ref_content = get_active_branch_ref_content()
    return _extract_branch_name(active_branch_ref_content)


def create_head_commit_ref(commit_hash) -> None:
    branch_name = get_active_branch_name()
    create_head_commit_ref_for_branch(commit_hash, branch_name)


def get_active_branch_ref_content() -> str:
    return FileUtil.read_file_content(get_head_file_path())


def update_head_ref_to_branch(branch_ref) -> str:
    FileUtil.overwrite_file(get_head_file_path(), branch_ref)


def get_head_hash() -> str:
    return FileUtil.read_file_content(_head_commit_hash_path(get_active_branch_name()))


def create_head_commit_ref_for_branch(commit_hash: str, branch_name: str) -> None:
    path = os.path.join(get_refs_heads_path(), branch_name)
    print(f"Branch head create in: {path}. {commit_hash}")
    FileUtil.create_file_with_dir(path, commit_hash + "\n")


def _extract_branch_name(head_content) -> str:
    if head_content.startswith("ref: refs/heads/"):
        branch = head_content.split("refs/heads/")[1]
        return branch
    else:
        return None


def _head_commit_hash_path(branch) -> str:
    return os.path.join(get_refs_heads_path(), branch)


def list_branches() -> list[str]:
    branches_path = os.path.join(get_refs_heads_path())
    return [f.name for f in Path(branches_path).iterdir() if f.is_file()]


def get_active_branch_head_flat_tree_object() -> list[dict[str, str]]:
    branch_name = get_active_branch_name()
    return get_head_flat_tree_object_by_branch(branch_name)


def get_head_flat_tree_object_by_branch(branch_name: str) -> list[dict[str, str]]:
    if not FileUtil.is_file_exist(_head_commit_hash_path(branch_name)):
        return None

    head_commit_hash = FileUtil.read_file_content(_head_commit_hash_path(branch_name))
    commit_object_path = get_path_in_objects(head_commit_hash)
    commit_object_content_lines = FileUtil.read_lines_from_file(commit_object_path)
    commit_object: CommitObject = CommitObject.from_string(commit_object_content_lines)
    commit_tree_hash = commit_object.tree_hash
    tree_object: list[dict[str, str]] = flatten_tree_object_rec(commit_tree_hash)
    return tree_object


def flatten_tree_object_rec(tree_hash: str, dirname: str = "") -> list[dict[str, str]]:
    flat_blobs: list[dict[str, str]] = []
    tree_object_base: list[dict[str, str]] = tree_object_by_hash(tree_hash)
    if not tree_object_base:
        raise Exception(f"Tree not found by hash! {tree_hash}")
    for en in tree_object_base:
        if en["type"] == "blob":
            en["name"] = os.path.join(dirname, en["name"])
            flat_blobs.append(en)
        elif en["type"] == "tree":
            sub_dir_flat = flatten_tree_object_rec(en["hash"], os.path.join(dirname, en["name"]))
            flat_blobs.extend(sub_dir_flat)
        else:
            raise Exception(f"Tree object parsing error. Unknown type: {en["type"]} .{tree_hash}")

    return flat_blobs


def tree_object_by_hash(commit_tree_hash: str) -> list[dict[str, str]]:
    # print(f"Tree hash: {commit_tree_hash}")
    tree_object_path = get_path_in_objects(commit_tree_hash)
    # print(f"Tree object path: {tree_object_path}")
    tree_object_content = FileUtil.read_lines_from_file(tree_object_path)

    base_blobs: list[dict[str, str]] = []

    for line in tree_object_content:
        mode, type_, hash_, name = line.split(maxsplit=3)
        base_blobs.append({"mode": mode, "type": type_, "hash": hash_, "name": name})

    return base_blobs


def get_all_work_files() -> list[IndexEntry]:
    all_working_files = FileUtil.list_all_files_rec(get_work_dir(), storage_dir())
    return transform_paths_to_entries(all_working_files)


def get_index_entries() -> list[IndexEntry]:
    if not FileUtil.is_file_exist(get_index_file_path()):
        return []
    return FileUtil.parse_index_file_lines(get_index_file_path())


def build_index_entry(abs_path: str) -> IndexEntry:
    tail = abs_path.removeprefix(get_work_dir())
    rel_path = tail.lstrip("/")
    sha1 = FileUtil.sha1_of_file(abs_path)
    file_stat = os.stat(abs_path)
    mod_time = file_stat.st_mtime_ns
    size = file_stat.st_size
    stage_num = 0
    return IndexEntry(rel_path, sha1, mod_time, size, stage_num)


def transform_paths_to_entries(paths: list[str]) -> list[IndexEntry]:
    return list(map(build_index_entry, paths))


# def convert_flat_tree_to_index(flat_head_tree: list[dict[str, str]]) -> list[IndexEntry]:
#     index = []
#     for blob in flat_head_tree:
#         abs_path = get_path_in_objects(blob.get("hash"))
#         entry: IndexEntry = build_index_entry(abs_path)
#         index.append(entry)


#  build_index_entry(abs_path: str) -> IndexEntry:
# path
# sha1
# mod_time
# size,
# stage_num


def overwrite_index_file(index_entries: list[IndexEntry]) -> None:
    FileUtil.update_index_file(get_index_file_path(), index_entries)


def copy_object_to_work_dir(name: str, hash: str) -> None:
    src_ = get_path_in_objects(hash)
    dest_path = os.path.join(get_work_dir(), name)
    FileUtil.copy_file(src_, dest_path)
    return dest_path


def delete_work_dir_file(rel_path: str) -> None:
    FileUtil.delete_file(os.path.join(get_work_dir(), rel_path))
