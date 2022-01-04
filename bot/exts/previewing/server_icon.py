from loguru import logger
from PIL import Image
from disnake.interactions import ApplicationCommandInteraction
from bot.bot import Bot
from bot.utils.images import download_image, image_to_file
from disnake.ext import commands
from .preview import Preview

ICON_TEMPLATES = "bot/assets/templates/server_icon/{mode}.png"
ICON_POSITIONS = [(12, 42), (94, 42), (176, 42)]
ICON_SIZE = (48, 48)

Modes = commands.option_enum(["Dark", "Light"])


class ServerIcon(commands.Cog):
    """Utilities for previewing server icons."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def to_mask(image: Image.Image) -> Image.Image:
        data: list[int] = []
        for item in image.convert("RGBA").getdata():
            data.append(0 if item[3] == 0 else 256)

        mask = Image.new("L", image.size)
        mask.putdata(data)
        return mask

    @staticmethod
    def add_background(image: Image.Image, color: str | int):
        canvas = Image.new("RGBA", image.size, color=color)
        return Image.composite(image, canvas, ServerIcon.to_mask(image))

    @staticmethod
    def draw_icons(background: Image.Image, icon: Image.Image) -> None:
        for position in ICON_POSITIONS:
            background.paste(icon, position)

    @Preview.preview.sub_command()
    async def server_icon(
        self, inter: ApplicationCommandInteraction, file_url: str, mode: Modes = "Dark"
    ) -> None:
        """Sends a preview of the given image, in different states."""
        icon = (await download_image(file_url)).resize(ICON_SIZE)
        icon = ServerIcon.add_background(
            icon, "#202225FF" if mode == "Dark" else "#E2E5E8FF"
        )

        with Image.open(ICON_TEMPLATES.format(mode=mode)) as template:
            preview = Image.new("RGBA", template.size)
            ServerIcon.draw_icons(preview, icon)

            with Image.open(ICON_TEMPLATES.format(mode="Mask")) as mask:
                mask = mask.convert("L")
                preview = Image.composite(preview, template, mask)

        await inter.response.send_message(file=image_to_file(preview))


def setup(bot: Bot) -> None:
    """Loads the ServerIcon cog."""
    bot.add_cog(ServerIcon(bot))
