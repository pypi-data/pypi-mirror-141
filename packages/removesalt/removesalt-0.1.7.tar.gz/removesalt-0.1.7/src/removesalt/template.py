import logging
import pathlib
import shutil

import hydra
import jinja2
import pkg_resources

log = logging.getLogger(__name__)


def main(cfg):
    orig_cwd = pathlib.Path(hydra.utils.get_original_cwd()).resolve()
    deploy = orig_cwd / cfg.deploy
    work1 = orig_cwd / cfg.work1
    bin_path = orig_cwd / cfg.bin_path

    package = __name__.split(".")[0]
    TEMPLATES_PATH = pathlib.Path(
        pkg_resources.resource_filename(package, "templates/")
    )
    deploy.mkdir(exist_ok=True, parents=True)

    src = TEMPLATES_PATH / "product1.wxs"
    tpl_str = src.read_text()
    tpl = jinja2.Template(tpl_str)
    rendered = tpl.render(data=cfg)
    out_path = work1 / "product.wxs"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)

    src = TEMPLATES_PATH / "ClassicTheme.xml"
    tpl_str = src.read_text()
    tpl = jinja2.Template(tpl_str)
    rendered = tpl.render(data=cfg)
    out_path = work1 / src.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)

    src = TEMPLATES_PATH / "ClassicTheme.wxl"
    tpl_str = src.read_text()
    tpl = jinja2.Template(tpl_str)
    rendered = tpl.render(data=cfg)
    out_path = work1 / src.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)

    src = TEMPLATES_PATH / "bundle0.wxs"
    tpl_str = src.read_text()
    tpl = jinja2.Template(tpl_str)
    rendered = tpl.render(data=cfg)
    out_path = work1 / "bundle.wxs"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)
    log.debug(f"copied {src.resolve()} to {out_path.resolve()}")

    src = TEMPLATES_PATH / "custom_actions.wxs"
    dst = work1 / src.name
    dst.unlink(missing_ok=True)
    shutil.copy(src, dst)

    # work1: to be used to make installer
    resource = bin_path / "IRIS Decoder Placard.png"
    shutil.copy(resource, work1 / resource.name)

    resource = bin_path / "streambox_iris_quickstart.pdf"
    shutil.copy(resource, work1 / resource.name)

    # deploy: to be delployed
    resource = bin_path / "encassist.ini"
    shutil.copy(resource, deploy / resource.name)

    resource = bin_path / "service.ps1"
    shutil.copy(resource, deploy / resource.name)

    resource = bin_path / "cleanlogs.ps1"
    shutil.copy(resource, deploy / resource.name)
