from dhooks import *
import requests
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands
import discord


client = commands.Bot(command_prefix='.')
icon = "https://cdn.discordapp.com/attachments/799962707377127444/960562092556030072/unknown.png"


@client.event
async def on_ready():
    datetime_object = datetime.now()
    datetime_real = str(datetime_object)
    print(datetime_real + " - CryptoScraper is live.")
    await client.change_presence(activity=discord.Game(name="Checking $DOGE", icon=icon))


@client.command(pass_context=True)
async def check(ctx, crypto):
    s = requests.Session()

    link = f'https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-product-by-symbol?symbol={crypto}USDT'

    r = s.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    text = str(soup)

    current_price = text.split('"c":"')[1].split('",')[0]
    today_high = text.split('"h":"')[1].split('",')[0]
    today_low = text.split('"l":"')[1].split('",')[0]
    today_volume = text.split('"v":"')[1].split('",')[0]

    now = just_date()
    embed = discord.Embed(title=f"Crypto checker: {crypto} to USDT", url=f"https://www.binance.com/en"
                          f"/trade/{crypto}_USDT?theme=dark&type=spot", color=0x202020)
    embed.add_field(name="Current price", value=f"${current_price}")
    embed.add_field(name="Today high", value=f"${today_high}")
    embed.add_field(name="Today low", value=f"${today_low}")
    embed.add_field(name=f"Today volume ({crypto})", value=f"{today_volume}")
    embed.set_footer(text=f"{now} • powered by @nicko",
                     icon_url="https://cdn.discordapp.com/attachments/799962707377127444/9909842"
                              "01664888912/bartFoto.PNG")
    await ctx.message.channel.send(embed=embed)
    datetime_object = datetime.now()
    datetime_real = str(datetime_object)
    print(datetime_real + " - Crypto update sent!")


client.run("DISCORD_BOT_TOKEN_HERE")
