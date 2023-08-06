# by Kipling Crossing
import os
import shutil


def sync(source_dir: str, changed_dir: str):
    file_types = ["py"]
    suffixes = [".", "_"]
    files = [f for f in os.listdir(changed_dir) if f.split(".")[-1] in file_types]
    sub_dirs = [
        f
        for f in os.listdir(changed_dir)
        if os.path.isdir(os.path.join(changed_dir, f)) and f[0] not in suffixes
    ]
    for file in files:
        changed_path = os.path.join(changed_dir, file)
        source_path = os.path.join(source_dir, file)
        os.remove(source_path)
        shutil.copyfile(changed_path, source_path)

    for sub_dir in sub_dirs:
        change_sub_dir = os.path.join(changed_dir, sub_dir)
        source_sub_dir = os.path.join(source_dir, sub_dir)
        sync(source_sub_dir, change_sub_dir)
