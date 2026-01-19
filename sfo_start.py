import sys
import argparse
import json
import os
import shutil
from sfo import start_gui, start_sorting


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_user_config_path():
    appdata = os.getenv("APPDATA")
    config_dir = os.path.join(appdata, "SylvaFileOrganizer")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "file_dictionary.json")

default_path = resource_path("file_dictionary.json")
user_path = get_user_config_path()

if os.path.exists(user_path):
    path_to_use = user_path
else:
    shutil.copy(default_path, user_path)
    path_to_use = user_path

with open(path_to_use, "r", encoding="utf-8") as f:
    file_categories = json.load(f)

def hide_console():
    if os.name != "nt":
        return
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

def start_cli():
    parser = argparse.ArgumentParser(description="Sylva's File Organizer CLI")
    parser.add_argument("directory", help="Folder to organize")
    parser.add_argument("--misc-sort", action="store_true", help="Sort unknown file types into Misc")
    args = parser.parse_args()

    start_sorting(
        directory=args.directory,
        misc_sort=args.misc_sort,
        gui_log=None,
        file_categories=file_categories
    )

if len(sys.argv) > 1 and sys.argv[1] != "--help":
    start_cli()
else:
    hide_console()
    start_gui(file_categories)