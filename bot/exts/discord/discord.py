import disnake
from bot.bot import Bot
from bot.constants import Emojis
from bot.utils.embeds import create_embed
from disnake import User
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

EMBED_WARNING = f"{Emojis.warn}  **This embed is not an official bot message**"


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

    @discord.sub_command()
    async def embed(
        self,
        inter: ApplicationCommandInteraction,
        title: str,
        description: str,
        # color: str = None,
        thumbnail_url: str = None,
        image_url: str = None,
        footer: str = None,
        footer_icon_url: str = None,
        author: str = None,
        author_icon_url: str = None,
    ) -> None:
        """Preview a discrod embed."""
        embed = disnake.Embed(
            title=title,
            description=description,
            # color=color,
        )
        embed.set_thumbnail(thumbnail_url or disnake.Embed.Empty)
        embed.set_image(image_url or disnake.Embed.Empty)
        embed.set_footer(
            text=footer or disnake.Embed.Empty,
            icon_url=footer_icon_url or disnake.Embed.Empty,
        )
        if author:
            embed.set_author(
                name=author,
                icon_url=author_icon_url or disnake.Embed.Empty,
            )

        send_disclaimer = not await self.bot.is_owner(inter.author)
        try:
            await inter.response.send_message(
                EMBED_WARNING if send_disclaimer else "",
                embed=embed,
            )
        except commands.CommandInvokeError:
            raise commands.BadArgument(
                "No valid embed could be generated form the given input."
            )


def setup(bot: Bot) -> None:
    """Loads the Discord cog."""
    bot.add_cog(Discord(bot))
