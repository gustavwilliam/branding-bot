from typing import Literal

import disnake
from emoji import UNICODE_EMOJI_ENGLISH
from bot.bot import Bot
from bot.utils.embeds import create_embed
from bot.utils.emojis import alias_to_name, codepoint_from_input, get_emoji
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

BASE_URL = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main"
# https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u1f605.png


class NotoEmojis(commands.Cog):
    """Utilities for working with Noto Emojis."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def get_url(
        codepoint: str,
        format: Literal["png", "svg"],
        size: Literal[32, 72, 128, 512] = None,
    ) -> str:
        """Returns a source file URL for the specified emoji, in the corresponding format."""
        codepoint = codepoint.replace("-", "_")  # Noto uses underscores for file names

        if format == "svg":
            return f"{BASE_URL}/svg/emoji_u{codepoint}.svg"
        return f"{BASE_URL}/png/{size}/emoji_u{codepoint}.png"

    @staticmethod
    def build_embed(codepoint: str) -> disnake.Embed:
        """Returns the main embed for the `noto_emoji` commmand."""
        emoji = "".join(get_emoji(e) for e in codepoint.split("-"))

        embed = create_embed(
            title=alias_to_name(UNICODE_EMOJI_ENGLISH[emoji]),
            description=f"{codepoint.replace('-', ' ')}\n[Download svg]({NotoEmojis.get_url(codepoint, 'svg')})",
            thumbnail_url=NotoEmojis.get_url(codepoint, "png", 128),
        )
        return embed

    @commands.slash_command()
    async def noto_emoji(
        self, inter: ApplicationCommandInteraction, raw_emoji: str
    ) -> None:
        """Sends a preview of a given Noto Emoji, specified by codepoint or emoji."""
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
    """Loads the NotoEmojis cog."""
    bot.add_cog(NotoEmojis(bot))
