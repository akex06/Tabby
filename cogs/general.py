import discord
import os

from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
from typing import Any, List, Optional

from src.constants import (
    HEXCOLOR
)

class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label = "Economy",
                description = "Interact with other members with the economy system",
                value = "economy"
            ),
            discord.SelectOption(
                label = "General",
                description = "Some general commands",
                value = "general"
            ),
            discord.SelectOption(
                label = "Levels",
                description = "Check who are the most active people in the server",
                value = "levels"
            ),
            discord.SelectOption(
                label = "Settings",
                description = "Configure your server at it's finest",
                value = "settings"
            )
        ]
        super().__init__(
            placeholder = "Select a category",
            min_values = 1,
            max_values = 1,
            options = options
        )
    
    async def callback(self, interaction: discord.Interaction) -> Any:
        embed = discord.Embed(description = "Detailed info about a command using `/commands <command>`", color = HEXCOLOR)
        embed.set_author(name = f"Help {self.values[0]}", icon_url = "https://cdn.discordapp.com/avatars/868470190499827762/bccea487fbde02fe8244c6ab9638bc74.webp")

        await interaction.message.edit(embed = embed, view = None)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

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
        extension: str = None
    ) -> None:
        if not extension:

            embed = discord.Embed(description = f"Tabby has `{len([x for x in os.listdir('./cogs') if x.endswith('.py')])}` categories and `y` commands", color = HEXCOLOR)
            embed.set_author(name = "Tabby Commands", url="https://tabbybot.xyz/commands", icon_url=self.bot.user.avatar.url)
            embed.add_field(name = "Help Menu", value = "Use `/commands` for a list of all commands\nUse `/commands <command>` for a specific description of a command", inline = False)
            embed.add_field(name = "Categories", value = "`/help economy` - Economy\n`/help general` - General\n`/help levels` - Levels\n`/help Settings` - Settings", inline = False)
            embed.add_field(name = "Links", value = "[Website](https://tabbybot.xyz/) | [Dashboard](https://tabbybot.xyz/dashboard) | [Support](https://discord.tabbybot.xyz/) | [Commands](https://tabbybot.xyz/commands)", inline = False)

            await ctx.reply(embed = embed, view = SelectView())

    @help.autocomplete("extension")
    async def extension_autocomplete(
        self,
        ctx: commands.Context,
        current: str
    ) -> List[app_commands.Choice[str]]:
        extensions = ["Economy", "Levels", "Settings", "General"]
        return [app_commands.Choice(name = extension, value = extension) for extension in extensions if current.lower() in extension.lower()]

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))