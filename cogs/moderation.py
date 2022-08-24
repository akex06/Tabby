import discord

from discord.ext import commands
from datetime import datetime, timedelta
from typing import List, Optional, Union

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name = "kick",
        description = "Kick a member from the server",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        reason: Optional[str] = "A reason hasn't been set"
    ) -> None:
        await member.kick(reason = reason)
        await ctx.reply(f"{member} has been kicked")


    @commands.hybrid_command(
        name = "ban",
        description = "Bans a member from the server",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        delete_message_days: int = 0,
        reason: Optional[str] = "A reason hasn't been set",

    ) -> None:
        if delete_message_days > 7:
            delete_message_days = 7

        elif delete_message_days < 0:
            delete_message_days = 0

        await member.ban(reason = reason)
        await ctx.reply(f"{member} has been banned")

    @commands.hybrid_command(
        name = "unban",
        description = "Unbans a member from the server"
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def unban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        reason: Optional[str] = "A reason hasn't been set"
    ) -> None:
        await member.unban(reason = reason)
        await ctx.reply(f"{member} has been unbaned")

    @commands.hybrid_command(
        name = "timeout",
        description = "Timeout a member from the server"
    )
    @commands.guild_only()
    @commands.has_permissions(moderate_members = True)
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member,
        until: Optional[Union[timedelta, datetime]],
        reason: Optional[str] = "A reason hasn't been set"
    ) -> None:
        await member.timeout(until = until, reason = reason)
        await ctx.reply(f"{member} has been kicked")

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))