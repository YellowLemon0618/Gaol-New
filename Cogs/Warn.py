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

guild_ids = [827445316218257408, 891315672418750525]


# await interaction.response.defer()
class Check(discord.ui.Button):
    def __init__(self, btn_name: str, btn_id: str):
        super().__init__(
            label=btn_name,
            style=discord.ButtonStyle.primary,
            custom_id=btn_id
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            btn_type = self.custom_id.split('_')[0]
            page = int(self.custom_id.split('_')[-1].split('/')[0])
            whole = int(self.custom_id.split('_')[-1].split('/')[1])
            user = interaction.guild.get_member(int(self.custom_id.split('_')[-2]))

            if (btn_type == "prv" and page <= 1) or (btn_type == "nxt" and page >= whole):
                return

            conn = pymysql.connect(host='localhost', user='root', password='Mysql_0618^&', db='py', charset='utf8')
            cur = conn.cursor()

            sql = f"SELECT * FROM `warning` WHERE user = {user.id}"
            cur.execute(sql)
            res = cur.fetchall()

            embed = discord.Embed(title=f"{user.name}#{user.discriminator} 's Warning List", color=0xFF0000)
            view = discord.ui.View(timeout=None)

            if btn_type == "prv":
                bywho = interaction.guild.get_member(int(res[page - 2][2]))

                embed.title = f"{embed.title} ( {page - 1} / {len(res)} )"
                embed.add_field(name="**By**",
                                value=f"{bywho.mention} ( {bywho.name}#{bywho.discriminator} / {bywho.id} )",
                                inline=False)
                embed.add_field(name="**Why**", value=f"{res[page - 2][5]}", inline=True)
                embed.add_field(name="**When**", value=f"{res[page - 2][3]}", inline=True)
                embed.add_field(name=" ", value=" ", inline=True)
                embed.add_field(name="**Count**", value=f"{res[page - 2][4]}", inline=True)
                embed.add_field(name="**Total Warning**", value=f"{res[-1][6]}", inline=True)
                embed.add_field(name=" ", value=" ", inline=True)

                view.add_item(Check("Previous", f"prv_{user.id}_{page - 1}/{len(res)}"))
                view.add_item(Check("Next", f"nxt_{user.id}_{page - 1}/{len(res)}"))
            elif btn_type == "nxt":
                bywho = interaction.guild.get_member(int(res[page][2]))

                embed.title = f"{embed.title} ( {page + 1} / {len(res)} )"
                embed.add_field(name="**By**",
                                value=f"{bywho.mention} ( {bywho.name}#{bywho.discriminator} / {bywho.id} )",
                                inline=False)
                embed.add_field(name="**Why**", value=f"{res[page][5]}", inline=True)
                embed.add_field(name="**When**", value=f"{res[page][3]}", inline=True)
                embed.add_field(name=" ", value=" ", inline=True)
                embed.add_field(name="**Count**", value=f"{res[page][4]}", inline=True)
                embed.add_field(name="**Total Warning**", value=f"{res[-1][6]}", inline=True)
                embed.add_field(name=" ", value=" ", inline=True)

                view.add_item(Check("Previous", f"prv_{user.id}_{page + 1}/{len(res)}"))
                view.add_item(Check("Next", f"nxt_{user.id}_{page + 1}/{len(res)}"))

            await interaction.response.edit_message(embed=embed, view=view)

            conn.commit()
            conn.close()
        except:
            print("failed")


class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.application_command(name="warn", cls=discord.SlashCommand)

    @slash_command(name='경고부여', description="Give warning to user", guild_ids=guild_ids)
    @option('user', discord.Member, description="Enter the user")
    @option('count', float, description="Enter the number how much warning to give")
    @option('reason', str, description="Enter the reason")
    async def warn(self, ctx: ApplicationContext, user: discord.Member, count: int, *, reason: str):
        now = datetime.datetime.now()

        try:
            conn = pymysql.connect(host='localhost', user='root', password='Mysql_0618^&', db='py', charset='utf8')
            cur = conn.cursor()

            sql = f"SELECT count(*) FROM `warning`;"
            cur.execute(sql)
            rownum = cur.fetchone()

            sql = f"select * from `warning` where id in (select max(id) from warning where user = {user.id});"
            cur.execute(sql)
            res = cur.fetchone()
            if res is None:
                total = count
            else:
                total = res[6] + count
            total = round(total, 2)

            sql = f"INSERT INTO `warning` VALUES ({int(rownum[0]) + 1}, '{user.id}', '{ctx.author.id}', '{now.year}-{now.month}-{now.day}', {count}, '{reason}', {total}); "
            cur.execute(sql)

            embed = discord.Embed(title=f"**{user.name}#{user.discriminator} has been warned.**", color=0xFF0000)
            embed.add_field(name="**User**", value=f"{user.mention} ( {user.name}#{user.discriminator} / {user.id} )",
                            inline=False)
            embed.add_field(name="**By**",
                            value=f"{ctx.author.mention} ( {ctx.author.name}#{ctx.author.discriminator} / {ctx.author.id} )",
                            inline=False)
            embed.add_field(name="**Why**", value=f"{reason}", inline=True)
            embed.add_field(name="**When**", value=f"{now.year}-{now.month}-{now.day}", inline=True)
            embed.add_field(name=" ", value=" ", inline=True)
            embed.add_field(name="**Count**", value=f"{count}", inline=True)
            embed.add_field(name="**Total Warning**", value=f"{total}", inline=True)
            embed.add_field(name=" ", value=" ", inline=True)
            embed.set_footer(icon_url=self.bot.user.avatar.url,
                             text=f"Gaol#8640 | {now.year}-{now.month}-{now.day} • {now.hour} : {now.minute} : {now.second}")
            await ctx.respond(embed=embed)

            conn.commit()
            conn.close()

        except:
            print("failed")

        return

    @slash_command(name='경고조회', description="Check warning(s)", guild_ids=guild_ids)
    @option('user', discord.Member, description="Enter the user")
    async def check(self, ctx: ApplicationContext, user: str):
        now = datetime.datetime.now()

        try:
            conn = pymysql.connect(host='localhost', user='root', password='Mysql_0618^&', db='py', charset='utf8')
            cur = conn.cursor()

            sql = f"SELECT count(*) FROM `warning`;"
            cur.execute(sql)
            rownum = cur.fetchone()

            sql = f"SELECT * FROM `warning` WHERE user = {user.id}"
            cur.execute(sql)
            res = cur.fetchall()

            embed = discord.Embed(title=f"test {user.name}#{user.discriminator} 's Warning List", color=0xFF0000)
            if not res:
                embed.add_field(name="**This user has no warning history.**", value="** **", inline=False)
                view = None
            else:
                bywho = ctx.guild.get_member(int(res[0][2]))

                embed.title = f"{embed.title} ( 1 / {len(res)} )"
                embed.add_field(name="**By**",
                                value=f"{bywho.mention} ( {bywho.name}#{bywho.discriminator} / {bywho.id} )",
                                inline=False)
                embed.add_field(name="**Why**", value=f"{res[0][5]}", inline=True)
                embed.add_field(name="**When**", value=f"{res[0][3]}", inline=True)
                embed.add_field(name=" ", value=" ", inline=True)
                embed.add_field(name="**Count**", value=f"{res[0][4]}", inline=True)
                embed.add_field(name="**Total Warning**", value=f"{res[-1][6]}", inline=True)
                embed.add_field(name=" ", value=" ", inline=True)
                view = discord.ui.View(timeout=None)
                view.add_item(Check("Previous", f"prv_{user.id}_1/{len(res)}"))
                view.add_item(Check("Next", f"nxt_{user.id}_1/{len(res)}"))

            await ctx.respond(embed=embed, view=view)

            conn.commit()
            conn.close()

        except:
            print("failed")

        return


def setup(bot):
    bot.add_cog(Warn(bot))
