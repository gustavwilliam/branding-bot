import disnake
from disnake.ext.commands.errors import BadArgument
from bot.bot import Bot
from bot.constants import Emojis
from bot.utils.embeds import create_embed
from bot.utils.color import parse_color, rgb_to_hex
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
        color: str = None,
        thumbnail_url: str = None,
        image_url: str = None,
        footer: str = None,
        footer_icon_url: str = None,
        author: str = None,
        author_url: str = None,
        author_icon_url: str = None,
    ) -> None:
        """Preview a Discord embed."""
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
                url=author_url or disnake.Embed.Empty,
                icon_url=author_icon_url or disnake.Embed.Empty,
            )
        if color:
            try:
                color = rgb_to_hex(parse_color(color)).removeprefix("#")
                embed.color = int(color, base=16)
            except ValueError as e:
                raise BadArgument(str(e))

        send_disclaimer = not await self.bot.is_owner(inter.author)
        await inter.response.send_message(
            EMBED_WARNING if send_disclaimer else "",
            embed=embed,
        )

    @embed.error
    async def on_embed_error(
        inter: ApplicationCommandInteraction,
        error: commands.CommandInvokeError,
    ) -> None:
        """Error event handler for `embed` command."""
        match error.original:
            # https://stackoverflow.com/a/67525259/13884898
            # It's required to do `disnake.HTTPException`,
            # instead of just `HTTPException`
            case disnake.HTTPException:
                raise commands.BadArgument(
                    "Invalid URL provided."
                )
            case _:
                raise commands.BadArgument(
                    "No valid embed could be generated from the given input."
                )
            

def setup(bot: Bot) -> None:
    """Loads the Discord cog."""
    bot.add_cog(Discord(bot))
