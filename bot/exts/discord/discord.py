from bot.bot import Bot
from bot.utils.embeds import create_embed
from disnake import User
from bot.utils.images import download_image, image_to_file
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction


class Discord(commands.Cog):
    """Base cog for commands relating to Discord assets."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def discord(self, _: ApplicationCommandInteraction) -> None:
        """Command group for Discord-related utilities."""

    @discord.sub_command()
    async def avatar(self, inter: ApplicationCommandInteraction, user: User) -> None:
        """Get the avatar of a Discord user."""
        embed = create_embed(
            title="Discord avatar",
            description=f"Showing {user.mention}'s avatar.",
            fields={
                "Link": f"[Download avatar]({user.avatar})",
            },
        )
        embed.set_thumbnail(user.avatar)

        await inter.response.send_message(embed=embed)


def setup(bot: Bot) -> None:
    """Loads the Discord cog."""
    bot.add_cog(Discord(bot))
