from disnake.interactions.application_command import ApplicationCommandInteraction
from bot.bot import Bot
from disnake.ext import commands


class Preview(commands.Cog):
    """Base cog for commands relating to previewing assets."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def preview(self, _: ApplicationCommandInteraction) -> None:
        """Command group for previewing assets."""
        pass


def setup(bot: Bot) -> None:
    """Loads the Preview cog."""
    bot.add_cog(Preview(bot))
