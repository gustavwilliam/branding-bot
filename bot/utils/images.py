import io

import aiohttp
from PIL import Image, UnidentifiedImageError
import disnake
from disnake.ext import commands


async def download_image(url: str) -> Image.Image:
    """Downloads image from a url and returns a it, or `None`, if no image was found."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    image_bytes = io.BytesIO(await resp.read())
                    try:
                        return Image.open(image_bytes)
                    except UnidentifiedImageError:
                        raise commands.BadArgument(
                            f"The given [URL]({url}) leads to an invalid image."
                        )

                raise commands.BadArgument(f"The given [URL]({url}) can't be accessed.")
        except (aiohttp.InvalidURL, aiohttp.ClientConnectionError):
            raise commands.BadArgument("The given URL is invalid.")


def image_to_file(image: Image.Image, filename: str = "image.png") -> disnake.File:
    """Converts a Pillow Image object to a Disnake File object."""
    with io.BytesIO() as image_binary:
        image.save(image_binary, "PNG")
        image_binary.seek(0)
        return disnake.File(fp=image_binary, filename=filename)
