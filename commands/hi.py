import discord
from discord.ext import commands
import random
from settings import *

class Hi(commands.Cog, name="Hi"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def hi(self, ctx):
        text = [
            "สวัสดีจร้าาา มีอะไรให้ช่วยหรือเปล่า",
            "ฮายยย! วันนี้สบายดีมั้ย",
            "อัลโหลๆ มีใครอยู่ม้ายยย",
            "ฮายกะเทยยยยยยยย",
            "Hello! My name is Konmaek!"
        ]
        
        embed = discord.Embed(
            description=random.choice(text),
            color=colorTheme
        )

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Hi(bot))