from loguru import logger
from PIL import Image
from disnake.interactions import ApplicationCommandInteraction
from bot.bot import Bot
from bot.constants import IconTemplates
from bot.utils.images import download_image, image_to_file
from disnake.ext import commands
from .preview import Preview

PREVIEW_MARGIN = 0
PREVIEW_SPACING = 10


class ServerIcon(commands.Cog):
    """Utilities for previewing server icons."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self._preview_size: tuple[int, int] | None = None

    @staticmethod
    def _get_preview_size() -> tuple[int, int]:
        logger.debug("Calculating background size for server icon preview.")
        width, height = 0, 0

        for template in IconTemplates:
            with Image.open(template.value) as image:
                width += image.width + PREVIEW_SPACING

                if image.height > height:
                    height = image.height

        return (
            width + PREVIEW_MARGIN * 2 - PREVIEW_SPACING,
            height + PREVIEW_MARGIN * 2,
        )

    @property
    def preview_size(self) -> tuple[int, int]:
        if self._preview_size is None:
            self._preview_size = self._get_preview_size()

        return self._preview_size

    @staticmethod
    def draw_background(background: Image.Image) -> Image.Image:
        x, y = PREVIEW_MARGIN, PREVIEW_MARGIN
        for template in IconTemplates:
            with Image.open(template.value) as template:
                background.paste(template, (x, y))
                x += template.width + PREVIEW_SPACING

        return background

    @Preview.preview.sub_command()
    async def server_icon(
        self,
        inter: ApplicationCommandInteraction,
        file_url: str,
    ) -> None:
        """Sends a preview of the given image, in different states."""
        preview = Image.new("RGBA", self.preview_size)
        self.draw_background(preview)

        server_icon = await download_image(file_url)
        await inter.response.send_message(file=image_to_file(preview))


def setup(bot: Bot) -> None:
    """Loads the ServerIcon cog."""
    bot.add_cog(ServerIcon(bot))
