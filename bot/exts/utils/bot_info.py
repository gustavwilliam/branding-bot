from datetime import datetime
from platform import python_version

import humanize
from bot.bot import Bot
from bot.constants import INVITE, About
from disnake import __version__
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from bot.utils.embeds import create_embed


class BotInfo(commands.Cog):
    """Get information about the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter: ApplicationCommandInteraction) -> None:
        """Ping the bot and return the latency."""
        embed = create_embed(
            title="Pong!",
            description=f"Gateway Latency: {round(self.bot.latency * 1000)}ms",
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def stats(self, inter: ApplicationCommandInteraction) -> None:
        """Get information about the version and current uptime of the bot."""
        uptime = humanize.precisedelta(
            datetime.utcnow().timestamp() - self.bot.launch_time
        )
        embed = create_embed(
            title="Bot stats",
            fields={
                "Python version": python_version(),
                "Disnake version": __version__,
                "Uptime": uptime,
            },
            thumbnail_url=self.bot.user.display_avatar.url,
        )

        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def about(self, inter: ApplicationCommandInteraction) -> None:
        """Get information about bot."""
        embed = create_embed(
            title=About.name,
            description=About.description,
            fields={"Source code": f"[View on GitHub]({About.repo_url})"},
            fields_inline=True,
            thumbnail_url=self.bot.user.display_avatar.url,
        )
        if INVITE:
            embed.add_field(
                name="Invite",
                value=f"[Invite to your server]({INVITE})",
            )

        await inter.response.send_message(embed=embed)


def setup(bot: Bot) -> None:
    """Loads the BotInfo cog."""
    bot.add_cog(BotInfo(bot))
