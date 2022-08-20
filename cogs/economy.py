import discord

from discord.ext import commands
from discord.ui import View, Button
from src.tabby import Tabby

from src.constants import (
    MAX_ICON_LENGTH,
    HEXCOLOR
)

tabby = Tabby()

class Reset(discord.ui.View):
    def __init__(self):
        super().__init__()

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

        await tabby.reset_economy(interaction.guild)
        await interaction.response.send_message(
            "The economy of the server has been reset",
            ephemeral = True
        )

class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "bal",
        description = "Check's an user balance"
    )
    @commands.guild_only()
    async def balance(
        self,
        ctx: commands.Context,
        member: discord.Member = None
    ) -> None:
        if not member:
            member = ctx.author
        
        elif member.bot:
            await ctx.reply(
                "You can't use this command on a bot",
                ephemeral = True
            )
            return
                

        wallet, bank = await tabby.get_bal(member)

        embed = discord.Embed(description = f"{member.name} is top x in economy leaderboard", color = HEXCOLOR)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name = "Wallet", value = wallet)
        embed.add_field(name = "Bank", value = bank)

        await ctx.reply(embed = embed)

    @commands.hybrid_command(
        name = "deposit",
        description = "Deposit money into your bank",
        with_app_command = True
    )
    @commands.guild_only()
    async def deposit(
        self,
        ctx: commands.Context,
        amount: int
    ) -> None:
        if amount <= 0:
            await ctx.reply(
                "You need to specify an amount equal or greater than 1",
                ephemeral = True
            )
            return

        balance = await tabby.get_bal(ctx.author)
        if amount > int(balance[0]):
            await ctx.reply(
                "The amount to deposit can't be bigger than your wallet balance",
                ephemeral = True
            )
            return

        await tabby.add_money(ctx.author, (-amount, amount))

        await ctx.reply(f"You've deposited `{amount}$`")

    @commands.hybrid_command(
        name = "withdraw",
        description = "Withdraw money from your bank",
        with_app_command = True
    )
    @commands.guild_only()
    async def withdraw(
        self,
        ctx: commands.Context,
        amount: int
    ) -> None:
        if amount <= 0:
            await ctx.reply(
                "You need to specify an amount equal or greater than 1",
                ephemeral = True
            )
            return

        balance = await tabby.get_bal(ctx.author)
        if amount > int(balance[0]):
            await ctx.reply(
                "The amount to withdraw can't be bigger than your bank balance",
                ephemeral = True
            )
            return

        await tabby.add_money(ctx.author, (amount, -amount))

        await ctx.reply(f"You've withdrawed `{amount}$`")


    @commands.hybrid_command(
        name = "addmoney",
        description = "Add money to a member",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def addmoney(
        self,
        ctx: commands.Context,
        member: discord.Member,
        amount: int
    ) -> None:
        
        if member.bot:
            await ctx.reply(
                "You can't use this command on a bot",
                ephemeral = True
            )
            
        if amount <= 0:
            await ctx.reply(
                "The amount needs to be greater or equal to 0",
                ephemeral = True
            )
            return
        
        await tabby.add_money(member, (0, amount))
        
        await ctx.reply(
            f"You've added `{amount}` to {member}'s balance",
            ephemeral = True
        )

    @commands.hybrid_command(
        name = "removemoney",
        description = "Add money to a member",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def removemoney(
        self,
        ctx: commands.Context,
        member: discord.Member,
        amount: int
    ) -> None:
        if member.bot:
            await ctx.reply(
                "You can't use this command on a bot",
                ephemeral = True
            )
            
        if amount <= 0:
            await ctx.reply(
                "The amount needs to be greater or equal to 0",
                ephemeral = True
            )
            return

        await tabby.add_money(member, (0, -amount))

        await ctx.reply(
            f"You've removed `{amount}` from {member}'s balance",
            ephemeral = True
        )

    @commands.hybrid_command(
        name = "addmoneyrole",
        description = "Add money to all members in a role",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def addmoneyrole(
        self,
        ctx: commands.Context,
        role: discord.Role,
        amount: int
    ) -> None:
        if amount <= 0:
            await ctx.reply(
                "The amount to give needs to be equal or greater than 1",
                ephemeral = True
            )
            return

        for member in role.members:
            if not member.bot:
                await tabby.add_money(member, (0, amount))

        await ctx.reply(f"Total amount given {len(role.members) * amount}")

    @commands.hybrid_command(
        name = "removemoneyrole",
        description = "Remove money from all members in a role",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def removemoneyrole(
        self,
        ctx: commands.Context,
        role: discord.Role,
        amount: int
    ) -> None:
        if amount <= 0:
            await ctx.reply(
                "The amount to give needs to be equal or greater than 1",
                ephemeral = True
            )
            return

        for member in role.members:
            if not member.bot:
                await tabby.add_money(member, (0, -amount))

        await ctx.reply(f"Total amount removed {len(role.members) * amount}")

    @commands.hybrid_command(
        name = "reset-economy",
        description = "Reset the server's economy",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def reset_economy(
        self,
        ctx: commands.Context
    ) -> None:
        view = Reset()

        embed = discord .Embed(description = "Are you sure you want to reset the economy?", color = HEXCOLOR)
        embed.set_author(name = "Economy reset", icon_url = self.bot.user.avatar.url)
        
        await ctx.reply(
            view = view,
            embed = embed,
            ephemeral = True
        )

    @commands.hybrid_command(
        name = "give",
        description = "Give money to other members",
        with_app_command = True
    )
    @commands.guild_only()
    async def give(
        self,
        ctx: commands.Context,
        member: discord.Member,
        amount: int
    ) -> None:
        if member.bot:
            await ctx.reply(
                "You can't use this command on a bot",
                ephemeral = True
            )
            return

        elif member == ctx.author:
            await ctx.reply(
                "You can't give money to yourself",
                ephemeral = True
            )

        elif amount <= 0:
            await ctx.reply(
                "You need to specify an amount equal or higher than 1",
                ephemeral = True
            )
            return

        balance = await tabby.get_bal(ctx.author)

        if amount > int(balance[1]):
            await ctx.reply(
                "You don't have enough money in your bank",
                ephemeral = True
            )
            return

        await tabby.add_money(member, (0, amount))
        await tabby.add_money(ctx.author, (0, -amount))

        await ctx.reply(f"You gave {member} `{amount}`$")
        
    @commands.hybrid_command(
        name = "reset-bal",
        with_app_command = True,
        description = "Reset the balance of a member"
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def reset_bal(
        self,
        ctx: commands.Context,
        member: discord.Member
    ) -> None:
        wallet, bank = await tabby.get_bal(member)
        await tabby.reset_bal(member)

        await ctx.reply(
            f"Old Balance `Wallet: {wallet}` `Bank: {bank}` >>> New Balance `Wallet: 100` `Bank: 0`",
            ephemeral = True
        )

    @commands.hybrid_command(
        name = "set-currency",
        description = "Set the currency icon",
        with_app_command = True
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def set_currency(
        self,
        ctx: commands.Context,
        icon: str = None
    ) -> None:
        if not icon:
            icon = await tabby.get_icon(ctx.guild)

            await ctx.reply(f"The server's currency icon is `{icon}`")
            return

        if len(icon) > MAX_ICON_LENGTH:
            await ctx.reply(
                f"The length of the icon can't be bigger than {MAX_ICON_LENGTH}",
                ephemeral = True
            )
            return

        await tabby.set_icon(ctx.guild, icon)
        await ctx.reply(f"The new currency icon is `{icon}`")

    @commands.hybrid_command(
        name = "leaderboard",
        description = "Check the economy leaderboard",
        with_app_command = True
    )
    @commands.guild_only()
    async def leaderboard(
        self,
        ctx: commands.Context
    ) -> None:
        leaderboard = await tabby.get_economy_leaderboard(ctx.guild)

        embed = discord.Embed(description = f"Top 10 economy leaderboard in the server, check the whole leaderboard [here](https://tabbybot.xyz/leaderboard/economy/{ctx.guild.id}))", color = HEXCOLOR)
        embed.set_author(name = f"{ctx.guild.name} economy leaderboard", icon_url = ctx.guild.icon.url)
        
        for i in leaderboard:
            member = ctx.guild.get_member(int(i[0]))

            embed.add_field(
                name = member.name,
                value = f"```Total: {i[1] + i[2]}\nWallet: {i[1]}\nBank: {i[2]}```",
                inline = False
            )

        button = Button(label = "See full leaderboard", emoji = "🔗", url = f"https://tabbybot.xyz/leaderboard/economy/{ctx.guild.id}")
        view = View()
        view.add_item(button)

        await ctx.reply(view = view, embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))