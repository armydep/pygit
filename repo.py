import os

from model.commit_object import CommitObject
from model.tree_object import TreeObject
from util.file_util import FileUtil


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
    return os.path.join("/home/duser/projects/git-pygit/work_dir")


def get_default_branch_ref() -> str:
    return "ref: " + os.path.join(refs(), heads(), default_branch())


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


def create_head_commit_ref(commit_hash) -> None:
    head_content = FileUtil.read_file_content(get_head_path())
    branch_name = _extract_branch_name(head_content)
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


def get_tree_object() -> TreeObject:
    print("tree entries")
    # 1
    head_content = FileUtil.read_file_content(get_head_path())
    print(f"Head content: {head_content}")
    # 2
    branch_name = _extract_branch_name(head_content)
    print(f"Branch name: {branch_name}")
    # 3
    if not FileUtil.is_file_exist(_head_commit_hash_path(branch_name)):
        print(f"No commits yet on branch. No head commit. ref path: {_head_commit_hash_path(branch_name)}")
        return None

    head_commit_hash = FileUtil.read_file_content(_head_commit_hash_path(branch_name))
    print(f"Head commit hash: {head_commit_hash}. ref path:{_head_commit_hash_path(branch_name)}")

    commit_object_path = get_path_in_objects(head_commit_hash)
    print(f"Commit object path: {commit_object_path}")
    commit_object_content_lines = FileUtil.read_lines_from_file(commit_object_path)
    commit_object: CommitObject = CommitObject.from_string(commit_object_content_lines)
    commit_tree_hash = commit_object.tree_hash
    print(f"Tree hash: {commit_tree_hash}")

    # tree_object_path = get_path_in_objects(commit_tree_hash)
    # print(f"Tree object path: {tree_object_path}")
    # tree_object_content = FileUtil.read_lines_from_file(tree_object_path)
    # print(f"Tree object content: {tree_object_content}")
    # tree_object: TreeObject = TreeObject.from_string(tree_object_content)
    tree_object: list[dict[str, str]] = flatten_tree_object_rec(commit_tree_hash)
    print("Tree flat blobs list built")
    for blob in tree_object:
        print(f"\t{blob}")
    """
    1. <head> <- read content of file(HEAD)
    2. <branch name> <- content of file(HEAD)
    3. if not file exist (branch name)
            ..
     <head commit hash> <- read content of (refs/heads/<branch name>)        
    5. commit content < - read content (objects / <head commit hash>) 
    6. tree hash <- parse (commit object)
    7. tree object <- read content (tree hash)
    8. tree entries <- parse (tree object)       
    """

    # return None


def flatten_tree_object_rec(tree_hash: str, dirname: str = "") -> list[dict[str, str]]:
    flat_blobs: list[dict[str, str]] = []
    tree_object_base: list[dict[str, str]] = tree_object_by_hash(tree_hash)
    if not tree_object_base:
        raise Exception(f"Tree not found by hash! {tree_hash}")
    for en in tree_object_base:
        if en["type"] == "blob":
            en["name"] = en["name"]  # os.path.join(dirname, en["name"])
            flat_blobs.append(en)
        elif en["type"] == "tree":
            sub_dir_flat = flatten_tree_object_rec(en["hash"], en["name"])  # os.path.join(dirname, en["name"]))
            flat_blobs.extend(sub_dir_flat)
        else:
            raise Exception(f"Tree object parsing error. Unknown type: {en["type"]} .{tree_hash}")

    return flat_blobs


def tree_object_by_hash(commit_tree_hash: str) -> list[dict[str, str]]:
    print(f"Tree hash: {commit_tree_hash}")
    tree_object_path = get_path_in_objects(commit_tree_hash)
    print(f"Tree object path: {tree_object_path}")
    tree_object_content = FileUtil.read_lines_from_file(tree_object_path)

    base_blobs: list[dict[str, str]] = []

    for line in tree_object_content:
        mode, type_, hash_, name = line.split(maxsplit=3)
        base_blobs.append({"mode": mode, "type": type_, "hash": hash_, "name": name})

    return base_blobs
