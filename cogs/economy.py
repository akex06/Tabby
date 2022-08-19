import discord

from discord import app_commands, ui
from discord.ext import commands
from src.tabby import Tabby
from datetime import datetime

tabby = Tabby()

class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name = "bal",
        description = "Check's an user balance"
    )
    @commands.guild_only()
    async def balance(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ) -> None:
        if not member:
            member = interaction.user

        wallet, bank = await tabby.get_bal(member)

        embed = discord.Embed(description = f"{member.name} is top x in economy leaderboard", color = tabby.hexcolor)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name = "Wallet", value = wallet)
        embed.add_field(name = "Bank", value = bank)

        await interaction.response.send_message(embed = embed)

    @app_commands.command(
        name = "deposit",
        description = "Deposit money into your bank"
    )
    async def deposit(
        self,
        interaction: discord.Interaction,
        amount: int = None
    ) -> None:
        if not amount:
            await interaction.response.send_message(
                "You need to specify an amount equal or greater than 1",
                ephemeral = True
            )
            return

        if amount <= 0:
            await interaction.response.send_message(
                "You need to specify an amount equal or greater than 1",
                ephemeral = True
            )
            return

        balance = wallet, bank = await tabby.get_bal(interaction.user)
        if amount > wallet:
            await interaction.response.send_message(
                "The amount to deposit can't be bigger than the one you have in your wallet",
                ephemeral = True
            )
            return

        await tabby.add_money(interaction.user, (amount, 0))

        embed = discord.Embed()



async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))