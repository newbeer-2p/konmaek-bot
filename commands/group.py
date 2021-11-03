import discord
from discord.ext import commands
from settings import *
import random

class Group(commands.Cog, name="Group"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def group(self, ctx, cmd="", *, attr=""):

        if cmd in ["random", "r"]:
            attr = attr.split()
            embed = discord.Embed(
                    title="📜 ผลจากการสุ่มกลุ่ม 📜",
                    color=colorTheme
                )
            if not attr[0].isdigit():
                attr.pop(0)
                embed.add_field(
                    name="ผู้โชคดีก็คือ...",
                    value=f"```{random.choice(attr)}```"
                )
            else:
                num_group = int(attr.pop(0))
                ran_group = []
                for _ in range(num_group):
                    ran_group.append([])
                group_no = 0
                while len(attr) != 0:
                    rdm = random.randint(0, len(attr)-1)
                    ran_group[group_no] += [attr.pop(rdm)]
                    group_no += 1
                    if group_no == num_group:
                        group_no = 0
                
                print(ran_group)
                for i in range(num_group):
                    names = ""
                    for name in ran_group[i]:
                        names += f"\n{name}"
                    else:
                        names += " "
                    embed.add_field(
                        name=f"กลุ่มที่ {i+1}",
                        value=f"```{names}```"
                    )
        else:
            embed = discord.Embed(
                title="📜 คำสั่งเกี่ยวกับกลุ่ม 📜",
                description=f"อยากให้เราช่วยเธอหรอ คำสั่งนี้อาจเธอได้นะ ```{prefix}help group```",
                color=colorTheme
            )

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Group(bot))