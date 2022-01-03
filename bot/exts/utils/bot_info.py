from datetime import datetime
from platform import python_version

import humanize
from bot.bot import Bot
from bot.constants import INVITE, About
from disnake import Colour, Embed, __version__
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction


class BotInfo(commands.Cog):
    """Get information about the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter: ApplicationCommandInteraction) -> None:
        """Ping the bot and return the latency."""
        embed = Embed(
            title="Pong!",
            description=f"Gateway Latency: {round(self.bot.latency * 1000)}ms",
            color=Colour.blurple(),
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def stats(self, inter: ApplicationCommandInteraction) -> None:
        """Get information about the version and current uptime of the bot."""
        embed = Embed(
            title="Bot Stats",
            color=Colour.blurple(),
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        uptime = humanize.precisedelta(
            datetime.utcnow().timestamp() - self.bot.launch_time
        )
        fields = {
            "Python version": python_version(),
            "Disnake version": __version__,
            "Uptime": uptime,
        }
        for name, value in list(fields.items()):
            embed.add_field(name=name, value=value, inline=False)

        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def about(self, inter: ApplicationCommandInteraction) -> None:
        """Get information about bot."""
        embed = Embed(
            description=About.description,
            title=About.name,
            color=Colour.blurple(),
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(
            name="Source code",
            value=f"[View on GitHub]({About.repo_url})",
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
