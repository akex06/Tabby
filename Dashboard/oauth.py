import requests

from constants import (
    TOKEN,
    SECRET
)

class Oauth:
    client_id = "868470190499827762"
    client_secret = SECRET
    redirect_uri = "http://127.0.0.1:5000/dashboard"
    scope = "identify%20email%20guilds"
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=868470190499827762&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fdashboard&response_type=code&scope=identify%20email%20guilds"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"
    invite = "https://discord.com/oauth2/authorize?client_id=868470190499827762&permissions=1102132341878&scope=bot%20applications.commands"
    bot_token = TOKEN

    @staticmethod
    def get_access_token(code):
        payload = {
            "client_id": Oauth.client_id,
            "client_secret": Oauth.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Oauth.redirect_uri,
            "scope": Oauth.scope
        }

        access_token = requests.post(url = Oauth.discord_token_url, data = payload).json()
        return access_token["access_token"]

    @staticmethod
    def get_user_json(access_token):
        url = f"{Oauth.discord_api_url}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_object = requests.get(url, headers = headers).json()
        return user_object

    @staticmethod
    def get_guilds(guilds):
        url = f"{Oauth.discord_api_url}/users/@me/guilds"
        headers = {"Authorization": f"Bot {Oauth.bot_token}"}

        bot_guilds = requests.get(url, headers = headers).json()
        bot_guild_ids = [guild["id"] for guild in bot_guilds]

        for guild in guilds:
            if guild["id"] in bot_guild_ids:
                guild["shared"] = "shared-green"
                guild["url"] = f"https://tabbybot.xyz/dashboard/{guild['id']}"
                

            else:
                guild["shared"] = "shared-red"
                guild["url"] = f"{Oauth.invite}&guild_id={guild['id']}"

        return guilds

    @staticmethod
    def get_user_guilds(access_token):
        url = f"{Oauth.discord_api_url}/users/@me/guilds"
        headers = {"Authorization": f"Bearer {access_token}"}

        raw_guilds = requests.get(url, headers = headers).json()
        
        guilds = []
        for guild in raw_guilds:
            if guild["permissions"] & 0x8 == 8:
                data = {"id": guild["id"], "name": guild["name"]}

                if guild["icon"]:
                    data["icon"] = f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}"

                else:
                    data["icon"] = "https://external-preview.redd.it/4PE-nlL_PdMD5PrFNLnjurHQ1QKPnCvg368LTDnfM-M.png?auto=webp&s=ff4c3fbc1cce1a1856cff36b5d2a40a6d02cc1c3"

                guilds.append(data)
        
        guilds = Oauth.get_guilds(guilds)
        return guilds

    @staticmethod
    def get_guild_amount():
        url = f"{Oauth.discord_api_url}/users/@me/guilds"
        headers = {"Authorization": f"Bot {Oauth.bot_token}"}

        guild_amount = len(requests.get(url, headers = headers).json())
        return guild_amount

    @staticmethod
    def get_user_amount():
        url = f"{Oauth.discord_api_url}/users/@me/users"
        headers = {"Authorization": f"Bot {Oauth.bot_token}"}

        user_amount = requests.get(url, headers = headers).json()
        return user_amount

import discord

discord.Client.users