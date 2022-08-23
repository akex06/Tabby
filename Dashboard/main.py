from re import S
from flask import Flask, render_template, request, session, redirect
from oauth import Oauth

app = Flask(__name__)
app.config["SECRET_KEY"] = "test123"

failed = {"code": 0, "message": "401: Unauthorized"}

@app.route("/")
def home():
    guild_amount = Oauth.get_guild_amount()

    return render_template("index.html", guild_amount=guild_amount)

@app.route("/dashboard")
@app.route("/login")
def login():
    at = session.get(request.remote_addr)
    user = Oauth.get_user_json(at)

    if user == failed:
        code = request.args.get("code")
        if code:
            at = Oauth.get_access_token(code)
            user = Oauth.get_user_json(at)
            
            if user == failed:
                return redirect(Oauth.discord_login_url)

            else:
                session[request.remote_addr] = at

        elif not code:
            return redirect(Oauth.discord_login_url)

    name = f"{user['username']}#{user['discriminator']}"
    guilds = Oauth.get_user_guilds(at)

    return render_template("dashboard.html", name = name, guilds = guilds)

if __name__ == "__main__":
    app.run(debug = True)