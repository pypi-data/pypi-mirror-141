import logging.config

from bom.configuration.configtree import ConfigTree


def setup_logger(config: ConfigTree) -> None:
    config.env  # pylint: disable=pointless-statement
    log_conf = config.get("logging")
    if not log_conf:
        raise ValueError("Invalid configuration.")

    logging.config.dictConfig(log_conf.to_dict())
