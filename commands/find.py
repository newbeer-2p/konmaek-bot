import discord
from discord.ext import commands
from settings import *

class Find(commands.Cog, name="Find"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def find(self, ctx, cmd, *, attr):
        if cmd in ["channel", "ch"]:
            embed = discord.Embed(
                title="ผลการค้นหา Channel: ",
                color=themeColor
            )
            for ch in ctx.guild.channels:
                if attr in ch.name:
                    embed.add_field(name="Channel: ", value=f"{ch.mention}", inline=False)
        else:
            find_cmd = ["channel"]
            embed = discord.Embed(
                title="จะให้ค้นหาอะไรหรอ",
                description="\n".join(find_cmd),
                color=themeColor
            )

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Find(bot))