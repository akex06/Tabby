#   BOT MADE BY AKEX06
#   https://github.com/akex06 <3

import discord

from discord.ext import commands
from discord import app_commands, errors
from src.tabby import conn, c

from src.constants import (
    TOKEN,
    DEFAULT_PREFIX
)

def get_prefix(client: discord.Client, message: discord.Message):
    c.execute("SELECT prefix FROM prefixes WHERE guild = %s", (message.guild.id, ))
    prefix = c.fetchone()
    if not prefix:
        c.execute("INSERT INTO prefixes (guild, prefix) VALUES (%s, %s)", (message.guild.id, DEFAULT_PREFIX))
        conn.commit()

        return DEFAULT_PREFIX

    return prefix[0]

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=get_prefix,
            intents=discord.Intents.all(),
            help_command = None
        )

    async def on_ready(self) -> None:
        print(f"[   READY   ]: {self.user}")
        print(f"[   GUILDS   ]: {len(self.guilds)}")
        print(f"[   USERS   ]: {len(self.users)}")

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.economy")
        await self.load_extension("cogs.levels")
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.settings")
        await self.load_extension("cogs.moderation")
        
        await self.tree.sync()

bot = Bot()
bot.run(TOKEN)