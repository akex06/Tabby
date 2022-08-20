import discord

from discord.ext import commands
from discord.ui import Button, View

from src.constants import (
    HEXCOLOR
)

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "discord",
        description = "Link to the support Discord",
        with_app_command = True
    )
    async def discord(
        self,
        ctx: commands.Context
    ) -> None:
        embed = discord.Embed(description = "Join our [Discord](https://discord.gg/urfHdtBwjT) server for support", color = HEXCOLOR)
        embed.set_author(name = "Discord", icon_url = self.bot.user.avatar.url, url = "https://discord.gg/urfHdtBwjT")

        await ctx.reply(embed = embed)


    @commands.hybrid_command(
        name = "dashboard",
        description = "Get a link to the dashboard",
        with_app_command = True
    )
    async def dashboard(
        self,
        ctx: commands.Context
    ) -> None:
        button = Button(label = "Link to Dashboard", url = "https://tabbybot.xyz/dashboard")

        view = View()
        view.add_item(button)

        await ctx.reply(view = view)

    @commands.hybrid_command(
        name = "commands",
        description = "Check all the commands from the bot",
        with_app_command = True
    )
    async def commands(
        self,
        ctx: commands.Context
    ) -> None:
        button = Button(label = "Link to Commands", url = "https://tabbybot.xyz/commands")

        view = View()
        view.add_item(button)

        await ctx.reply(view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))