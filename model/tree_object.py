class TreeObject:
    def __init__(self, tree_hash: str):
        self.tree_hash = tree_hash
        self.sha1 = "aaa"

    def __eq__(self, other):
        return isinstance(other, TreeObject) and self.tree_hash

    def __hash__(self):
        return hash((self.tree_hash))

    def __str__(self):
        return f"{self.tree_hash}|{self.sha1}"

    # @classmethod
    # def from_string(cls, lines: list[str]):
    #     blobs: list[str] = flatten_tree_object(lines)
    #     return cls("tree_hash")


"""
git cat-file -p 07fbb54a88b2d5297ebbd4609eb9f748bd838208

100644 blob 8baef1b4abc478178b004d62031cf7fe6db6f903	bbb.txt
040000 tree e183545695a5d1e4fdc4f3a9a9c78eca572a95c2	myp1
100644 blob 1a52584b7fb352fc19c3b1937cddc22015308c38	sec.txt
"""
