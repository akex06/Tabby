import discord

from discord import app_commands
from discord.ext import commands
from src.tabby import Tabby

tabby = Tabby()

class Reset(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(
        label = "Reset economy",
        style = discord.ButtonStyle.danger,
        emoji = "⛔"
    )
    async def menu1(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:

        await tabby.reset(interaction.guild)
        await interaction.response.send_message(
            "The economy of the server has been reset",
            ephemeral = True
        )

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
                
                await tabby.add_money(member, (0, amount))
                
                await interaction.response.send_message(
                    f"You've added `{amount}` to {member}'s balance",
                    ephemeral = True
                )
            
            else:
                await tabby.add_money(member, (0, -amount))

                await interaction.response.send_message(
                    f"You've removed `{amount}` from {member}'s balance",
                    ephemeral = True
                )

    @app_commands.command(
        name = "addmoneyrole",
        description = "Add money to all members in a role"
    )
    async def addmoneyrole(
        self,
        interaction: discord.Interaction,
        role: discord.Role = None,
        amount: int = None
    ) -> None:
        if await tabby.isadmin(interaction):
            if amount <= 0:
                await interaction.response.send_message(
                    "The amount to give needs to be equal or greater than 1",
                    ephemeral = True
                )
                return

            if not role:
                await interaction.response.send_message(
                    "You need to specify a role",
                    ephemeral = True
                )
                return
            
            if not amount:
                await interaction.response.send_message(
                    "You need to specify an amount to give",
                    ephemeral = True
                )
                return

            for member in role.members:
                await tabby.add_money(member, (0, amount))

            await interaction.response.send_message(
                f"Total amount given {len(role.members) * amount}",
                ephemeral = True
            )

    @app_commands.command(
        name = "removemoneyrole",
        description = "Remove money from all members in a role"
    )
    async def removemoneyrole(
        self,
        interaction: discord.Interaction,
        role: discord.Role = None,
        amount: int = None
    ) -> None:
        if await tabby.isadmin(interaction):
            if amount <= 0:
                await interaction.response.send_message(
                    "The amount to give needs to be equal or greater than 1",
                    ephemeral = True
                )
                return
            if not role:
                await interaction.response.send_message(
                    "You need to specify a role",
                    ephemeral = True
                )
                return
            
            if not amount:
                await interaction.response.send_message(
                    "You need to specify an amount to give",
                    ephemeral = True
                )
                return

            for member in role.members:
                await tabby.add_money(member, (0, -amount))

            await interaction.response.send_message(
                f"Total amount removed {len(role.members) * amount}",
                ephemeral = True
            )

    @app_commands.command(
        name = "reset-economy",
        description = "Reset the server's economy"
    )
    async def reset_economy(
        self,
        interaction: discord.Interaction
    ) -> None:
        if tabby.isadmin(interaction.user):
            view = Reset()

            embed = discord.Embed(title = "Economy reset", description = "Are you sure you want to reset the economy?", color = tabby.hexcolor)
            embed.set_author(name = "Economy reset", icon_url = self.bot.user.avatar.url)
            
            await interaction.response.send_message(
                view = view,
                embed = embed,
                ephemeral = True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))