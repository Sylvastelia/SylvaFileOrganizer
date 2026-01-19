#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

def get_file_type(file: Path) -> str:
    return file.suffix.lower()

def log(msg, gui_log=None):
    if gui_log:
        gui_log.insert(tk.END, msg + "\n")
        gui_log.see(tk.END)
    else:
        print(msg)

def start_gui(file_categories):
    root = tk.Tk()
    root.title("Sylva's File Organizer")
    root.geometry("600x450")

    path_var = tk.StringVar()
    misc_var = tk.BooleanVar(value=False)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)

    ttk.Label(root, text="Select Folder:").pack(pady=5)
    ttk.Entry(root, textvariable=path_var, width=60).pack(pady=5)
    ttk.Button(root, text="Browse", command=browse_folder).pack(pady=5)
    ttk.Checkbutton(
        root,
        text="Sort unknown file types into Misc",
        variable=misc_var
    ).pack(pady=5)

    text_area = scrolledtext.ScrolledText(
        root, width=60, height=15
    )
    text_area.pack(pady=5)

    ttk.Button(
        root,
        text="Start Sorting",
        command=lambda: start_sorting(
            directory=path_var.get(),
            misc_sort=misc_var.get(),
            gui_log=text_area,
            file_categories=file_categories
        )
    ).pack(pady=10)

    root.mainloop()

def start_sorting(directory, misc_sort=False, gui_log=None, file_categories=None):
    if not file_categories:
        log("No file categories provided.", gui_log)
        return

    path = Path(directory or Path.home() / "Downloads")

    if not path.exists():
        log(f"Error: {path} does not exist.", gui_log)
        if gui_log:
            messagebox.showerror("Invalid path", f"{path} does not exist.")
        return

    moved = 0

    for file in path.iterdir():
        if not file.is_file():
            continue

        ext = get_file_type(file)
        category = next(
            (cat for cat, exts in file_categories.items() if ext in exts),
            None
        )

        if not category and not misc_sort:
            continue

        dest_folder = path / (category or "Misc")
        dest_folder.mkdir(exist_ok=True)

        destination = dest_folder / file.name
        if destination.exists():
            destination = dest_folder / f"{file.stem}_copy{file.suffix}"

        shutil.move(str(file), str(destination))
        log(f"{file.name} → {dest_folder.name}", gui_log)
        moved += 1

    log(f"Sorting complete! {moved} files moved.", gui_log)
    if gui_log:
        messagebox.showinfo("Done!", f"Sorting complete! {moved} files moved.")