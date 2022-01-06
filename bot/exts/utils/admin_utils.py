import contextlib
import inspect
import pprint
import re
import textwrap
import traceback
from io import StringIO
from typing import Any

import disnake
from bot.bot import Bot
from bot.utils.embeds import create_embed
from bot.utils.helpers import find_nth_occurrence
from disnake.channel import TextChannel
from disnake.errors import Forbidden, HTTPException, NotFound
from disnake.ext import commands
from disnake.ext.commands import Context
from disnake.message import Message
from loguru import logger


class AdminUtils(commands.Cog):
    """Utilities for administrating the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.env = {}
        self.ln = 0
        self.stdout = StringIO()

    @staticmethod
    async def _delete_message(message: Message) -> None:
        BASE_ERROR_MESSAGE = f"Message ({message.id}) could not be deleted."

        try:
            await message.delete()
        except Forbidden:
            logger.debug(f"{BASE_ERROR_MESSAGE} Missing permissions.")
        except NotFound:
            logger.debug(f"{BASE_ERROR_MESSAGE} It is already deleted.")
        except HTTPException:
            logger.debug(f"{BASE_ERROR_MESSAGE} The deletion request failed.")

    @commands.command(aliases=("exit", "quit"))
    @commands.is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """Shuts down the bot."""
        logger.info(f"Shutdown initiated by {ctx.author} ({ctx.author.id})")

        embed = create_embed("confirmation", "Shutting down...")
        await ctx.send(embed=embed)
        await self.bot.close()

    @commands.command(aliases=("print", "say"))
    @commands.is_owner()
    async def echo(
        self, ctx: Context, channel: TextChannel | None, *, content: str
    ) -> None:
        """Relays a message to the same or a different channel."""
        if channel is None:
            channel = ctx.channel  # type: ignore
        message = await channel.send(content)  # type: ignore

        if ctx.channel == channel:
            await AdminUtils._delete_message(ctx.message)
        else:
            embed = create_embed(
                "confirmation",
                f"Your message was sent. View it [here]({message.jump_url}).",
            )
            await ctx.send(embed=embed)

    def _format(self, inp: str, out: Any) -> tuple[str, disnake.Embed | None]:
        """Format the eval output into a string & attempt to format it into an Embed."""
        self._ = out

        res = ""

        # Erase temp input we made
        if inp.startswith("_ = "):
            inp = inp[4:]

        # Get all non-empty lines
        lines = [line for line in inp.split("\n") if line.strip()]
        if len(lines) != 1:
            lines += [""]

        # Create the input dialog
        for i, line in enumerate(lines):
            if i == 0:
                # Start dialog
                start = f"In [{self.ln}]: "

            else:
                # Indent the 3 dots correctly;
                # Normally, it's something like
                # In [X]:
                #    ...:
                #
                # But if it's
                # In [XX]:
                #    ...:
                #
                # You can see it doesn't look right.
                # This code simply indents the dots
                # far enough to align them.
                # we first `str()` the line number
                # then we get the length
                # and use `str.rjust()`
                # to indent it.
                start = "...: ".rjust(len(str(self.ln)) + 7)

            if i == len(lines) - 2:
                if line.startswith("return"):
                    line = line[6:].strip()

            # Combine everything
            res += start + line + "\n"

        self.stdout.seek(0)
        text = self.stdout.read()
        self.stdout.close()
        self.stdout = StringIO()

        if text:
            res += text + "\n"

        if out is None:
            # No output, return the input statement
            return (res, None)

        res += f"Out[{self.ln}]: "

        if isinstance(out, disnake.Embed):
            # We made an embed? Send that as embed
            res += "<Embed>"
            res = (res, out)

        else:
            if isinstance(out, str) and out.startswith(
                "Traceback (most recent call last):\n"
            ):
                # Leave out the traceback message
                out = "\n" + "\n".join(out.split("\n")[1:])

            if isinstance(out, str):
                pretty = out
            else:
                pretty = pprint.pformat(out, compact=True, width=60)

            if pretty != str(out):
                # We're using the pretty version, start on the next line
                res += "\n"

            if pretty.count("\n") > 20:
                # Text too long, shorten
                li = pretty.split("\n")

                pretty = (
                    "\n".join(li[:3])  # First 3 lines
                    + "\n ...\n"  # Ellipsis to indicate removed lines
                    + "\n".join(li[-3:])
                )  # last 3 lines

            # Add the output
            res += pretty
            res = (res, None)

        return res  # Return (text, embed)

    async def _eval(self, ctx: Context, code: str) -> disnake.Message | None:
        """Eval the input code string & send an embed to the invoking context."""
        self.ln += 1

        if code.startswith("exit"):
            self.ln = 0
            self.env = {}
            return await ctx.send("```Reset history!```")

        env = {
            "message": ctx.message,
            "author": ctx.message.author,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "ctx": ctx,
            "self": self,
            "bot": self.bot,
            "inspect": inspect,
            "discord": disnake,
            "disnake": disnake,
            "contextlib": contextlib,
        }

        self.env.update(env)

        # Ignore this code, it works
        code_ = """
async def func():  # (None,) -> Any
    try:
        with contextlib.redirect_stdout(self.stdout):
{0}
        if '_' in locals():
            if inspect.isawaitable(_):
                _ = await _
            return _
    finally:
        self.env.update(locals())
""".format(
            textwrap.indent(code, "            ")
        )

        try:
            exec(code_, self.env)  # noqa: B102,S102
            func = self.env["func"]
            res = await func()

        except Exception:
            res = traceback.format_exc()

        out, embed = self._format(code, res)
        out = out.rstrip("\n")  # Strip empty lines from output

        # Truncate output to max 15 lines or 1500 characters
        newline_truncate_index = find_nth_occurrence(out, "\n", 15)

        if newline_truncate_index is None or newline_truncate_index > 1500:
            truncate_index = 1500
        else:
            truncate_index = newline_truncate_index

        if len(out) > truncate_index:
            await ctx.send(
                f"```py\n{out[:truncate_index]}\n```" f"... response truncated",
                embed=embed,  # type: ignore
            )
            return

        await ctx.send(f"```py\n{out}```", embed=embed)  # type: ignore

    @commands.command(aliases=("e",))
    @commands.is_owner()
    async def eval(self, ctx: Context, *, code: str) -> None:
        """Run unrestricted eval in a REPL-like format."""
        code = code.strip("`")
        if re.match("py(thon)?\n", code):
            code = "\n".join(code.split("\n")[1:])

        if (
            not re.search(  # Check if it's an expression
                r"^(return|import|for|while|def|class|" r"from|exit|[a-zA-Z0-9]+\s*=)",
                code,
                re.M,
            )
            and len(code.split("\n")) == 1
        ):
            code = "_ = " + code

        await self._eval(ctx, code)


def setup(bot: Bot) -> None:
    """Loads the AdminUtils cog."""
    bot.add_cog(AdminUtils(bot))
