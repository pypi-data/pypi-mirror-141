import io
import logging
import os
import pathlib
import zipfile

import boto3
import botocore.exceptions
import hydra

log = logging.getLogger(__name__)


s3_client = boto3.client(
    "s3",
    region_name="us-west-2",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


def upload_my_file(bucket, folder, file_as_binary, file_name):
    file_as_binary = io.BytesIO(file_as_binary)
    key = folder + "/" + file_name
    try:
        s3_client.upload_fileobj(
            file_as_binary, bucket, key, ExtraArgs={"ACL": "public-read"}
        )
    except botocore.exceptions.ClientError as e:
        print(e)
        return False
    return True


def wrapper(cfg, bucket, folder, file_as_binary, file_name):
    if not cfg.stop_all_uploads:
        upload_my_file(bucket, folder, file_as_binary, file_name)


def main(cfg):
    logging.getLogger("botocore").setLevel(logging.WARNING)
    orig_cwd = pathlib.Path(hydra.utils.get_original_cwd()).resolve()

    # for key in logging.Logger.manager.loggerDict:
    #     print(key)

    version = cfg.product_version

    orig_cwd = pathlib.Path(hydra.utils.get_original_cwd()).resolve()
    work1 = orig_cwd / cfg.work1
    bundle = orig_cwd / cfg.bundle
    zip_ver = orig_cwd / cfg.zip

    ver_file = work1 / "version.txt"
    ver_file.write_text(version)

    os.chdir(bundle.parent)
    # win/0.0.1/streambox_iris_win_0.0.1.zip
    with zipfile.ZipFile(zip_ver.name, mode="w") as zf:
        zf.write(bundle.name)
    file_binary = open(zip_ver, "rb").read()
    os.chdir(orig_cwd)
    log.info(f"overwriting win/{version}/{zip_ver.name}")
    wrapper(cfg, "streambox-iris", f"win/{version}", file_binary, zip_ver.name)

    # win/0.0.1/version.txt
    log.info(f"overwriting win/{version}/{ver_file.name}")
    file_binary = open(ver_file, "rb").read()
    wrapper(cfg, "streambox-iris", f"win/{version}", file_binary, ver_file.name)

    # latest/win/streambox_iris_quickstart.pdf
    pdf = work1 / "streambox_iris_quickstart.pdf"
    file_binary = open(pdf, "rb").read()
    log.info(f"overwriting latest/win/{pdf.name}")
    wrapper(cfg, "streambox-iris", "latest/win", file_binary, pdf.name)

    if cfg.stop_all_uploads or not cfg.release:
        log.info(
            (
                "not updating win/latest because "
                "cfg.stop_all_uploads=true or cfg.release=false"
            )
        )
        return

    # overwrite latest folder below / release it

    # latest/win/streambox_iris_win.zip
    os.chdir(bundle.parent)
    zip = pathlib.Path(cfg.zip_no_ver)
    with zipfile.ZipFile(zip.name, mode="w") as zf:
        zf.write(bundle.name)
    file_binary = open(zip, "rb").read()
    log.info(f"overwriting latest/win/{zip.name} (because cfg.release=True)")
    wrapper(cfg, "streambox-iris", "latest/win", file_binary, zip.name)

    # latest/win/version.txt
    file_binary = open(ver_file, "rb").read()
    log.info(f"overwriting latest/win/{ver_file.name} (because cfg.release=True)")
    wrapper(cfg, "streambox-iris", "latest/win", file_binary, ver_file.name)
