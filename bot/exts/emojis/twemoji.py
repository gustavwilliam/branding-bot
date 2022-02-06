from typing import Literal

import disnake
from emoji import UNICODE_EMOJI_ENGLISH
from bot.bot import Bot
from bot.utils.embeds import create_embed
from bot.utils.emojis import alias_to_name, codepoint_from_input, get_emoji
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction


BASE_URLS = {
    "png": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/",
    "svg": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/",
}


class Twemoji(commands.Cog):
    """Utilities for working with Twemojis."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def get_url(codepoint: str, format: Literal["png", "svg"]) -> str:
        """Returns a source file URL for the specified Twemoji, in the corresponding format."""
        return f"{BASE_URLS[format]}{codepoint}.{format}"

    @staticmethod
    def build_embed(codepoint: str) -> disnake.Embed:
        """Returns the main embed for the `twemoji` commmand."""
        emoji = "".join(get_emoji(e) for e in codepoint.split("-"))

        embed = create_embed(
            title=alias_to_name(UNICODE_EMOJI_ENGLISH[emoji]),
            description=f"{codepoint.replace('-', ' ')}\n[Download svg]({Twemoji.get_url(codepoint, 'svg')})",
            thumbnail_url=Twemoji.get_url(codepoint, "png"),
        )
        return embed

    @commands.slash_command()
    async def twemoji(
        self, inter: ApplicationCommandInteraction, raw_emoji: str
    ) -> None:
        """Sends a preview of a given Twemoji, specified by codepoint or emoji."""
        if len(raw_emoji) == 0:
            return
        try:
            codepoint = codepoint_from_input(raw_emoji)
        except ValueError:
            raise commands.BadArgument(
                "please include a valid emoji or emoji codepoint."
            )

        await inter.response.send_message(embed=self.build_embed(codepoint))


def setup(bot: Bot) -> None:
    """Load the Twemoji cog."""
    bot.add_cog(Twemoji(bot))
