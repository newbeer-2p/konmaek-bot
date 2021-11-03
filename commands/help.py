import discord
from discord.ext import commands
from settings import *

class Help(commands.Cog, name="Help"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx, attr=""):
        embed = discord.Embed(
            title="😎 คำสั่งช่วยเหลือท่าน 😎",
            description=f"คำสั่งของเค้านะ :\n\n**Prefix :** ```{prefix}```",
            color=colorTheme
        )

        if (attr in ["chat", "ct"]):
                embed.add_field(name="ตัวอย่างการพิมพ์คำสั่ง :", value=f"```{prefix}role add Rainbow```", inline=False)
                embed.add_field(name="คำสั่งเกี่ยวกับบทบาท :", value=f"\
```\
{prefix}chat setup : สร้างบทบาท\n\
```", inline=False)
        elif (attr in ["group", "g"]):
                embed.add_field(name="ตัวอย่างการพิมพ์คำสั่ง :", value=f"```{prefix}group random 2 ก้อนเมฆ สายรุ้ง```", inline=False)
                embed.add_field(name="คำสั่งเกี่ยวกับกลุ่ม :", value=f"\
```\
{prefix}group random [จำนวนกลุ่ม] [ชื่อคั่นด้วยเว้นวรรค]\n\
```", inline=False)
# {prefix}group list\n\
        elif (attr in ["role", "r"]):
                embed.add_field(name="ตัวอย่างการพิมพ์คำสั่ง :", value=f"```{prefix}chat setup```", inline=False)
                embed.add_field(name="คำสั่งเกี่ยวกับการแชท :", value=f"\
```\
{prefix}role create  [ชื่อ] : (c)  สร้างบทบาท\n\
{prefix}role delete  [ชื่อ] : (d)  ลบบทบาท\n\
{prefix}role list         : (l)  แสดงชื่อบทบาททั้งหมด\n\
```", inline=False)
# {prefix}role add     [ชื่อ] : (a)  เพิ่มคนเข้าบทบาท\n\
# {prefix}role remove  [ชื่อ] : (rm) เอาคนออกจากบทบาท\n\
        else:
            embed.add_field(name="ตัวอย่างการพิมพ์คำสั่ง :", value=f"```{prefix}cheerup, {prefix}au```", inline=False)
            embed.add_field(name="คำสั่งทั่วไป (ตัวย่อ) :",value=f"คำสั่งเต็ม : (ตัวย่อ) คำอธิบายคำสั่ง\n\
```\
{prefix}author  : (au) แสดงคนจัดทำ\n\
{prefix}chat    : (ct) คำสั่งคุยกับเค้า\n\
{prefix}cheerup : (cu) คำสั่งให้กำลังใจ\n\
{prefix}find    : (f)  คำสั่งค้นหา\n\
{prefix}group   : (g)  คำสั่งเกี่ยวกับกลุ่ม\n\
{prefix}help    : (h)  ช่วยเหลือคำสั่ง\n\
{prefix}hi      :      คำสั่งทักทาย\n\
{prefix}me      :      คำสั่งถามว่าเธอคือใคร\n\
{prefix}role    : (r)  คำสั่งเกี่ยวกับบทบาท\n\
```", inline=False)
# {prefix}perm []  :(p) คำสั่งเกี่ยวกับบทบาท\n\
        embed.add_field(name="ต้องการดูคำสั่งเพิ่มเติม : ", value=f"```{prefix}help [คำสั่ง]```", inline=False)
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))