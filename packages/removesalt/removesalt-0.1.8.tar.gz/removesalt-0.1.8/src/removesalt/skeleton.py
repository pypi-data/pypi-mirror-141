import logging

import hydra
import omegaconf

# from removesalt import __version__
from removesalt import deploy, reorg, template, wix

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


# A logger for this file
log = logging.getLogger(__name__)


@hydra.main(config_path="conf", config_name="config.yaml")
def my_app(cfg: omegaconf.DictConfig) -> None:
    log.info("Starting script...")

    # for key in logging.Logger.manager.loggerDict:
    #     log.info(key)

    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("hydra").setLevel(logging.INFO)

    reorg.clean(cfg)
    reorg.main(cfg)
    template.main(cfg)
    wix.main(cfg)
    deploy.main(cfg)

    log.info("Script ends here")


if __name__ == "__main__":
    my_app()
