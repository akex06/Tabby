import discord

from discord.ext import commands
from src.tabby import Tabby

from src.constants import (
    MAX_PREFIX_LENGTH
)

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tabby = Tabby()

    @commands.hybrid_command(
        name = "setprefix",
        description = "Change the prefix of the server",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def setprefix(
        self,
        ctx: commands.Context,
        prefix: str
    ) -> None:
        if len(prefix) > MAX_PREFIX_LENGTH:
            await ctx.reply(
                f"The length of the prefix can't be larger than {MAX_PREFIX_LENGTH}",
                ephemeral = True
            )
            return

        await self.tabby.set_prefix(ctx.guild, prefix)

        await ctx.reply(
            f"The prefix succesfully changed to {prefix}"
        )

    @commands.hybrid_command(
        name = "channel",
        description = "Change settings from channels",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def channel(
        self,
        ctx: commands.Context,
        action: str,
        type: str,
        channel: discord.TextChannel
    ) -> None:
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))