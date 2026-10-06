import os
import shutil
import json
import logging
import argparse

def main():
    sort_files()

def sort_files():
    args = parse_args()
    setup_logging()
    rules = load_rules()

    src_folder = args.src
    items = os.listdir(src_folder)

    for item in items:
        item_full_path = get_item_full_path(src_folder, item)

        if not is_file(item_full_path):
            continue

        item_folder = get_item_folder(rules, src_folder, item)

        if is_duplicate(item, item_folder):
            continue

        move_file_to_folder(item_full_path, item_folder)
        log_move(item, item_folder)

# settings

def setup_logging():
    logging.basicConfig(
        filename="sort.log",
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
    )

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="Source folder")
    return parser.parse_args()

def load_rules():
    path = os.path.join(os.path.dirname(__file__), "rules.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# getter

def get_item_full_path(src_folder, item):
    return os.path.join(src_folder, item)

# boolean

def is_file(item_full_path):
    return os.path.isfile(item_full_path)

def is_duplicate(item, item_folder):
    if os.path.exists(os.path.join(item_folder, item)):
        return True
    return False

# folder

def get_item_folder(rules, src_folder, file):
    folder_name = get_target_folder(rules, file)
    path = os.path.join(src_folder, folder_name)
    if not os.path.isdir(path):
        path = make_folder(src_folder, folder_name)
    return path

def get_target_folder(rules, file):
    ext = "." + file.split(".")[-1].lower()
    return rules.get(ext, "Other")

def make_folder(src_folder, folder_name):
    path = os.path.join(src_folder, folder_name)
    os.makedirs(path, exist_ok=True)
    return path

# move

def move_file_to_folder(item_full_path, item_folder):
    shutil.move(item_full_path, item_folder)

# log
def log_move(item, item_folder):
    logging.info(f"{item} -> {item_folder}")


if __name__ == "__main__":
    main()