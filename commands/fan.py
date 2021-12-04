import discord
from discord.ext import commands
from settings import *
from firebase_admin import db

class Fan(commands.Cog, name="Fan"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def fan(self, ctx, cmd="", *, attr=""):
        fan_db = db.reference(f"/{ctx.author.id}/fan/")
        fan = fan_db.get()
        if (cmd in ["set", "s"]):
            attrs = attr.split()
            fan_db.update({
                "name" : attrs[0],
                "image" : attrs[1]
            })
            embed = discord.Embed(
                title=f"เพิ่มชื่อและรูปเรียบร้อยแล้วว",
                color=colorTheme
            )
        elif (cmd in ["setname", "sn"]):
            fan_db.update({
                "name" : attr
            })
            embed = discord.Embed(
                title=f"เปลี่ยนชื่อเรียบร้อยแล้วว",
                color=colorTheme
            )
        elif (cmd in ["setimage", "si"]):
            fan_db.update({
                "image" : attr
            })
            embed = discord.Embed(
                title=f"เปลี่ยนรูปเรียบร้อยแล้วว",
                color=colorTheme
            )
        else:
            if fan is None:
                embed = discord.Embed(
                    title="คุณยังไม่มีแฟนเลย ลองพิมคำสั่ง",
                    description=f"```{prefix}fan set [ชื่อเพื่อน] [ลิงก์รูปภาพ]```",
                    color=colorTheme
                )
            else:
                embed = discord.Embed(
                    title=f"สวัสดีครับ คุณ, {ctx.author.display_name}",
                    description=f"ผมชื่อ {fan['name']}",
                    color=colorTheme
                )
                embed.set_thumbnail(url=fan["image"])

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Fan(bot))