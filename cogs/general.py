import discord
import os

from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
from typing import List 

from src.constants import (
    HEXCOLOR
)

class General(commands.Cog, name = "general"):
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
    async def command(
        self,
        ctx: commands.Context,
        command: str = None
    ) -> None:
        if not command:    
            button = Button(label = "Link to Commands", url = "https://tabbybot.xyz/commands")

            view = View()
            view.add_item(button)

            await ctx.reply(view = view)

    @commands.hybrid_command(
        name = "help",
        description = "Dsiplays a help menu",
        with_app_command = True
    )
    async def help(
        self,
        ctx: commands.Context,
        extension: str = None,
        command: commands.Command = None
    ) -> None:
        if not extension:
            embed = discord.Embed(description = f"Tabby has `{len([x for x in os.listdir('./cogs')])}` categories and `{len(self.bot.commands)}` commands", color = HEXCOLOR)
            embed.set_author(name = "Tabby's Help Menu", url = "https://tabbybot.xyz/commands", icon_url = self.bot.user.avatar.url)
            embed.add_field(name = "Help Commands", value = "List of commands: `/help <category>`\nSpecific command help: `/help <command>`", inline = False)
            embed.add_field(name = "Categories", value = '\n'.join([f'`/help {name}` » {name.title()}' for name, cog in self.bot.cogs.items()]), inline = False)

            await ctx.reply(embed = embed)

            

    @help.autocomplete("extension")
    async def extension_autocomplete(
        self,
        ctx: commands.Context,
        current: str
    ) -> List[app_commands.Choice[str]]:
        extensions = [x.title() for x in self.bot.cogs.keys()]
        return [app_commands.Choice(name = extension, value = extension) for extension in extensions if current.lower() in extension.lower()]

    @help.autocomplete("command")
    async def command_autocomplete(
        self,
        ctx: commands.Context,
        current: str
    ) -> List[app_commands.Choice[str]]:
        commands = [x.name.title() for x in self.bot.commands]
        return [app_commands.Choice(name = command, value = command) for command in commands if current.lower() in command.lower()]

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))