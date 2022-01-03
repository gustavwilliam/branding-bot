from bot.bot import Bot
from bot.utils.embeds import create_embed
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


def setup(bot: Bot) -> None:
    """Loads the AdminUtils cog."""
    bot.add_cog(AdminUtils(bot))
