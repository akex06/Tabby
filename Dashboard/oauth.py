import requests

class Oauth:
    client_id = "868470190499827762"
    client_secret = "VDFz7-20-QgisLUcWjZjuLfgjTNIyk-C"
    redirect_uri = "http://127.0.0.1:5000/login"
    scope = "identify%20email%20guilds"
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=868470190499827762&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin&response_type=code&scope=identify%20email%20guilds"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"
    bot_token = "ODY4NDcwMTkwNDk5ODI3NzYy.GYVwc4.olvoPGuN2YH9ifqUCE_lVN2E-o74lY6w_xuEGA"

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
                guild["shared"] = True

            else:
                guild["shared"] = False

        return guilds

    @staticmethod
    def get_user_guilds(access_token):
        url = f"{Oauth.discord_api_url}/users/@me/guilds"
        headers = {"Authorization": f"Bearer {access_token}"}

        raw_guilds = requests.get(url, headers = headers).json()
        
        guilds = []
        for guild in raw_guilds:
            if guild["permissions"] & 0x8 == 8:
                data = {"id": guild["id"], "name": guild["name"], "icon": f"https://cdn.discordapp/icons/{guild['id']}/{guild['icon']}.png"}
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