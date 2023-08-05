import os
import logging
from collections import namedtuple

import click
import yaml
from . import core


@click.command()
@click.argument("config")
@click.argument("mount")
def main(config, mount):
    """
    Mount an instabase drive
    to local folder using a config file.
    """
    with open(config, "r") as fl:
        config = yaml.safe_load(fl.read())
    for key in [
        "instance",
        "folder",
        "api",
        "allow_ext",
        "invalidate_cache_after_n_seconds",
        "api_timeout",
    ]:
        if key not in config:
            raise ValueError(f"{key} missing in config")
    # --- freeze config
    config = {k: tuple(v) if isinstance(v, list) else v for k, v in config.items()}
    config["token"] = os.environ["IB_TOKEN"]
    config["folder"] = "/" + config["folder"].lstrip("/")
    config["instance"] = config["instance"].rstrip("/")
    # Default options
    config["enable_local_files"] = config.get("enable_local_files", True)
    Config = namedtuple("Config", " ".join(sorted(config.keys())))
    config = Config(**config)
    print(config)
    logging.basicConfig(level=logging.INFO)

    core.FUSE(
        core.IBFS(config, mount),
        mount,
        foreground=True,
        nothreads=True,
        allow_other=True,
    )


if __name__ == "__main__":
    main()
