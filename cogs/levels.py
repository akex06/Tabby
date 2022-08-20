import discord

from discord.ext import commands
from src.tabby import Tabby

from src.constants import (
    HEXCOLOR
)

tabby = Tabby()

class Levels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            member = message.author
            await tabby.add_exp(member)
            

    @commands.hybrid_command(
        name = "level",
        description = "Check a member's level",
        with_app_command = True
    )
    @commands.guild_only()
    async def level(
        self,
        ctx: commands.Context,
        member: discord.Member = None
    ) -> None:
        if not member:
            member = ctx.author

        level = await tabby.get_level(member)
        embed = discord.Embed(description = f"{member.name} is top x in level leaderboard", color = HEXCOLOR)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.add_field(name = "Level", value = level[0])
        embed.add_field(name = "Exp", value = level[1])

        await ctx.reply(
            embed = embed
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Levels(bot))