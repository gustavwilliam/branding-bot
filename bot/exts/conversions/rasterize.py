from disnake import ApplicationCommandInteraction, Attachment
from disnake.ext import commands

from bot.bot import Bot
from bot.constants import OUTPUT_IMAGE_FORMATS
from bot.utils.executor import in_executor
from bot.utils.images import (
    download_bytes,
    filename_from_url,
    image_to_file,
    rasterize_svg,
)

OutputFormats = commands.option_enum(OUTPUT_IMAGE_FORMATS)


class Rasterize(commands.Cog):
    """Rasterizes vector graphics"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def do_rasterize(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
        output_format: OutputFormats,
        scale: int,
    ):
        await inter.response.defer()

        raw_bytes = (await download_bytes(image_url)).getvalue()

        image = await in_executor(rasterize_svg, raw_bytes, scale)
        file = await image_to_file(
            image, filename_from_url(image.filename), output_format
        )

        await inter.edit_original_message(file=file)

    @commands.slash_command()
    async def rasterize(
        self,
        inter: ApplicationCommandInteraction,
        image: Attachment,
        output_format: OutputFormats = "PNG",
        scale: int = 1,
    ) -> None:
        """Rasterizes a given SVG-file."""
        pass

    @rasterize.sub_command()
    async def from_url(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
        output_format: OutputFormats = "PNG",
        scale: int = 1,
    ):
        """Rasterizes a given SVG-file.

        Parameters
        ----------
        image: The image to rasterize.
        output_format: The perferred output format.
        scale: The factor to scale the image by.
        """
        await self.do_rasterize(inter, image_url, output_format, scale)

    @rasterize.sub_command()
    async def from_file(
        self,
        inter: ApplicationCommandInteraction,
        image: Attachment,
        output_format: OutputFormats = "PNG",
        scale: int = 1,
    ):
        """Rasterizes a given SVG-file.

        Parameters
        ----------
        image: The image to rasterize.
        output_format: The perferred output format.
        scale: The factor to scale the image by.
        """
        await self.do_rasterize(inter, image.url, output_format, scale)


def setup(bot: Bot) -> None:
    """Loads the Rasterize cog."""
    bot.add_cog(Rasterize(bot))
