import discord
import mysql.connector

from discord.ext import commands
from mysql.connector.connection import MySQLConnection

conn: MySQLConnection = mysql.connector.connect(
    host="panel.f4ke.ml",
    user="u4_6D7b3sikkH",
    password="Yex8xXK@JXih.KfGdyPpKE^N",
    database="s4_tabby"
)
c = conn.cursor(buffered=True)

class Tabby:
    hexcolor = 0xffe100

    async def check_bal(self, member: discord.Member) -> None:
        c.execute("SELECT id FROM economy WHERE id = %s", (member.id, ))
        if not c.fetchone():
            c.execute("INSERT INTO economy (id, guild, wallet, bank) VALUES (%s, %s, 100, 0)", (member.id, member.guild.id))
            conn.commit()

    async def get_bal(self, member: discord.Member) -> tuple:
        await self.check_bal(member)

        c.execute("SELECT wallet, bank FROM economy WHERE id = %s AND guild = %s", (member.id, member.guild.id))
        return c.fetchone()

    async def add_money(self, member: discord.Member, amount: tuple) -> tuple:
        await self.check_bal(member)
        c.execute(
            "UPDATE economy SET wallet = wallet + %s, bank = bank + %s WHERE id = %s AND guild = %s",
            (amount[0], amount[1], member.id, member.guild.id)
        )
        conn.commit()
        
        return await self.get_bal(member)

    async def isadmin(self, interaction: discord.Interaction):
        permission = interaction.user.guild_permissions.administrator

        if permission:
            return permission

        await interaction.response.send_message(
            "You don't have permissions for using this command",
            ephemeral = True
        )