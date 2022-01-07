import os
from datetime import datetime

from disnake import AllowedMentions, Intents
from disnake.ext import commands
from loguru import logger

from bot.utils.extensions import EXTENSIONS, walk_extensions

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
        if constants.DEBUG and constants.TEST_SERVERS:
            bot_kwargs["test_guilds"] = constants.TEST_SERVERS

        super().__init__(**bot_kwargs)
        self.load_extensions()

        self.launch_time = datetime.utcnow().timestamp()

    def load_extensions(self) -> None:
        """Load all extensions as released by walk_extensions()."""
        logger.debug("Updating available extensions")
        EXTENSIONS.update(walk_extensions())
        logger.info("Start loading extensions from ./exts/")

        for ext in EXTENSIONS:
            try:
                self.load_extension(ext)
                logger.debug(f"Successfully loaded extension: {ext}")
            except Exception as e:
                logger.error(f"Error when loading extension: {ext}\n{e}")

        logger.info("Finished loading extenisons")

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
