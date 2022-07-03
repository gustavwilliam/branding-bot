from disnake import ApplicationCommandInteraction, Attachment
from disnake.ext import commands
from disnake.ext.commands import BadArgument

from bot.bot import Bot
from bot.constants import OUTPUT_IMAGE_FORMATS
from bot.utils.executor import in_executor
from bot.utils.images import (
    download_bytes,
    download_image,
    filename_from_url,
    image_to_file,
    rasterize_svg,
)

OutputFormats = commands.option_enum(OUTPUT_IMAGE_FORMATS)


class Convert(commands.Cog):
    """Commands for converting between file formats"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def do_conversion(
        self,
        inter: ApplicationCommandInteraction,
        url: str,
        output_format: OutputFormats,
    ) -> None:
        await inter.response.defer()
        try:
            image = await download_image(url)
        except commands.BadArgument as e:
            try:  # It might be a .SVG
                raw_bytes = (await download_bytes(url)).getvalue()
                image = await in_executor(rasterize_svg, raw_bytes)
            except BadArgument:
                raise e  # Raise the original error

        output_file = await image_to_file(image, filename_from_url(url), output_format)
        await inter.edit_original_message(file=output_file)

    @commands.slash_command()
    async def convert(
        self,
        inter: ApplicationCommandInteraction,
    ) -> None:
        """Converts an image to a given format."""
        pass

    @convert.sub_command()
    async def from_url(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
        output_format: OutputFormats,
    ) -> None:
        """Converts an image to a given format.

        Parameters
        ----------
        image_url: A url to an image to convert.
        output_format: The requested output format.
        """
        await self.do_conversion(inter, image_url, output_format)

    @convert.sub_command()
    async def from_file(
        self,
        inter: ApplicationCommandInteraction,
        image: Attachment,
        output_format: OutputFormats,
    ) -> None:
        """Converts the provided image to a given format.

        Parameters
        ----------
        image_url: A url to an image to convert.
        output_format: The requested output format.
        """
        await self.do_conversion(inter, image.url, output_format)


def setup(bot: Bot) -> None:
    """Loads the Convert cog."""
    bot.add_cog(Convert(bot))
