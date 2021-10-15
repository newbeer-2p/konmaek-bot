import discord
from discord.ext import commands
from settings import *

class Author(commands.Cog, name="Author"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def author(self, ctx):
        embed = discord.Embed(
            title="🌈 คนนี้คือเจ้าของของเค้าเอง 🌈",
            description="``` นิวเบียร์ (Newbeer) ```\nช่องทางการติดต่อ:",
            color=colorTheme
        )
        embed.add_field(
            name="Github :",
            value="[newbeerpongsakorn](https://github.com/newbeerpongsakorn)"
        )
        embed.add_field(
            name="Facebook :",
            value="[Newbeer Pongsakorn](https://facebook.com/newbeerpongsakorn)"
        )
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/56405832?s=400&u=3ec2869ae276ba6a08dfa5f5a4d29e8c07ead187&v=4")
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Author(bot))