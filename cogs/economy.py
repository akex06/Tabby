import discord

from discord import app_commands, ui
from discord.ext import commands
from src.tabby import Tabby

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
    @commands.guild_only()
    async def deposit(
        self,
        interaction: discord.Interaction,
        amount: int = None
    ) -> None:
        if not amount or amount <= 0:
            await interaction.response.send_message(
                "You need to specify an amount equal or greater than 1",
                ephemeral = True
            )
            return

        balance = await tabby.get_bal(interaction.user)
        if amount > int(balance[0]):
            await interaction.response.send_message(
                "The amount to deposit can't be bigger than your wallet balance",
                ephemeral = True
            )
            return

        balance = await tabby.add_money(interaction.user, (amount, -amount))

        await interaction.response.send_message("")

    @app_commands.command(
        name = "withdraw",
        description = "Withdraw money from your bank"
    )
    @commands.guild_only()
    async def withdraw(
        self,
        interaction: discord.Interaction,
        amount: int = None
    ) -> None:
        if not amount or amount <= 0:
            interaction.response.send_message(
                "You need to specify an amount equal or greater than 1",
                ephemeral = True
            )
            return
        
        bank = tabby.get_bal(interaction.user)[1]
        if amount > bank:
            await interaction.response.send_message(
                "The amount to withdraw can't be bigger than your bank balance"
            )
            return

    @app_commands.command(
        name = "addmoney",
        description = "Add money to a member"
    )
    async def addmoney(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None,
        action: str = None,
        amount: int = None
    ) -> None:
        if await tabby.isadmin(interaction):
            if not amount or amount <= 0:
                await interaction.response.send_message(
                    "The amount needs to be greater or equal to 0",
                    ephemeral = True
                )
                return
            if not action or action.lower() not in ("add", "remove"):
                await interaction.response.send_message(
                    "You need to specify an action (add / remove).",
                    ephemeral = True
                )
                return

            if not member:
                member = interaction.user

            if action == "add":
                
                await tabby.add_money(member, (amount, 0))
                
                await interaction.response.send_message(
                    f"You've added `{amount}` to {member}'s balance",
                    ephemeral = True
                )
            
            else:
                await tabby.add_money(member, (-amount, 0))

                await interaction.response.send_message(
                    f"You've removed `{amount}` from {member}'s balance",
                    ephemeral = True
                )

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))