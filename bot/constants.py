import os
import pathlib
from typing import NamedTuple


ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

# Environment variables
PREFIX = os.getenv("PREFIX", "b!")
TOKEN = os.getenv("TOKEN")
INVITE = os.getenv("INVITE")
DEBUG = os.getenv("DEBUG", False)

# Paths
EXTENSIONS = pathlib.Path("bot/exts/")
LOG_FILE = pathlib.Path("log/gurkbot.log")


class About(NamedTuple):
    name = "Branding Bot"
    description = "A Discord utility bot for working with server branding."
    repo_url = "https://github.com/gustavwilliam/branding-bot"
