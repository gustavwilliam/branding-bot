import os
from datetime import datetime

from disnake import AllowedMentions, Intents
from disnake.ext import commands
from loguru import logger

from . import constants


class Bot(commands.Bot):
    """The core of the bot."""

    def __init__(self) -> None:
        intents = Intents.default()
        intents.members = True
        intents.presences = True

        bot_kwargs = {
            "command_prefix": constants.PREFIX,
            "intents": intents,
            "allowed_mentions": AllowedMentions(
                everyone=False,
                users=True,
                roles=[],
                replied_user=True,
            ),
        }
        if constants.DEBUG:
            bot_kwargs["test_guilds"] = [793864455527202847]

        super().__init__(**bot_kwargs)
        self.load_extensions()

        self.launch_time = datetime.utcnow().timestamp()

    def load_extensions(self) -> None:
        """Load all the extensions in the exts/ folder."""
        logger.info("Start loading extensions from ./exts/")
        for extension in constants.EXTENSIONS.glob("*/*.py"):
            if extension.name.startswith("_"):
                continue  # Ignore files starting with _
            dot_path = str(extension).replace(os.sep, ".")[:-3]  # Remove the .py
            self.load_extension(dot_path)
            logger.info(f"Successfully loaded extension: {dot_path}")

    def run(self) -> None:
        """Run the bot with the token in constants.py/.env ."""
        logger.info("Starting bot")

        if constants.TOKEN is None:
            raise EnvironmentError(
                "token value is None. Make sure you have configured the TOKEN field in .env"
            )

        super().run(constants.TOKEN)

    async def on_ready(self) -> None:
        """Ran when the bot has connected to discord and is ready."""
        logger.info("Bot online")
