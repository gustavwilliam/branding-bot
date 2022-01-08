from typing import Literal

from bot.bot import Bot
from bot.utils.executor import in_executor
from bot.utils.images import add_background, download_image, image_to_file
from disnake.ext import commands
from disnake.interactions.application_command import \
    ApplicationCommandInteraction
from PIL import Image

ICON_TEMPLATES = "bot/assets/templates/server_icon/{mode}.png"
ICON_POSITIONS = [(12, 42), (94, 42), (176, 42)]
ICON_SIZE = (48, 48)

Modes = commands.option_enum(["Dark", "Light"])


class Preview(commands.Cog):
    """Base cog for commands relating to previewing assets."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def background_color(mode: Literal["light", "dark"]) -> str:
        """Returns an RGBA hexadecimal color based on the mode."""
        return "#202225FF" if mode == "dark" else "#E2E5E8FF"

    @commands.slash_command()
    async def preview(self, _: ApplicationCommandInteraction) -> None:
        """Command group for previewing assets."""
        pass

    @preview.sub_command()
    async def server_icon(
        self, inter: ApplicationCommandInteraction, file_url: str, mode: Modes = "Dark"
    ) -> None:
        """Sends a preview of the given image, in different states."""
        icon = (await download_image(file_url)).resize(ICON_SIZE)
        icon = add_background(icon, Preview.background_color(mode.lower()))  # type: ignore

        def preview():
            with Image.open(ICON_TEMPLATES.format(mode=mode)) as template:
                preview = Image.new("RGBA", template.size)
                for position in ICON_POSITIONS:
                    preview.paste(icon, position)

                with Image.open(ICON_TEMPLATES.format(mode="Mask")) as mask:
                    mask = mask.convert("L")
                    return Image.composite(preview, template, mask)

        preview = await in_executor(preview)

        await inter.response.send_message(file=await image_to_file(preview))


def setup(bot: Bot) -> None:
    """Loads the Preview cog."""
    bot.add_cog(Preview(bot))
