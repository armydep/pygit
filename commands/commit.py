import hashlib
import os
import time
from index_entry import IndexEntry
from model.tree_object import TreeObject
from repo import create_head_commit_ref, get_index_file_path, get_path_in_objects, get_storage_root, get_tree_object
from util.file_util import FileUtil
from registry import register

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
    head_tree: TreeObject = get_tree_object()
    print(f"[commit] 4. tree_object: {head_tree}")
    if head_tree:
        print(f"Head tree exists")
    else:
        if not index_entries:
            print(f"No head tree. No commits yet and o staged files. Nothing to commit")
            return
        create_commit(index_entries, message)


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
    # _head_commit_hash_path(branch_name)}")
    # path =
    create_head_commit_ref(commit_hash)


"""
tree b2a6bc2d5b6175ca82adbce1eea8a0df4fd12b14
parent cf53306bf948ebc45fa114bc3cfbccae8a9cecc6
author Arkady <orkasha@gmail.com> 1746481341 +0300
committer Arkady <orkasha@gmail.com> 1746481341 +0300

swtich fixed
"""

"""
1. 
"""


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


"""
git cat-file -p 07fbb54a88b2d5297ebbd4609eb9f748bd838208

100644 blob 8baef1b4abc478178b004d62031cf7fe6db6f903	bbb.txt
040000 tree e183545695a5d1e4fdc4f3a9a9c78eca572a95c2	myp1
100644 blob 1a52584b7fb352fc19c3b1937cddc22015308c38	sec.txt
"""


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
