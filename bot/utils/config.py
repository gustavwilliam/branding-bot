from contextlib import suppress
from pathlib import Path
from typing import Type
from bot.utils.helpers import get_class_attributes

import yaml
from loguru import logger

CONFIG_FILE = Path("config.yaml")

try:
    with open(CONFIG_FILE) as f:
        logger.info(f"Loading YAML config from {CONFIG_FILE}.")
        _YAML_CONFIG = yaml.safe_load(f.read())

        if _YAML_CONFIG is None:  # File is empty
            _YAML_CONFIG = {}
except FileNotFoundError:
    logger.info(
        f"No YAML config file found at {CONFIG_FILE}. "
        "Proceeding with default config."
    )
    _YAML_CONFIG = {}


def env_list(
    data: str | None,
    type_: type = str,
    delimiter: str = ",",
) -> list | None:
    """
    Splits the given `data` and returns a list of values, with the given `output_type`.

    Returns `None` if `data` is `None`
    """
    if data is not None:
        return [type_(item) for item in data.split(delimiter)]


def autochain(cls: Type) -> Type:
    """
    Decorator for automatically overwriting attributes of a NamedTuple
    with values specifed in the CONFIG_FILE. The name of the NamedTuple
    class will be used as the name of the section in the YAML config file.

    Example usage
    -------------
    #constants.py
    @autochain
    class Emojis(NamedTuple):
        cross = "<:cross:928492357870034987>"
        check = "CorruptedEmoji"

    #config.yaml
    emojis:
        check = <:check:928492358230769674>
        warn: <:warn:928492358574702592>

    #python
    >>> from constans import Emojis
    >>> Emojis.cross
    "<:cross:928492357870034987>"
    >>> Emojis.check
    <:check:928492358230769674>
    >>> Emojis.warn
    <:warn:928492358574702592>
    """

    class ChainClass(cls):
        pass

    for attr in get_class_attributes(cls):
        setattr(ChainClass, *attr)
    with suppress(KeyError):
        for name, value in _YAML_CONFIG[cls.__name__.lower()].items():
            setattr(ChainClass, name, value)

    return ChainClass
