import discord
from discord.ext import commands
from discord.ext import tasks
from settings import *
from modules import *

cog = commands.Cog

class Timer(commands.Cog, name="Timer"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.index = 0
    
    @commands.command()
    async def timer(self, ctx):
        embed = discord.Embed(
            title="น้องก้อนเมฆจะจับเวลาละนะ",
            description=f"**▶️ เพื่อเริ่มจับเวลา\n\n⏸ เพื่อหยุดจับเวลา\n\n⏹ เพื่อรีเซตการจับเวลา**",
            color=themeColor
        )
        self.msg = await ctx.channel.send(embed=embed)
        for emoji in ["▶️", "⏸", "⏹"]:
            await self.msg.add_reaction(emoji)
    
    @cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.bot.user.id == user.id:
            return
        if reaction.emoji == "▶️":
            if not self.printer.is_running():
                self.printer.start()
        elif reaction.emoji == "⏸":
            self.printer.cancel()
            embed = discord.Embed(
                title="น้องก้อนเมฆนับ...",
                description="**%02d:%02d**" %(self.index//60, self.index%60)+"\n\nกำลังหยุดอยู่ \n▶️ เพื่อจับเวลาต่อ ⏹ เพื่อรีเซตการจับเวลา",
                color=(themeColor if self.index%2 == 0 else 0xffffff)
            )
            await reaction.message.edit(embed=embed)
        elif reaction.emoji == "⏹":
            self.printer.cancel()
            self.index = 0
            embed = discord.Embed(
                title="น้องก้อนเมฆจะจับเวลาละนะ",
                description=f"**▶️ เพื่อเริ่มจับเวลา\n\n⏸ เพื่อหยุดจับเวลา\n\n⏹ เพื่อรีเซตการจับเวลา**",
                color=themeColor
            )
            await reaction.message.edit(embed=embed)
        await reaction.message.remove_reaction(reaction.emoji, user)

    @tasks.loop(seconds=1)
    async def printer(self):
        self.index += 1
        embed = discord.Embed(
            title="น้องก้อนเมฆนับ...",
            description="**%02d:%02d**" %(self.index//60, self.index%60),
            color=(themeColor if self.index%2 == 0 else 0xffffff)
        )
        await self.msg.edit(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Timer(bot))