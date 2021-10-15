import discord
from discord.ext import commands
import random
from settings import *

class CheerUp(commands.Cog, name="CheerUp"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def cheerup(self, ctx):
        text = [
            "ไม่เป็นไรน้าาาาา เค้าอยู่ข้างเธอเสมอ 🥰",
            "เธอเก่งแล้วววววว 😁",
            "สู้ๆน้าาาา เค้าเป็นกำลังใจให้นะ ❤"
        ]
        embed = discord.Embed(
            description=random.choice(text),
            color=colorTheme
        )
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(CheerUp(bot))