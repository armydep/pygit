class CommitObject:
    def __init__(self, commit_info: dict[str, str]):
        self.object = commit_info
        self.tree_hash = commit_info['tree']

    # def __eq__(self, other):
    #     return isinstance(other, CommitObject) and self.object

    # def __hash__(self):
    #     return hash((self.tree_hash))

    def __str__(self):
        return f"{self.object}"

    def __repr__(self):
        return f"CommitObject({self.object})"

    @classmethod
    def from_string(cls, lines: list[str]):
        # lines = content.splitlines()

        commit_info = {}
        message_lines = []
        in_message = False

        for line in lines:
            if line.strip() == "" and not in_message:
                in_message = True
                continue
            if in_message:
                message_lines.append(line)
            else:
                key, value = line.split(" ", 1)
                commit_info[key] = value

        commit_info["message"] = "\n".join(message_lines)

        return cls(commit_info)

    # def get_tree_hash(self) -> str:
    #     return self.tree_hash


"""
git cat-file -p c78d5cd435a97cf00939c453a500c3b3712b7616

tree b2a6bc2d5b6175ca82adbce1eea8a0df4fd12b14
parent cf53306bf948ebc45fa114bc3cfbccae8a9cecc6
author Arkady <orkasha@gmail.com> 1746481341 +0300
committer Arkady <orkasha@gmail.com> 1746481341 +0300

swtich fixed
"""
