import pymysql
import cryptography
import asyncio
from typing import Union
import discord
from discord import slash_command, option, ApplicationContext
from discord.ext import commands
import datetime
import random
from math import *
import os
from dotenv import load_dotenv

guild_ids = [827445316218257408, 891315672418750525]
load_dotenv()
db_pw = os.getenv("DB_PW")


# await interaction.response.defer()
class Check(discord.ui.Button):
    def __init__(self, btn_name: str, btn_id: str, color: discord.Button.style):
        super().__init__(
            label=btn_name,
            style=color,
            custom_id=btn_id
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            if self.custom_id.split(' - ')[0] == "No":
                await interaction.message.delete()
            elif self.custom_id.split(' - ')[0] == "Yes":
                user = interaction.guild.get_member(int(self.custom_id.split(' - ')[1]))
                embed = discord.Embed(title="정말로 해당 유저를 밴 하겠습니까?",
                                      description=f"**{user.name}#{user.discriminator} / {user.id}** 유저가 밴 처리 되었습니다.")
                await interaction.message.edit(embed=embed, view=None)
                await user.ban(reason=interaction.message.embeds[0].fields[2].name)

            await interaction.response.defer()

        except:
            await interaction.response.defer()
            print("failed")


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @slash_command(name='ban', description="Ban user", guild_ids=guild_ids)
    @option('user', discord.Member, description="Enter the user")
    @option('reason', str, description="Enter the reason")
    async def ban(self, ctx: ApplicationContext, user: discord.Member, *, reason: str):
        now = datetime.datetime.now()

        try:
            embed = discord.Embed(title="정말로 해당 유저를 밴 하겠습니까?", color=0xFF0000)
            embed.add_field(name=" ", value=" ")
            embed.add_field(name=f"**{user.name}#{user.discriminator} / {user.id}**",
                            value="밴 하려는 유저가 맞는지 확인 해주세요.", inline=False)
            embed.add_field(name=f"Reason", value=f"{reason}", inline=False)
            view = discord.ui.View(timeout=None)
            view.add_item(Check("아니오", f"No", color=discord.ButtonStyle.danger))
            view.add_item(Check("예", f"Yes - {user.id}", color=discord.ButtonStyle.green))

            await ctx.respond(embed=embed, view=view)

        except:
            print("failed")

        return


def setup(bot):
    bot.add_cog(Ban(bot))
