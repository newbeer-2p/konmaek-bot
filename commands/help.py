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
            description=f"คำสั่งของเค้านะ () :\n(ตัวย่อ)คำสั่งเต็ม [สามารถใส่ข้อมูลเพิ่มเติมได้] : คำอธิบายคำสั่ง\n\n**Prefix :** ```{prefix}```",
            color=colorTheme
        )

        if (attr == "role"):
                embed.add_field(name="ตัวอย่างการพิมพ์คำสั่ง:", value=f"```{prefix}role add Rainbow```", inline=False)
                embed.add_field(name="คำสั่งเกี่ยวกับบทบาท:", value="\
```\
role (c)create  [ชื่อ] : สร้างบทบาท\n\
role (a)add     [ชื่อ] : เพิ่มคนเข้าบทบาท\n\
role (rm)remove [ชื่อ] : เอาคนออกจากบทบาท\n\
role (d)delete  [ชื่อ] : ลบบทบาท\n\
role (l)list         : แสดงชื่อบทบาททั้งหมด\n\
```", inline=False)
        else:
            embed.add_field(name="ตัวอย่างการพิมพ์คำสั่ง:", value=f"```{prefix}cheerup, {prefix}au```", inline=False)
            embed.add_field(name="คำสั่งทั่วไป (ตัวย่อ) :",value="(ตัวย่อ)คำสั่งเต็ม [สามารถใส่ข้อมูลเพิ่มเติมได้] : คำอธิบายคำสั่ง\n\
```\
(au)author  : แสดงคนจัดทำ\n\
(cu)cheerup : คำสั่งให้กำลังใจ\n\
(h)help []  : ช่วยเหลือคำสั่ง\n\
()hi        : คำสั่งทักทาย\n\
()me        : คำสั่งถามว่าเธอคือใคร\n\
```", inline=False)
# (r)role []  : คำสั่งเกี่ยวกับบทบาท\n\
# (p)perm []  : คำสั่งเกี่ยวกับบทบาท\n\
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))