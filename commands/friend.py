import discord
from discord.ext import commands
from settings import *
from firebase_admin import db

class Friend(commands.Cog, name="Friend"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def friend(self, ctx, cmd="", *, attr=""):
        friends_db = db.reference(f"/{ctx.author.id}/friends/")
        friends = friends_db.get()

        if cmd in ["add", "a"]:
            for name in attr.split():
                friends_db.push({
                    "name": name
                })
            embed = discord.Embed(
                title="ได้เพิ่มเพื่อนเรียบร้อยแล้ว",
                description=f"{attr} ถูกเพิ่มเข้ารายชื่อเพื่อนเรียบร้อยแล้ว",
                color=0x00ff00
            )
        elif cmd in ["remove", "rm"]:
            friends_rm = attr.split()
            for key in friends:
                if friends[key]["name"] in friends_rm:
                    db.reference(f"/{ctx.author.id}/friends/{key}/").delete()
            embed = discord.Embed(
                title="ได้ลบเพื่อนเรียบร้อยแล้ว",
                description=f"{attr} ถูกลบออกรายชื่อเพื่อนเรียบร้อยแล้ว",
                color=0x00ff00
            )
        else:
            friends_name = ""
            if friends is None:
                embed = discord.Embed(
                    title="เศร้าจังเลย... 😥",
                    description=f"เพิ่มเพื่อนได้คำสั่ง: ```{prefix}friend add [ชื่อเพื่อน]```",
                    color=colorTheme
                )
            else:
                for key in friends:
                    friends_name += f"📜 {friends[key]['name']}\n";
                embed = discord.Embed(
                    title="เพื่อนของเธอก็คือ...",
                    description=f"```{friends_name}```",
                    color=colorTheme
                )
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Friend(bot))