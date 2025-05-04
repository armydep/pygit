import os
import shutil
import hashlib


class IndexEntry:
    def __init__(self, path: str, sha1: str, mod_time: int, size: int):
        self.path = path
        self.sha1 = sha1
        self.mod_time = mod_time
        self.size = size

    def __eq__(self, other):
        return isinstance(other, IndexEntry) and self.path == other.path and self.sha1 == other.sha1 and self.size == other.size

    def __hash__(self):
        return hash((self.path, self.sha1, self.size))

    def __str__(self):
        return f"{self.path}|{self.sha1}|{self.mod_time}|{self.size}"

    @classmethod
    def from_string(cls, line: str):
        path, sha1, mod_time_str, size_str = line.split("|")
        return cls(path, sha1, int(mod_time_str), int(size_str))


class FileUtil:

    @staticmethod
    def is_file_exist(file_path) -> bool:
        return os.path.isfile(file_path)

    @staticmethod
    def is_dir_exist(file_path) -> bool:
        return os.path.isdir(file_path)

    @staticmethod
    def create_dir_if_not_exist(dir_path) -> bool:
        os.makedirs(dir_path)
        # try:
        #     os.makedirs(dir_path)
        #     return 1
        # except FileExistsError:
        #     return 0

    @staticmethod
    def create_file_and_write(abs_path: str, content: str) -> bool:
        # parent_dir = os.path.dirname(abs_path)
        # os.makedirs(parent_dir, exist_ok=True)
        # Write content to the file
        with open(abs_path, "w") as f:
            f.write(content)
        # print(f"Written to {abs_path}")

    @staticmethod
    def list_all_files_rec(dir_path: str, exclude_name: str) -> list[str]:
        all_files = []
        for root, dirs, files in os.walk(dir_path):
            # Exclude directories with matching name (in-place modification of 'dirs')
            dirs[:] = [d for d in dirs if d != exclude_name]

            for file in files:
                if file == exclude_name:
                    continue  # Exclude specific file name
                full_path = os.path.join(root, file)
                all_files.append(full_path)

        return all_files

    @staticmethod
    def write_lines_to_file(file_path: str, lines: list[str]) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            for line in lines:
                f.write(line + "\n")

    @staticmethod
    def overwrite_file(file_path: str, str1: str) -> None:
        with open(file_path, "w") as f:
            f.write(str1 + "\n")

    @staticmethod
    def update_index_file(file_path: str, lines: list[IndexEntry]) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            for line in lines:
                f.write(str(line) + "\n")

    @staticmethod
    def add_file_to_objects(orig_file: str, target_dir: str) -> None:
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        shutil.copy2(orig_file, target_dir)

    @staticmethod
    def list_indexed_files(path) -> list[str]:
        with open(path, "r") as f:
            return [line.rstrip("\n") for line in f]

    @staticmethod
    def copy_to_directory(orig_file: str, target_dir: str) -> None:
        if not os.path.exists(orig_file):
            raise FileNotFoundError(f"Source path does not exist: {orig_file}")

        # os.makedirs(target_dir, exist_ok=True)  # Ensure target directory exists

        if os.path.isdir(orig_file):
            # Copy directory into target directory (recursively)
            dest = os.path.join(target_dir, os.path.basename(orig_file))
            shutil.copytree(orig_file, dest, dirs_exist_ok=True)
        else:
            # Copy single file into target directory
            shutil.copy2(orig_file, target_dir)

    @staticmethod
    def copy_dir_contents(d1: str, d2: str) -> None:
        # os.makedirs(d2, exist_ok=True)  # Ensure d2 exists
        for item in os.listdir(d1):
            src = os.path.join(d1, item)
            dst = os.path.join(d2, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

    @staticmethod
    def list_dir_non_recursive_with_exclude(path: str, exc: str) -> list[str]:
        return [os.path.join(path, entry) for entry in os.listdir(path) if entry != exc]

    @staticmethod
    def list_dir_non_recursive(path: str) -> list[str]:
        return [entry for entry in os.listdir(path)]

    @staticmethod
    def read_lines_from_file(file_path: str) -> list[str]:
        with open(file_path, "r") as f:
            return [line.rstrip("\n") for line in f]

    @staticmethod
    def read_file_content(file_path: str) -> str:
        with open(file_path, "r") as f:
            return "".join(line.strip() for line in f)

    @staticmethod
    def sha1_of_file(file_path: str) -> str:
        sha1 = hashlib.sha1()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):  # Read in 8 KB chunks
                sha1.update(chunk)
        return sha1.hexdigest()

    @staticmethod
    def parse_index_file_lines(file_path: str) -> list[IndexEntry]:
        ts_list = []
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # skip empty lines
                    # tokens = line.split("|")
                    ts_list.append(IndexEntry.from_string(line))
        return ts_list

    @staticmethod
    def build_index_entry(file_path: str) -> IndexEntry:
        path = file_path
        sha1 = FileUtil.sha1_of_file(file_path)
        file_stat = os.stat(file_path)
        mod_time = file_stat.st_mtime_ns
        size = file_stat.st_size
        return IndexEntry(path, sha1, mod_time, size)

    def transform_paths_to_entries(paths: list[str]) -> list[IndexEntry]:
        return list(map(FileUtil.build_index_entry, paths))

    @staticmethod
    def clear_dir(path: str) -> None:
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory")

        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
