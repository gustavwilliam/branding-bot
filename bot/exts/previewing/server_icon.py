from pathlib import Path
from disnake.interactions import ApplicationCommandInteraction
from bot.bot import Bot
from bot.utils.images import download_image, image_to_file
from disnake.ext import commands
from .preview import Preview

preview = Preview.preview

TEMPLATE_ICON_PREVIEWS_BASE = Path("bot/assets/templates/server_icon")


class ServerIcon(commands.Cog):
    """Utilities for previewing server icons."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @preview.sub_command()
    async def server_icon(
        self,
        inter: ApplicationCommandInteraction,
        file_url: str,
    ) -> None:
        """Sends a preview of the given image, in different states."""
        image = await download_image(file_url)
        await inter.response.send_message(file=image_to_file(image))


def setup(bot: Bot) -> None:
    """Loads the ServerIcon cog."""
    bot.add_cog(ServerIcon(bot))
