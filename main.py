import os
import pathlib
import datetime as dt
from discord.ext import commands

BOT_PREFIX = '!'

with open(pathlib.Path('token.txt'), 'r') as file:
    token = file.read()
    
bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)


for cog in os.listdir(pathlib.Path('./cogs')):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded:")
            raise e


@bot.event
async def on_ready():
    log_in = f'Logged in as {bot.user.name}'
    print(log_in)
    print(bot.user.id)
    print(dt.datetime.now())
    print("-" * len(log_in))

bot.run(token)
