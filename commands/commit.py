import hashlib
import os
import time
from index_entry import IndexEntry
from repo import (
    create_head_commit_ref,
    get_active_branch_head_flat_tree_object,
    get_index_file_path,
    get_path_in_objects,
    get_storage_root,
)
from util.file_util import FileUtil
from registry import register


# No commits yet on branch. No head commit.
# ref path: /home/duser/projects/git-pygit/work_dir/.pygit/refs/heads/main
# print(f"No commits yet on branch. No head commit. ref path: {_head_commit_hash_path(branch_name)}")
@register("commit")
def commit_command(args, staged):
    message = "my message com!"
    print("[commit] 1 Validation: " + "_".join(args))
    storage_full_path = get_storage_root()
    if not FileUtil.is_dir_exist(storage_full_path):
        print("The work dir is not a git repository. missing .git directory")
        return

    index_file_path = get_index_file_path()
    print(f"[commit] 2 index path: {index_file_path}")
    if not FileUtil.is_file_exist(index_file_path):
        print("No index file. Add files to stage. Nothing to commit")
        return
    print("[commit] 3")
    index_entries = FileUtil.parse_index_file_lines(index_file_path)
    print(f"[commit] 4. index_entries: {index_entries}")
    flat_head_tree: list[dict[str, str]] = get_active_branch_head_flat_tree_object()
    print(f"[commit] 4. tree_object: {flat_head_tree}")
    if flat_head_tree:
        print(f"[commit] 5. Head tree exists")
        if head_equals_to_index(flat_head_tree, index_entries):
            print(f"[commit] 6. Head tree equals to Index. Nothing to commit")
            return
        create_commit(index_entries, message)
    else:
        if not index_entries:
            print(f"[commit] 5. No head tree. No commits yet and o staged files. Nothing to commit")
            return
        create_commit(index_entries, message)


# should be compared by two trees. convert index to tree
def head_equals_to_index(flat_tree: list[dict[str, str]], index_entries: list[IndexEntry]) -> bool:
    if len(flat_tree) != len(index_entries):
        return False
    for entry in index_entries:
        if not (index_tree_found_in_flat_tree_object(entry, flat_tree)):
            return False
    return True


# should be compared by file mode as well.
def index_tree_found_in_flat_tree_object(entry: IndexEntry, flat_tree: list[dict[str, str]]) -> bool:
    return any(blob.get("name") == entry.path and blob.get("hash") == entry.sha1 for blob in flat_tree)


def create_commit(index_entries: list[IndexEntry], message: str, parent: str = "") -> None:
    tree_hash = create_tree_object(index_entries)
    if parent:
        parent = f"parent {parent}\n"
    timestamp = str(time.time_ns())
    author_line = f"author Auth <pygit@pygit.com> {timestamp}"
    committer_line = f"commiter Cm <pygit@pygit.com> {timestamp}"
    message_line = f"\n{message} - {timestamp}"
    commit_object_content = f"tree {tree_hash}\n{parent}{author_line}\n{committer_line}\n{message_line}\n"

    size_ = len(commit_object_content)
    mode_ = "000000"
    wrap = f"commit {size_} {mode_} {commit_object_content}"
    commit_hash = hashlib.sha1(wrap.encode("utf-8")).hexdigest()

    path_in_objects = get_path_in_objects(commit_hash)
    FileUtil.create_file_with_dir(path_in_objects, commit_object_content)
    create_head_commit_ref(commit_hash)
    print(f"Commit created: {commit_hash}")


class IndexTree:
    def __init__(self, root: str):
        self.root = root
        self.sha1 = ""
        self.blobs: list[IndexEntry] = []
        self.sub_trees: dict[str, IndexTree] = {}

    def propagate_build(self, path: str, entry: IndexEntry) -> None:
        if is_base_level_file(path):
            self.blobs.append(entry)
        else:
            headDir = get_root_dir(path)
            subTree = self.sub_trees.setdefault(headDir, IndexTree(headDir))
            subTree.propagate_build(strip_root_dir(path), entry)

    def generate_hash_rec(self) -> str:
        tree_object_content = ""
        for key, value in self.sub_trees.items():
            sub_tree_hash = value.generate_hash_rec()
            mode_ = "000000"
            line = f"{mode_} tree {sub_tree_hash}\t{value.root}\n"
            tree_object_content += line

        for blob in self.blobs:
            mode_ = "000000"
            file_name = os.path.basename(blob.path)
            line = f"{mode_} blob {blob.sha1}\t{file_name}\n"
            tree_object_content += line

        size_ = len(tree_object_content)
        mode_ = "000000"
        wrap = f"tree {size_} {mode_} {tree_object_content}"
        self.sha1 = hashlib.sha1(wrap.encode("utf-8")).hexdigest()

        path_in_objects = get_path_in_objects(self.sha1)
        FileUtil.create_file_with_dir(path_in_objects, tree_object_content)
        return self.sha1


def create_tree_object(index_entries: list[IndexEntry]) -> str:
    tree: IndexTree = buildIndexTree(index_entries)
    hash = tree.generate_hash_rec()
    return hash


def strip_root_dir(path: str) -> str:
    parts = path.split("/", 1)
    return parts[1] if len(parts) > 1 else ""


def get_root_dir(path: str) -> str:
    parts = path.split("/", 1)
    return parts[0]


def is_base_level_file(path: str) -> bool:
    return "/" not in path


def buildIndexTree(index_entries: list[IndexEntry]) -> IndexTree:
    tree = IndexTree("")
    for entry in index_entries:
        if is_base_level_file(entry.path):
            tree.blobs.append(entry)
        else:
            headDir = get_root_dir(entry.path)
            subTree: IndexTree = tree.sub_trees.setdefault(headDir, IndexTree(headDir))
            subTree.propagate_build(strip_root_dir(entry.path), entry)
    return tree


"""
    1. check if there something to commit

    if not 
        print nothing to commit
        return    

    1. take index entries

    2. take head commit 
        if there is a head commit
    
        take tree object

    3. blobs set bs = {}    
    4. if head commit exists    
    5.      compare commit tree object vs index entries
    6.       fill blobs_set
    5. else
    7.       fill blobs_set
    8. create tree object (blobs_set)
    9. create commit object (tree object)
        
 """
"""
    1. check if there something to commit

    if not 
        print nothing to commit
        return    

    1. take index entries

    2. take head commit 
        if there is a head commit
    
        take tree object

    3. blobs set bs = {}    
    4. if head commit exists    
    5.      compare commit tree object vs index entries
    6.       fill blobs_set
    5. else
    7.       fill blobs_set
    8. create tree object (blobs_set)
    9. create commit object (tree object)
"""
