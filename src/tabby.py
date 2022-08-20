import discord
import mysql.connector
import random

from random import randint
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

    async def get_economy_leaderboard(self, guild: discord.Guild, max = 10) -> list:
        c.execute("SELECT id, wallet, bank FROM economy WHERE guild = %s ORDER BY wallet + bank DESC LIMIT %s", (guild.id, max))
        result = c.fetchall()

        return result

    async def get_level(self, member: discord.Member):
        c.execute("SELECT level, exp FROM levels WHERE id = %s AND guild = %s", (member.id, member.guild.id))
        result = c.fetchone()

        if not result:
            c.execute("INSERT INTO levels (id, guild, level, exp) VALUES (%s, %s, 0, 0)", (member.id, member.guild.id))
            conn.commit()

            return (0, 0)

        return result

    #   IF MEMBER LEVEL UPS RETURS TRUE ELSE FALSE
    async def add_exp(self, member: discord.Member) -> bool:
        level, exp = tuple(map(int, await self.get_level(member)))
        exp += random.randint(15, 25)

        needed_exp = 5 * (level ** 2) + (50 * level) + 100 - exp
        if needed_exp <= 0:
            exp = abs(needed_exp)
            c.execute("UPDATE levels SET level = level + 1, exp = %s WHERE id = %s AND guild = %s", (exp, member.id, member.guild.id))
            conn.commit()
            return True

        c.execute("UPDATE levels SET exp = %s WHERE id = %s AND guild = %s", (exp, member.id, member.guild.id))
        conn.commit()

        return False

    async def get_level_leaderboard(self, guild: discord.Guild, max = 10):
        c.execute("SELECT id, level, exp FROM levels WHERE guild = %s ORDER BY level DESC LIMIT %s", (guild.id, max))
        result = c.fetchall()
        return result