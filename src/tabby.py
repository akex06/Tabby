from tkinter import E
import discord
import mysql.connector

from discord.ext import commands
from mysql.connector.connection import MySQLConnection

from src.constants import (
    DEFAULT_ICON
)

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

    async def reset_economy(self, guild: discord.Guild) -> None:
        c.execute("DELETE FROM economy WHERE guild = %s", (guild.id, ))
        conn.commit()

    async def reset_bal(self, member: discord.Member):
        c.execute("UPDATE economy SET wallet = 100, bank = 0 WHERE id = %s AND guild = %s", (member.id, member.guild.id))
        conn.commit()

    async def get_icon(self, guild: discord.Guild):
        c.execute("SELECT icon FROM currency WHERE guild = %s", (guild.id, ))
        result = c.fetchone()

        if not result:
            c.execute("INSERT INTO currency (guild, icon) VALUES (%s, %s)", (guild.id, DEFAULT_ICON))
            conn.commit()

            return DEFAULT_ICON
        
        else:
            return result[0]

    async def set_icon(self, guild: discord.Guild, icon: str) -> None:
        await self.get_icon(guild)

        c.execute("UPDATE currency SET icon = %s WHERE guild = %s", (icon, guild.id))
        conn.commit()