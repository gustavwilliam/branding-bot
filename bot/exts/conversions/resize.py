from disnake import ApplicationCommandInteraction, Attachment
from disnake.ext import commands

from bot.bot import Bot
from bot.utils.executor import in_executor
from bot.utils.images import download_image, image_to_file

Size = tuple[int, int]


class Resize(commands.Cog):
    """Commands for resizing images"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _new_size(
        size: Size,
        width: int = None,
        height: int = None,
        scale: float = None,
    ) -> Size:
        """Gets a new image size, given the new width, height or scale compared to the old image."""
        if width == height == scale == None:
            raise ValueError(
                "At least one of the arguments `width`, `height` and `scale` must be provided."
            )
        if (
            (width is not None and width <= 0)
            or (height is not None and height == 0)
            or (scale is not None and scale == 0)
        ):
            raise ValueError("Width, height and scale must be greater than 0.")
        if scale and (width or height):
            raise ValueError(
                "When `scale` is provided, please don't pass `width` or `height`."
            )

        if scale:
            return (int(size[0] * scale), int(size[1] * scale))
        if width and height:
            return (width, height)
        if width:
            f_scale = width / size[0]
        if height:
            f_scale = height / size[1]
        return (int(size[0] * f_scale), int(size[1] * f_scale))  # type: ignore

    @commands.slash_command()
    async def resize(
        self,
        inter: ApplicationCommandInteraction,
        img: Attachment,
        width: int = None,
        height: int = None,
        scale: float = commands.param(default=None, gt=0, le=5.0),
    ) -> None:
        """
        Resizes an image.

        Parameters
        ----------
        width: New width in pixels
        height: New height in pixels
        scale: The scale of the new image compared to the old image. 1 is equal to the current image.
        """
        await inter.response.defer()
        image = await download_image(img.url)
        try:
            size = await in_executor(Resize._new_size, image.size, width, height, scale)
        except ValueError as e:
            raise commands.BadArgument(str(e))

        image = image.resize(size)
        await inter.edit_original_message(file=await image_to_file(image))


def setup(bot: Bot) -> None:
    """Loads the Resize cog."""
    bot.add_cog(Resize(bot))
