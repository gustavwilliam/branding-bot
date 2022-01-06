from datetime import datetime
from platform import python_version

import humanize
from bot.bot import Bot
from bot.constants import BOT_INVITE, SERVER_INVITE, About
from disnake import __version__, embeds
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
        guilds = self.bot.guilds
        embed = create_embed(
            title="Bot stats",
            fields={
                "Python version": python_version(),
                "Disnake version": __version__,
                "Uptime": uptime,
            },
            thumbnail_url=self.bot.user.display_avatar.url,
        )
        embed.add_field(name="Servers", value=len(guilds))
        embed.add_field(
            name="Members",
            value=sum([guild.member_count for guild in guilds]),
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
        if BOT_INVITE:
            embed.add_field(
                name="Bot invite", value=f"[Invite to server]({BOT_INVITE})"
            )
        if SERVER_INVITE:
            embed.add_field(
                name="Server invite", value=f"[Join server]({SERVER_INVITE})"
            )

        await inter.response.send_message(embed=embed)


def setup(bot: Bot) -> None:
    """Loads the BotInfo cog."""
    bot.add_cog(BotInfo(bot))
