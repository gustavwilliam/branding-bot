import os
import pathlib
from typing import NamedTuple

from disnake import Colour

from bot.utils.config import autochain, env_list

ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")


# Environment variables
TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", False)
PREFIX = os.getenv("PREFIX", "b!")
BOT_INVITE = os.getenv("BOT_INVITE")
TEST_SERVERS = env_list(os.getenv("TEST_SERVERS"), type_=int)
SERVER_INVITE = os.getenv("SERVER_INVITE")

# Paths
EXTENSIONS = pathlib.Path("bot/exts/")

OUTPUT_IMAGE_FORMATS = [
    "PNG",
    "JPEG",
    "ICO",
    "GIF",
    "PDF",
    "WEBP",
]  # `image_to_file` depends on this being uppercase.


class About(NamedTuple):
    name = "Branding Bot"
    repo_url = "https://github.com/gustavwilliam/branding-bot"
    description = "A Discord utility bot for working with server branding."


@autochain
class Emojis(NamedTuple):
    warn = "<:warn:928862585619628094>"
    cross = "<:cross:928858977381515294>"
    check = "<:check:928858977184411708>"

    status_dnd = "<:status_dnd:928866001611792445>"
    status_idle = "<:status_idle:928866001620197386>"
    status_online = "<:status_online:928866001641144360>"
    status_offline = "<:status_offline:928866001720852500>"


# Embeds
class EmbedColors(NamedTuple):
    info = Colour.blurple()
    error = Colour.red()
    warning = Colour.yellow()
    confirmation = Colour.green()


class EmbedEmojis(NamedTuple):
    error = Emojis.cross
    warning = Emojis.warn
    confirmation = Emojis.check


class EmbedTitles(NamedTuple):
    confirmation = [
        "Done!",
        "Alright",
        "Sure thing!",
        "You got it!",
        "Affirmative",
        "No problem!",
    ]
    warning = [
        "Be careful",
        "Proceed with caution",
        "Are you sure about that?",
    ]
    error = [
        "Nope",
        "Definitely not",
        "Let's not do that",
        "That was a mistake",
        "Out of the question",
        "That doesn't seem right",
    ]


class URLs(NamedTuple):
    github_bot_repo = "https://github.com/gustavwilliam/branding-bot/"
