import discord
from discord.ext import commands
from settings import *
from modules import *

class Help(commands.Cog, name="Help"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx, attr=""):
        embed = discord.Embed(
            title="😎 คำสั่งช่วยเหลือท่าน 😎",
            description=f"**Prefix :** ```{prefix}```",
            color=themeColor
        )
        help_cmds = load_json("database/help.json")

        help_cmds_text = ""
        if attr != "":
            for cmd in help_cmds:
                prefix_cmd = prefix + cmd["name"]
                if cmd["name"] == attr and len(cmd["commands"]) != 0:
                    for c in cmd["commands"]:
                        help_cmds_text += f"\n{prefix_cmd} {c['name']} [{'] ['.join(c['attributes'])}]\n: ({c['short']}) {c['details']}\n"
                    embed.add_field(name=f"คำสั่งของ {cmd['name']}", value=f"```{help_cmds_text} ```", inline=False)
                    break
                elif cmd["name"] == attr and len(cmd["commands"]) == 0:
                    help_cmds_text += f"{prefix}{cmd['name']} "+f"[{' ['.join(cmd['attributes'])}]"*(len(cmd["attributes"]) != 0)+f"\n: ({cmd['short']}) คำสั่งเกี่ยวกับ{cmd['description']}\n"
                    embed.add_field(name=f"คำสั่งของ {cmd['name']}", value=f"```{help_cmds_text} ```", inline=False)
        else:
            for cmd in help_cmds:
                if cmd["name"] not in dont_cmds:
                    help_cmds_text += f"\n{prefix}{cmd['name']} : ({cmd['short']}) คำสั่งเกี่ยวกับ{cmd['description']}"
            embed.add_field(name=f"คำสั่งทั้งหมด", value=f"```{help_cmds_text}```", inline=False)
        
        embed.add_field(name="ต้องการดูคำสั่งเพิ่มเติม : ", value=f"```{prefix}help [คำสั่ง]```", inline=False)
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))