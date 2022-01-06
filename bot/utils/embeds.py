from typing import Literal
import random
from bot.constants import EmbedColors, EmbedEmojis, EmbedTitles
from disnake import Embed

EMBED_TYPES = Literal["info", "confirmation", "warning", "error"]


def _title(embed_type: Literal["confirmation", "warning", "error"]) -> str:
    titles = getattr(EmbedTitles, embed_type)
    return f"{getattr(EmbedEmojis, embed_type)}  {random.choice(titles)}"


def create_embed(
    embed_type: EMBED_TYPES = "info",
    description: str = None,
    *,
    title: str = None,
    url: str = None,
    fields: dict[str, str] = None,
    fields_inline: bool = False,
    thumbnail_url: str = None,
) -> Embed:
    """Returns an embed with default presets."""
    embed = Embed(
        description=description if description else Embed.Empty,
        url=url if url else Embed.Empty,
        color=getattr(EmbedColors, embed_type),
    )

    if title is not None:
        embed.title = title
    elif embed_type in ["warning", "error", "confirmation"]:
        embed.title = _title(embed_type)  # type: ignore

    if fields:
        for name, value in list(fields.items()):
            embed.add_field(name=name, value=value, inline=fields_inline)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed
