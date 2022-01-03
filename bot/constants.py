import os
import pathlib


ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT is None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

# Environment variables
PREFIX = os.getenv("PREFIX", "b!")
TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", False)

# Paths
EXTENSIONS = pathlib.Path("bot/exts/")
LOG_FILE = pathlib.Path("log/gurkbot.log")
