import discord
from discord.ext import commands
from settings import *

class Role(commands.Cog, name="Role"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def role(self, ctx, cmd="", attr=""):
        cmd = cmd.lower()
        guild = ctx.guild
        user = ctx.author
        roles = guild.roles

        if (cmd == "create" or cmd == "c") and attr != "":
            if attr.lower() not in [y.name.lower() for y in roles]:
                try:
                    await guild.create_role(name=attr)
                    embed = discord.Embed(
                        title=f"สร้างบทบาท **{attr}** สำเร็จ",
                        description=f"ทำการเพิ่มบทบาท **{attr}** ลงเซิฟเวอร์เรียบร้อย",
                        color=greenColor
                    )
                except:
                    embed = discord.Embed(
                            title=f"สร้างบทบาท **{attr}** ไม่สำเร็จ",
                            description=f"เนื่องจากเธอยังไม่ได้ให้ Permission สำหรับ **☁ เจ้าก้อนเมฆ ☁** ตัวนี้",
                            color=redColor
                        )
            else:
                embed = discord.Embed(
                    title=f"สร้างบทบาท **{attr}** ไม่สำเร็จ",
                    description=f"เนื่องจากมีบทบาท **{attr}** อยู่แล้ว",
                    color=redColor
                )
        elif cmd == "delete" or cmd == "d":
            for role in roles:
                if attr.lower() == role.name.lower():
                    try:
                        await role.delete()
                        embed = discord.Embed(
                            title=f"ลบบทบาท **{attr}** สำเร็จ",
                            description=f"ทำการลบบทบาท **{attr}** ออกจากเซิฟเวอร์เรียบร้อย",
                            color=greenColor
                        )
                    except:
                        embed = discord.Embed(
                            title=f"ลบบทบาท **{attr}** ไม่สำเร็จ",
                            description=f"เนื่องจากเธอยังไม่ได้ให้ Permission สำหรับ **☁ เจ้าก้อนเมฆ ☁** ตัวนี้",
                            color=redColor
                        )
                    break
            else:
                embed = discord.Embed(
                    title=f"ลบบทบาท **{attr}** ไม่สำเร็จ",
                    description=f"เนื่องจากไม่มีบทบาท **{attr}** ในเซิฟเวอร์",
                    color=redColor
                )
        elif cmd == "list" or cmd == "l":
            roles = [f"- {y.name}" for y in roles]
            embed = discord.Embed(
                title=f"บทบาททั้งหมดใน {guild.name}",
                description="\n".join(roles),
                color=themeColor
            )
        else:
            embed = discord.Embed(
                title="ลองให้คำสั่งนี้ช่วยเหลือเธอสิ",
                description=f"```{prefix}help```",
                color=themeColor
            )

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Role(bot))