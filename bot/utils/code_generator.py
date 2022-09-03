from dataclasses import dataclass
from typing import Union

from disnake import ButtonStyle
from disnake.ui import View, Button, button
from disnake.interactions import MessageInteraction

from bot.utils.color import parse_color, rgb_to_hex


class Code:
    """String object for convenience"""

    def __init__(self) -> None:
        self.code = ""

    def add(
        self,
        code: str,
        exists: Union[int, str, None] = True,
        indents: int = 0,
    ) -> None:
        """Helper method for adding code"""
        if isinstance(exists, str):
            code = code.format(f'{exists!r}')
        if exists:
            indent = "    " * indents
            self.code += (indent + code + "\n")


@dataclass
class EmbedCodeView(View):
    """View for buttons that generate code for various frameworks/libraries"""

    title: str
    description: str
    url: str = None
    color: str = None
    thumbnail_url: str = None
    image_url: str = None
    footer: str = None
    footer_icon_url: str = None
    author: str = None
    author_url: str = None
    author_icon_url: str = None

    def __post_init__(self):
        super().__init__()

    @button(label="Disnake Code", style=ButtonStyle.blurple)
    async def disnake_embed(self, button: Button, inter: MessageInteraction) -> None:
        """Generates embed in disnake"""
        code = Code()
        code.add("embed = disnake.Embed(")

        if self.color:
            color = rgb_to_hex(parse_color(self.color)).removeprefix("#")
            code.add(f"color=0x{color},", self.color, 1)
        code.add("title={},", self.title, 1)
        code.add("url={},", self.url, 1)
        code.add("description={},", self.description, 1)
        code.add(")")

        code.add("embed.set_footer(", self.footer)
        if self.footer:
            code.add("text={},", self.footer, 1)
            code.add("icon_url={},", self.footer_icon_url, 1)
        code.add(")", self.footer)

        code.add("embed.set_author(", self.author)
        if self.author:
            code.add("name={},", self.author, 1)
            code.add("url={},", self.author_url, 1)
            code.add("icon_url={},", self.author_icon_url, 1)
        code.add(")", self.author)

        code.add("embed.set_thumbnail({})", self.thumbnail_url)
        code.add("embed.set_image({})", self.image_url)

        await inter.response.send_message(f"```py\n{code.code}\n```")
