import discord

from discord.ext import commands
from datetime import datetime

from src.constants import (
    HEXCOLOR
)

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "user-info",
        description = "Check user information",
        with_app_command = True
    )
    @commands.guild_only()
    async def user_info(
        self,
        ctx: commands.Context,
        member: discord.Member = None
    ) -> None:
        if not member:
            member = ctx.author

        embed = discord.Embed(description = f"{member} information", color = member.color)
        embed.set_author(name = member, icon_url = member.avatar.url)
        embed.add_field(name = "Name", value = member)
        embed.add_field(name = "Id", value = member.id)
        embed.add_field(name = "Created at", value = member.created_at())
        embed.add_field(name = "Status", value = member.status)
        embed.add_field(name = "Nick", value = member.nick)
        embed.add_field(name = "Roles", value = "\n".join([x.mention for x in member.roles]))
        embed.set_footer(text = datetime.now().strftime("%H:%M:%S"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))