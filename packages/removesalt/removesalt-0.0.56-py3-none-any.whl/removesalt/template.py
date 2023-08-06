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

    package = __name__.split(".")[0]
    TEMPLATES_PATH = pathlib.Path(
        pkg_resources.resource_filename(package, "templates/")
    )
    RESOURCES_PATH = pathlib.Path(
        pkg_resources.resource_filename(package, "resources/")
    )
    deploy.mkdir(exist_ok=True, parents=True)

    src = TEMPLATES_PATH / "cleanlogs.ps1"
    dst = deploy / src.name
    log.debug(f"cwd: {pathlib.Path.cwd()}")
    shutil.copy(src, dst)

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

    src = RESOURCES_PATH / "IRIS Decoder Placard.png"
    dst = work1 / src.name
    shutil.copy(src, dst)

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

    path = TEMPLATES_PATH / "encassist.ini"
    tpl_str = path.read_text()
    tpl = jinja2.Template(tpl_str)
    rendered = tpl.render(data=cfg)
    out_path = deploy / path.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    log.debug(f"creating {out_path}")
    out_path.write_text(rendered)

    path = TEMPLATES_PATH / "service.ps1"
    tpl_str = path.read_text()
    tpl = jinja2.Template(tpl_str)
    rendered = tpl.render(data=cfg)
    out_path = deploy / path.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)

    pdf = RESOURCES_PATH / "streambox_iris_quickstart.pdf"
    shutil.copy(pdf, work1 / pdf.name)
