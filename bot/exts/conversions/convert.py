from disnake.ext.commands.errors import BadArgument
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
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

OutputFormats = commands.option_enum(OUTPUT_IMAGE_FORMATS)


class Convert(commands.Cog):
    """Commands for converting between file formats"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def convert(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
        output_format: OutputFormats,
    ) -> None:
        """Convers an image to a given format."""
        try:
            image = await download_image(image_url)
        except commands.BadArgument as e:
            try:  # It might be a .SVG
                raw_bytes = (await download_bytes(image_url)).getvalue()
                image = await in_executor(rasterize_svg,raw_bytes)
            except BadArgument:
                raise e  # Raise the original error

        output_file = await image_to_file(image, filename_from_url(image_url), output_format)
        await inter.response.send_message(file=output_file)


def setup(bot: Bot) -> None:
    """Loads the Convert cog."""
    bot.add_cog(Convert(bot))
