import discord
from discord.ext import commands
import os
import asyncio
from settings import *
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
})

bot = commands.Bot(command_prefix=prefix, help_command=None)

@bot.event
async def on_ready():
    activity = discord.Activity(name="[k]help", type=2)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"We have logged in as {bot.user}")

cmds = []
short_cmds = {"au":"author", "cu":"cheerup", "h":"help", "p":"perm", "r":"role", "ct":"chat", "g":"group"}

for file in os.listdir("commands"):
    if ".py" in file:
        file = file.split(".py")[0]
        cmds += [file]
        bot.load_extension(f"commands.{file}")

@bot.event
async def on_message(message):
        if message.author == bot.user:
            return 
        
        msg = message.content.lower()
        author = message.author

        if message.channel.id == db.reference(f"/chats/{message.guild.id}").get()["channel"]:
            message.content = f"{prefix}chatbot {message.content}"
            await bot.process_commands(message)
            return
        
        if msg.startswith(prefix):
            txt = msg.split(prefix)[1].strip()
            msg = txt.split(" ")
            cmd = msg[0];
            print(f"{author} calls '{cmd}'")

            if cmd in ["role", "perm", "r", "p", "chatbot", "chat", "ct"]:
                if not message.author.id == authorId:
                    return
            if cmd in cmds:
                message.content = f"{prefix}{cmd} {txt[len(cmd)+1:len(txt)]}"
            elif cmd in short_cmds:
                message.content = f"{prefix}{short_cmds[cmd]} {txt[len(cmd)+1:len(txt)]}"
            await bot.process_commands(message)
            return

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

bot.run(token)