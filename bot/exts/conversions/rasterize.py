from xml.etree.ElementTree import ParseError

from io import BytesIO
import cairosvg
from bot.bot import Bot
from bot.constants import OUTPUT_IMAGE_FORMATS
from bot.utils.images import download_bytes, filename_from_url, image_to_file
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction
from PIL import Image

OutputFormats = commands.option_enum(OUTPUT_IMAGE_FORMATS)


class Rasterize(commands.Cog):
    """Rasterizes vector graphics"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def rasterize(
        self,
        inter: ApplicationCommandInteraction,
        image_url: str,
        output_format: OutputFormats = "PNG",
        scale: int = 1,
    ) -> None:
        """Rasterizes a given SVG-file."""
        raw_bytes = (await download_bytes(image_url)).getvalue()
        try:
            output = cairosvg.svg2png(bytestring=raw_bytes, scale=scale)
        except ParseError:
            raise commands.BadArgument("The provided URL returns to an invalid SVG.")
        if not output:
            raise commands.BadArgument("No image was found.")

        image = Image.open(BytesIO(output))
        file = image_to_file(image, filename_from_url(image_url), output_format)

        await inter.response.send_message(file=file)


def setup(bot: Bot) -> None:
    """Loads the Rasterize cog."""
    bot.add_cog(Rasterize(bot))
