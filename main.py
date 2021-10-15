import discord
from discord.ext import commands
import os
import asyncio
from settings import *


bot = commands.Bot(command_prefix=prefix, help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

cmds = []
short_cmds = {"au":"author", "cu":"cheerup", "h":"help", "p":"perm", "r":"role"}

for file in os.listdir("commands"):
    if ".py" in file:
        file = file.split(".py")[0]
        # if os.path.exists(os.path.join("commands", f"{file}.py")):
        cmds += [file]
        bot.load_extension(f"commands.{file}")

@bot.event
async def on_message(message):
        if message.author == bot.user:
            return 
        
        msg = message.content.lower()
        author = message.author
        
        if msg.startswith(prefix):
            txt = msg.split(prefix)[1].strip()
            msg = txt.split(" ")
            cmd = msg[0];
            print(f"{author} calls '{cmd}'")

            if cmd in ["role", "perm", "r", "p"]:
                if not check_permisstion(message.author.id):
                    return
            if cmd in cmds:
                message.content = f"{prefix}{cmd} {txt[len(cmd)+1:len(txt)]}"
            elif cmd in short_cmds:
                message.content = f"{prefix}{short_cmds[cmd]} {txt[len(cmd)+1:len(txt)]}"
            await bot.process_commands(message)

        if "ก้อนเมฆ" in msg:
            msg_del = await message.channel.send(
                embed=discord.Embed(
                    description="เอ๊ะ มีใครเรียกชื่อนะ",
                    color=colorTheme
                )
            )
            print(f"{message.author.name} says 'ก้อนเมฆ' in {message.channel.id}")
            await asyncio.sleep(3) 
            await msg_del.delete()


def check_permisstion(id):
    if id == authorId:
        return True
    return False

bot.run(token)