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
    print("===========================")
    print("Logged in as: ")
    print(bot.user.name)
    print(bot.user.id)
    print("===========================")
    game = discord.Game("TEST")
    await bot.change_presence(status=discord.Status.online, activity=game)


for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Missing Permission",
                              description="봇에게 해당 명령을 실행할 권한이 없습니다.",
                              color=0xFF0000)
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.CommandError):
        return


bot.run(token)
