class IndexEntry:
    def __init__(self, path: str, sha1: str, mod_time: int, size: int, stage_num: int):
        self.path = path
        self.sha1 = sha1
        self.mod_time = mod_time
        self.size = size
        self.stage_num = stage_num

    def __eq__(self, other):
        return isinstance(other, IndexEntry) and self.path == other.path and self.sha1 == other.sha1 and self.size == other.size

    def __hash__(self):
        return hash((self.path, self.sha1, self.size))

    def __str__(self):
        return f"{self.path}|{self.sha1}|{self.mod_time}|{self.size}|{self.stage_num}"

    @classmethod
    def from_string(cls, line: str):
        path, sha1, mod_time_str, size_str, stage_num_str = line.split("|")
        return cls(path, sha1, int(mod_time_str), int(size_str), int(stage_num_str))
