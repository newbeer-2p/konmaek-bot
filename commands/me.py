import discord
from discord.ext import commands
from settings import *

class Me(commands.Cog, name="Me"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def me(self, ctx):
        user = ctx.author
        embed = discord.Embed(
            title=f"{user.display_name}",
            description=f"({user})",
            color=colorTheme
        )
        embed.set_thumbnail(url=user.avatar_url)

        msg = await ctx.channel.send(embed=embed)
        for emoji in ["🇱", "🇴", "🇻", "🇪"]:
            await msg.add_reaction(emoji)

def setup(bot: commands.Bot):
    bot.add_cog(Me(bot))