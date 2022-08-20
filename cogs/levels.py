import discord

from discord.ext import commands
from discord.ui import Button, View
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

        level, exp = tuple(map(int, await tabby.get_level(member)))
        embed = discord.Embed(description = f"{member.name} is top x in level leaderboard", color = HEXCOLOR)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.add_field(name = "Level", value = level)
        embed.add_field(name = "Exp", value = exp)

        level += 1
        needed_exp = 5 * (level ** 2) + (50 * level) + 100
        n = int(exp / needed_exp * 10)
        progress = " ".join([':blue_square:' for x in range(n)] + [':black_large_square:' for x in range(10 - n)])

        embed.add_field(name = "Progress", value = progress, inline = False)
        await ctx.reply(
            embed = embed
        )

    @commands.hybrid_command(
        name = "levels",
        description = "Check the level leaderboard",
        with_app_command = True
    )
    @commands.guild_only()
    async def levels(
        self,
        ctx: commands.Context
    ) -> None:
        leaderboard = await tabby.get_level_leaderboard(ctx.guild)
        
        embed = discord.Embed(description = f"Top 10 level leaderboard in the server, check the whole leaderboard [here](https://tabbybot.xyz/leaderboard/levels/{ctx.guild.id})", color = HEXCOLOR)
        embed.set_author(name = f"{ctx.guild.name} levels", icon_url = ctx.guild.icon.url, url = f"https://tabbybot.xyz/leaderboard/levels/{ctx.guild.id}")

        for i in leaderboard:
            member = ctx.guild.get_member(int(i[0]))

            embed.add_field(
                name = member.name,
                value = f"```Level: {i[1]} Exp: {i[2]}```",
                inline = False
            )

        button = Button(label = "See full leaderboard", emoji = "🔗", url = f"https://tabbybot.xyz/leaderboard/levels/{ctx.guild.id}")
        view = View()
        view.add_item(button)

        await ctx.reply(view = view, embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Levels(bot))