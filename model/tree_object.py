class TreeObject:
    def __init__(self, tree_hash: str):
        self.tree_hash = tree_hash
        self.sha1 = "aaa"

    # def __eq__(self, other):
    #     return isinstance(other, TreeObject) and self.tree_hash

    # def __hash__(self):
    #     return hash((self.tree_hash))

    def __str__(self):
        return f"{self.tree_hash}|{self.sha1}"


