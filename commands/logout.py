import discord
from discord.ext import commands
from settings import *
from modules import *

class Logout(commands.Cog, name="Logout"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def logout(self, ctx):
        embed = discord.Embed(
            title="บ๊ายบายยยย เจอกันใหม่นะ",
            description="☁ ก้อนเมฆ ยินดีรับใช้บริการ ☁",
            color=themeColor
        )

        await ctx.channel.send(embed=embed)
        await self.bot.logout()

def setup(bot: commands.Bot):
    bot.add_cog(Logout(bot))