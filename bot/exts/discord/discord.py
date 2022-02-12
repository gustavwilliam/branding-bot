from typing import NoReturn, Optional

import disnake
from disnake import Guild, Invite, User
from disnake.ext import commands
from disnake.ext.commands.errors import BadArgument
from disnake.interactions import ApplicationCommandInteraction

from bot.bot import Bot
from bot.constants import Emojis
from bot.utils.color import parse_color, rgb_to_hex
from bot.utils.embeds import create_embed

EMBED_WARNING = f"{Emojis.warn}  **This embed is not an official bot message**"


class Discord(commands.Cog):
    """Base cog for commands relating to Discord assets."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command()
    async def discord(self, _: ApplicationCommandInteraction) -> None:
        """Command group for Discord-related utilities."""

    @discord.sub_command()
    async def avatar(
        self, inter: ApplicationCommandInteraction, user: Optional[User] = None
    ) -> None:
        """Get the avatar of a Discord user."""
        if user is None:
            user = inter.author
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
    async def server(
        self,
        inter: ApplicationCommandInteraction,
        guild_id: Optional[Guild] = None,
        invite: Optional[Invite] = None,
    ) -> None:
        """
        Get the icon of a Discord server.

        Parameters
        ----------
        guild_id: ID of the Discord server
        invite: Invite to the Discord server
        """
        match (guild_id, invite):
            case (None, None):
                guild = inter.guild
                icon = guild.icon
            case (None, invite):
                if (guild := invite.guild) is None:
                    raise BadArgument("Cannot fetch the icon of a group DM.")
                icon = guild.icon
            case (guild, _):
                # Only `guild_id`, or `guild_id` and `invite` specified.
                icon = guild.icon

        if icon is None:
            raise BadArgument("The server does not have an icon.")

        embed = create_embed(
            title="Server icon",
            description=f"Showing server icon of `{guild.name}`.",
            fields={"Link": f"[Download icon]({icon})"},
        )
        embed.set_thumbnail(icon)
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

    @embed.error  # type: ignore
    async def on_embed_error(
        self,
        inter: ApplicationCommandInteraction,
        error: commands.CommandInvokeError,
    ) -> NoReturn:
        """Error event handler for `embed` command."""
        match error.original:
            # https://stackoverflow.com/a/67525259/13884898
            # It's required to do `disnake.HTTPException()`,
            # instead of just `HTTPException()`
            case disnake.HTTPException():
                raise commands.BadArgument("Invalid URL provided.")
            case _:
                raise commands.BadArgument(
                    "No valid embed could be generated from the given input."
                )

    @server.error
    async def server_error(
        self, inter: ApplicationCommandInteraction, error: Exception
    ):
        if isinstance(error, commands.ConversionError):
            if isinstance(error.original, commands.GuildNotFound):
                embed = create_embed(
                    embed_type="error",
                    title=str(error.original).removesuffix("."),
                    description="Invalid ID or the bot does not have access to the server.",
                )

            if isinstance(error.original, commands.BadInviteArgument):
                embed = create_embed(
                    embed_type="error",
                    title=str(error.original).removesuffix("."),
                )
            await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot: Bot) -> None:
    """Loads the Discord cog."""
    bot.add_cog(Discord(bot))
