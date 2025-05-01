import os
from typing import List
import shutil


class FileUtil:

    @staticmethod
    def is_dir_exist(path) -> bool:
        return 1

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
    def list_all_files(dir_path: str, exclude_name: str) -> List[str]:
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
    def list_dir_non_recursive_with_exclude(path: str, exc: str) -> list[str]:
        return [
            os.path.join(path, entry)
            for entry in os.listdir(path)
            if entry != exc
        ]
    
    @staticmethod
    def list_dir_non_recursive(path: str) -> list[str]:
        return [entry for entry in os.listdir(path)]
