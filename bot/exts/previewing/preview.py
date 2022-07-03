from typing import Literal

from disnake import ApplicationCommandInteraction, Attachment
from disnake.ext import commands
from PIL import Image

from bot.bot import Bot
from bot.utils.executor import in_executor
from bot.utils.images import add_background, download_image, image_to_file

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

    @preview.sub_command_group()
    async def server_icon(
        self,
        inter: ApplicationCommandInteraction,
    ) -> None:
        """Sends a preview of the given icon, in different states."""
        if icon := inter.filled_options.get("icon"):
            icon = icon.url
        elif icon := inter.filled_options.get("icon_url"):
            pass
        else:
            raise RuntimeError("the required option was not provided.")
        icon = (await download_image(icon.url)).resize(ICON_SIZE)
        icon = add_background(icon, Preview.background_color(mode.lower()))  # type: ignore

        def _preview():
            with Image.open(ICON_TEMPLATES.format(mode=mode)) as template:
                preview = Image.new("RGBA", template.size)
                for position in ICON_POSITIONS:
                    preview.paste(icon, position)

                with Image.open(ICON_TEMPLATES.format(mode="Mask")) as mask:
                    mask = mask.convert("L")
                    return Image.composite(preview, template, mask)

        preview = await in_executor(_preview)

        await inter.response.send_message(file=await image_to_file(preview))

    @server_icon.sub_command('from_url')
    async def server_icon_from_url(
        self,
        inter: ApplicationCommandInteraction,
        icon_url: str,
        mode: Modes = "Dark",
    ):
        """
        Send a preview of the given icon in different states.

        Parameters
        ----------
        icon_url: The url of the icon.
        mode: Whether to show the preview in light or dark mode. (Defaults to dark.)
        """
        pass

    @server_icon.sub_command('from_file')
    async def server_icon_from_file(
        self,
        inter: ApplicationCommandInteraction,
        icon: Attachment,
        mode: Modes = "Dark",
    ):
        """
        Send a preview of the given icon in different states.

        Parameters
        ----------
        icon: The icon to preview.
        mode: Whether to show the preview in light or dark mode. (Defaults to dark.)
        """
        pass


def setup(bot: Bot) -> None:
    """Loads the Preview cog."""
    bot.add_cog(Preview(bot))
