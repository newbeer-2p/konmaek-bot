import discord
from discord.ext import commands
from settings import *

class Find(commands.Cog, name="Find"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def find(self, ctx, cmd, *, attr):
        find = False
        if cmd in ["channel", "ch"]:
            embed = discord.Embed(
                title="ผลการค้นหา Channel: ",
                color=colorTheme
            )
            for ch in ctx.guild.channels:
                if attr in ch.name:
                    find = True
                    embed.add_field(name="Channel: ", value=f"{ch.mention}", inline=False)
        else:
            embed = discord.Embed(
                description="Find",
                color=colorTheme
            )

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Find(bot))