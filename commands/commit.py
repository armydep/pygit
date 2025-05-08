import hashlib
import time
from index_entry import IndexEntry
from model.tree_object import TreeObject
from repo import get_index_file_path, get_path_in_objects, get_storage_root, get_tree_object
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
    mode_ = 000000
    wrap = f"commit {size_} {mode_} {commit_object_content}"
    commit_hash = hashlib.sha1(wrap.encode("utf-8")).hexdigest()

    path_in_objects = get_path_in_objects(commit_hash)
    FileUtil.create_file_with_dir(path_in_objects, commit_object_content)


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
            # subTree = IndexTree(headDir)
            # self.sub_trees[headDir] = subTree
            subTree.propagate_build(strip_root_dir(path), entry)


def create_tree_object(index_entries: list[IndexEntry]) -> str:
    tree: IndexTree = buildIndexTree(index_entries)

    return tree.sha1


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
            # if not subTree:
            #     subTree = IndexTree(headDir)
            #     tree.sub_trees[headDir] = subTree
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
        
    
    # objects_dir = "objects"
    index_file = "index"
    index_file_path = os.path.join(storage_full_path, index_file)
    index_entries = FileUtil.parse_index_file_lines(index_file_path)

    active_branch_file = "active_branch"
    active_branch_file_path = os.path.join(storage_full_path, active_branch_file)
    active_branch = FileUtil.read_file_content(active_branch_file_path)
    print(f"Active branch: {active_branch}")

    branches_dir_name = "branches"
    head_file = "HEAD"
    active_branch_head_path = os.path.join(storage_full_path, branches_dir_name, active_branch, head_file)
    head = FileUtil.read_file_content(active_branch_head_path)
    print(f"Active branch head: {head}")

    branch_root = os.path.join(storage_full_path, branches_dir_name, active_branch)
    print(f"curr branch root:{branch_root}")

    if not index_entries and not head:
        print("Nothing to commit. No commits yet happen. Nothing staged and no prev commits(empty repo). (case-0)")
        return

    #
    # 1. no staging no commits                       -> 0 1 - nothing to commit
    # 2. there is a staging and there are no commits -> commit-0 2 / commit all as is first commit
    # 3. there is commit                             -> commit-2 / commit only if there is a diff / ??? nothing to commit / create new commit with empty repo space

    # no such case
    # 4. there is commit and there is a staging      -> commit-2 / commit only if there is a diff between staging and last commit
    #
    # if exist at least one commit
    # else
    # if index is different from last commit
    #
    # if index_entries:

    # No commits yet happen. First commit. Will be check if there are staged files by diff index against last commit
    if not head:
        print("Commit all. First commit. (case-1)")
        commit_name = str(time.time_ns())
        commit_path = os.path.join(branch_root, commit_name, "objects")
        os.makedirs(commit_path)
        FileUtil.overwrite_file(active_branch_head_path, commit_name)
        print(f"Commit created: {commit_path}")

        objects_dir = "objects"
        path_in_objects = os.path.join(storage_full_path, objects_dir)
        print(f"Copy objects from {path_in_objects} -> {commit_path}")
        FileUtil.copy_dir_contents(path_in_objects, commit_path)
        FileUtil.copy_to_directory(index_file_path, os.path.join(branch_root, commit_name))

        return

    # There were commits.
    # Now we should detect if there are staged files since last commit
    commit_index_path = os.path.join(branch_root, head, "index")
    print(f"There are prev commits. Lets diff. head commit file: {commit_index_path}")
    commit_index_entries = FileUtil.parse_index_file_lines(commit_index_path)

    if compare_index_sets(index_entries, commit_index_entries):
        print(f"There are staged changes. Commiting")

        commit_name = str(time.time_ns())
        commit_path = os.path.join(branch_root, commit_name, "objects")
        print(f"Creating a commit dir: {commit_path}")
        os.makedirs(commit_path)

        FileUtil.overwrite_file(active_branch_head_path, commit_name)
        # print(f"Commit created: {commit_path}")
        objects_dir = "objects"
        path_in_objects = os.path.join(storage_full_path, objects_dir)
        print(f"Copy objects from {path_in_objects} -> {commit_path}")
        FileUtil.copy_dir_contents(path_in_objects, commit_path)
        FileUtil.copy_to_directory(index_file_path, os.path.join(branch_root, commit_name))
        # add reference to parent commit
        # commit_index_path = os.path.join(branch_root, head, "index")
        commit_parent_path = os.path.join(branch_root, commit_name, "parent")
        print(f"Parent commit: {commit_parent_path}")
        FileUtil.overwrite_file(commit_parent_path, head)
    else:
        print(f"No staged changes since last commit, index - {commit_index_path}. Nothing to commit")

        

        def create_tree_object(index_entries: list[IndexEntry]) -> str:
    tree_obj_content = ""
    for ie in index_entries:
        if is_base_level_file(ie.path):
            mode_ = 000000
            type_ = "blob"
            name_ = ie.path
            hash_ = ie.sha1
            tree_obj_content += f"{mode_} {type_} {hash_}\t{name_}\n"
        else:
            mode_ = 000000
            type_ = "tree"
            name_ = strip_root_dir(ie.path)
            hash_ = create_subtree_rec(name_, ie.sha1)
            tree_obj_content += f"{mode_} {type_} {hash_}\t{name_}\n"

    size_ = len(tree_obj_content)
    mode_ = 000000

    wrap = f"tree {size_} {mode_} {tree_obj_content}"
    tree_hash = hashlib.sha1(wrap.encode("utf-8")).hexdigest()

    path_in_objects = get_path_in_objects(tree_hash)
    FileUtil.create_file_with_dir(path_in_objects, tree_obj_content)

    return tree_hash
"""
