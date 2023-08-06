import logging
from pathlib import Path
from typing import List

import giftmaster.skeleton


def myfun(x, check):
    for item in check:
        z = str(Path(item)).lower()
        msg = f"checking for {z} in {x}"
        # logging.debug(msg)
        if z in str(x):
            msg = f"found {z} in {x}"
            logging.debug(msg)
            return True
    return False


def get_files_to_sign(basedir: Path) -> List[str]:
    paths = set(list(Path(basedir).rglob("*")))

    # filter on only file types and substrings in paths
    dirs = set(filter(lambda _str: Path(_str).is_dir(), paths))
    symlinks = set(filter(lambda _str: Path(_str).is_symlink(), paths))
    paths_filtered = paths - dirs - symlinks

    ignore = set()

    extensions_to_ignore = [
        ".bat",
        ".bmp",
        ".cfg",
        ".envrc",
        ".git",
        ".gitignore",
        ".go",
        ".ico",
        ".ini",
        ".log",
        ".md",
        ".mod",
        ".py",
        ".pyc",
        ".pdf",
        ".png",
        ".sum",
        ".tmpl",
        ".tox",
        ".txt",
        ".venv",
        ".wixobj",
        ".wxl",
        ".wxs",
        ".xml",
        ".yml",
        ".venv",
        ".zip",
    ]

    ignore |= set(filter(lambda x: myfun(x, extensions_to_ignore), paths_filtered))
    paths_filtered -= ignore
    logging.debug(paths_filtered)
    return list(paths_filtered)


def sign_files(basedir: Path) -> None:
    paths_filtered = get_files_to_sign(basedir)

    extensions = set()
    for path in paths_filtered:
        extensions.add(path.suffix.lower())

    file_list = list(paths_filtered)
    signtool_candidates = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\signtool.exe"
    ]
    batch_size = 10
    dry_run = None
    giftmaster.skeleton.client(file_list, signtool_candidates, batch_size, dry_run)
