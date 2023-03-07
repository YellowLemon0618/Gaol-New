import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
# intents.members = True
# intents.presences = True
bot = commands.Bot(intents=intents)
bot.remove_command('help')

load_dotenv()
token = os.getenv("TOKEN")


@bot.event
async def on_ready():
    print("============================")
    print("Logged in as: ")
    print(bot.user.name)
    print(bot.user.id)
    print("============================")
    game = discord.Game("TEST")
    await bot.change_presence(status=discord.Status.online, activity=game)


for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.MissingPermissions):
        return


bot.run(token)
