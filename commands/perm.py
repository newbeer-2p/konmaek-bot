import discord
from discord.ext import commands
import random
# from settings import token, prefix, authorId, colorTheme

class Hi(commands.Cog, name="Hi"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def perm(self, ctx):
        # if (not check_permisstion(ctx)):
        #     return

        print(ctx.author.guild_permissions)

def setup(bot: commands.Bot):
    bot.add_cog(Hi(bot))