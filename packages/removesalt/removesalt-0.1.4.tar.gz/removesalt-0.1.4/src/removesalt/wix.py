import logging
import os
import pathlib
import platform
import shlex
import subprocess
import sys

import hydra

import removesalt.sign

log = logging.getLogger(__name__)


def run(cmd):

    log.debug(shlex.join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = proc.communicate()
    return_code = proc.poll()
    out = out.decode(sys.stdin.encoding)
    err = err.decode(sys.stdin.encoding)
    log.debug(out)

    ex = subprocess.CalledProcessError(return_code, cmd=shlex.join(cmd), output=out)
    ex.stdout, ex.stderr = out, err

    """
    error LGHT0204 : ICE57: Component 'IrisControlPanelShortcutComponent'
    has both per-user data and a keypath that can be either per-user or
    per-machine.
    204
    """

    if proc.returncode not in [0, 204]:
        raise ex


def main(cfg):
    orig_cwd = pathlib.Path(hydra.utils.get_original_cwd()).resolve()
    work1 = orig_cwd / cfg.work1
    deploy = orig_cwd / cfg.deploy

    actions = work1 / "custom_actions.wxs"
    bundle = work1 / "bundle.exe"
    components1 = work1 / "components1.wxs"
    engine = work1 / "engine.exe"
    localization_file = work1 / "ClassicTheme.wxl"
    msi = work1 / "streambox_iris.msi"
    product = work1 / "product.wxs"
    theme_file = work1 / "ClassicTheme.xml"

    cmd_heat = [
        "heat",
        "dir",
        str(deploy),
        "-out",
        str(components1),
        f"-dVersion={cfg.product_version}",
        "-cg",
        "ComponentGroupIris",
        "-dr",
        "IRISROOTDIRECTORY",
        "-var",
        "var.SourceFilesDir",
        "-ag",
        "-g1",
        "-srd",
        "-suid",
        "-sreg",
        "-nologo",
        "-arch",
        "x64",
    ]

    cmd_candle1 = [
        "candle",
        "-out",
        str(actions.with_suffix(".wixobj")),
        str(actions),
        "-ext",
        "WixUtilExtension",
        "-nologo",
        "-arch",
        "x64",
    ]

    cmd_candle2 = [
        "candle",
        "-out",
        str(components1.with_suffix(".wixobj")),
        str(components1),
        f"-dSourceFilesDir={str(deploy)}",
        "-ext",
        "WixUtilExtension",
        "-nologo",
        "-arch",
        "x64",
    ]

    cmd_candle3 = [
        "candle",
        "-out",
        str(product.with_suffix(".wixobj")),
        str(product),
        "-ext",
        "WixUtilExtension",
        f"-dSourceFilesDir={str(deploy)}",
        "-nologo",
        "-arch",
        "x64",
    ]

    cmd_light1 = [
        "light",
        "-out",
        str(msi),
        str(product.with_suffix(".wixobj")),
        str(components1.with_suffix(".wixobj")),
        str(actions.with_suffix(".wixobj")),
        "-ext",
        "WixUtilExtension",
        "-ext",
        "WixUIExtension",
        "-spdb",
        "-nologo",
    ]

    cmd_candle4 = [
        "candle",
        str(bundle.with_suffix(".wxs")),
        "-out",
        str(bundle.with_suffix(".wixobj")),
        "-ext",
        "WixBalExtension",
        "-ext",
        "WixUtilExtension",
        "-arch",
        "x64",
        f"-dMsiPath={str(msi)}",
        f"-dThemeFile={str(theme_file)}",
        f"-dLocalizationFile={str(localization_file)}",
        "-nologo",
    ]

    os.chdir(work1)
    cmd_light2 = [
        "light",
        str(bundle.with_suffix(".wixobj")),
        "-out",
        str(bundle),
        "-ext",
        "WixBalExtension",
        f"-dThemeFile={str(theme_file)}",
        f"-dLocalizationFile={str(localization_file)}",
        "-spdb",
        "-nologo",
    ]
    os.chdir(orig_cwd)

    cmd_insignia_deatch = [
        "insignia",
        "-ib",
        str(bundle),
        "-o",
        str(engine),
    ]

    cmd_insignia_reattach = [
        "insignia",
        "-ab",
        str(engine),
        str(bundle),
        "-o",
        str(bundle),
    ]

    cmds_with_signing = [
        cmd_heat,
        cmd_candle1,
        cmd_candle2,
        cmd_candle3,
        cmd_light1,
        "sign",
        cmd_candle4,
        cmd_light2,
        "sign",
        "unsign_bundle",  # signtool remove /s bundle.exe
        cmd_insignia_deatch,
        cmd_insignia_reattach,
        "sign",
    ]

    cmds_no_signing = [
        cmd_heat,
        cmd_candle1,
        cmd_candle2,
        cmd_candle3,
        cmd_light1,
        cmd_candle4,
        cmd_light2,
    ]

    if not platform.system() == "Windows":
        for cmd in cmds_with_signing:
            if isinstance(cmd, list):
                print(shlex.join(cmd))
                continue
            print(cmd)
        return

    if not cfg.run_signtool:
        # no signing
        for cmd in cmds_no_signing:
            run(cmd)
    else:
        # signing
        removesalt.sign.sign_files(work1.parent)
        for cmd in cmds_with_signing:
            if type(cmd) == "list":
                run(cmd)
                continue
            removesalt.sign.sign_files(work1.parent)
