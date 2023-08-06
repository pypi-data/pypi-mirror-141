import argparse
import logging
import os
import pathlib
import shutil

import hydra

log = logging.getLogger(__name__)


def setup(cfg):
    orig_cwd = pathlib.Path(hydra.utils.get_original_cwd()).resolve()
    bin_path = orig_cwd / cfg.bin_path
    work1 = orig_cwd / cfg.work1
    deploy = orig_cwd / cfg.deploy

    os.chdir(bin_path.resolve())

    deploy.mkdir(parents=True, exist_ok=True)
    work1.mkdir(parents=True, exist_ok=True)

    ver_file = deploy / "version.txt"
    ver_file.write_text(cfg.product_version)

    files = [
        "controlpanel.exe",
        "decoder.exe",
        "chromactivate.exe",
        "sb-hd-bmp.bmp",
        r"C:\ProgramData\chocolatey\lib\NSSM\tools\nssm.exe",
    ]

    for file in files:
        shutil.copy(file, deploy)

    files = [
        "curl.exe",
        "libeay32.dll",
        "libssl32.dll",
        "msvcr90.dll",
    ]
    curl = deploy / "curl"
    curl.mkdir(exist_ok=True, parents=True)
    for file in files:
        shutil.copy(file, curl)

    shutil.copy(cfg.iris_icon, work1 / cfg.iris_icon)


def clean(cfg):
    dirs = [pathlib.Path(cfg.work), pathlib.Path(cfg.deploy)]
    for _dir in dirs:
        if _dir.exists():
            shutil.rmtree(_dir)


def main(cfg):
    if cfg.cleanbuild:
        clean(cfg)
    setup(cfg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
