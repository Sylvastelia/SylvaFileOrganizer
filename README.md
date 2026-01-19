# Sylva File Organizer

A small Python tool to organize files in a folder based on file extensions.

## Features
- GUI mode (double-click)
- CLI mode (run from terminal)
- User-defined file extensions category ()
- Optional sorting of unknown files into a `Misc` folder

## Usage

### GUI
Double-click the executable.

### CLI
```bash
SylvaFileOrganizer.exe <folder> --misc-sort
```
You can omit `--misc-sort` to prevent sorting unknown file extensions.

## Configuration

On first run, the program creates a `file_dictionary.json` file in:

- **Windows:** `%APPDATA%\SylvaFileOrganizer\file_dictionary.json`

You can edit this file to customize how files are categorized.
Restart the application after making changes.
