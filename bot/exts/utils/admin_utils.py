from bot.utils.embeds import create_embed
from disnake.ext import commands
from disnake.ext.commands import Context
from bot.bot import Bot

from loguru import logger


class AdminUtils(commands.Cog):
    """Utilities for administrating the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(aliases=("exit", "quit"))
    @commands.is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """Shuts down the bot."""
        logger.info(f"Shutdown initiated by {ctx.author} ({ctx.author.id})")

        embed = create_embed("confirmation", "Shutting down...")
        await ctx.send(embed=embed)
        await self.bot.close()


def setup(bot: Bot) -> None:
    """Loads the AdminUtils cog."""
    bot.add_cog(AdminUtils(bot))
