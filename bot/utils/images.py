import io
import os
from urllib.parse import urlparse

import aiohttp
import disnake
from bot.constants import OUTPUT_IMAGE_FORMATS
from disnake.ext import commands
from PIL import Image, UnidentifiedImageError


async def download_bytes(url: str) -> io.BytesIO:
    """Downloads bytes from a given `url` and return it."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return io.BytesIO(await resp.read())

                raise commands.BadArgument(f"The given [URL]({url}) can't be accessed.")
        except (aiohttp.InvalidURL, aiohttp.ClientConnectionError):
            raise commands.BadArgument("The given URL is invalid.")


async def download_image(url: str) -> Image.Image:
    """Downloads image from a url and returns a it."""
    try:
        return Image.open(await download_bytes(url))
    except UnidentifiedImageError:
        raise commands.BadArgument(f"The given [URL]({url}) leads to an invalid image.")


def image_to_file(
    image: Image.Image, filename: str = "image", format: str = "PNG"
) -> disnake.File:
    """
    Converts a Pillow Image object to a Disnake File object.

    Do not include any extension in the `filename` argument. For example, pass
    "image" instead of "image.png". The extension is appended
    automatically based on the format.
    """
    format = format.upper()
    if format not in OUTPUT_IMAGE_FORMATS:
        raise ValueError(
            f"'{format}' is not one of the supported formats ({', '.join(OUTPUT_IMAGE_FORMATS)})."
        )
    if format in ["JPEG", "PDF"]:
        image = image.convert("RGB")  # Removes transparancy

    with io.BytesIO() as image_binary:
        image.save(image_binary, format)
        image_binary.seek(0)
        return disnake.File(
            fp=image_binary,
            filename=f"{filename}.{format.lower()}",
        )


def bytes_to_file(byte_stream: bytes, filename: str = None) -> disnake.File:
    """Converts a bytes-like object to a Disnake File object."""
    image = Image.open(io.BytesIO(byte_stream))
    if filename:
        return image_to_file(image, filename)
    return image_to_file(image)


def filename_from_url(url: str) -> str:
    """
    Get the filename of a file, from a url

    Returns the first string in the filename. For example, "image" instead of
    "image.png", or "files" instead of "files.archive.zip".
    """
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename.split(".")[0]
