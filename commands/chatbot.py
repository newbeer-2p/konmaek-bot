import discord
from discord.ext import commands
from settings import *
import random

class Chatbot(commands.Cog, name="Chatbot"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.command()
    async def chatbot(self, ctx, msg=""):
        greeting = ["สวัสดี", "ดีจ้า", "ไง", "ฮัลโหล", "หวัดดี", "hi", "hello", "อรุณสวัสดิ์", "hey", "ฮาย"]
        dumb = ["เหี้ย", "สัส", "โง่", "ควาย", "ห่า"]
        sad = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
        call = ["ก้อนเมฆ"]

        bot_greeting = ["สวัสดีจ้าาา"]
        bot_dumb = ["ด่าเค้าหรอ!!!"]
        bot_sad = []
        bot_default = ["พูดอะไรไม่เห็นรู้เรื่องเลย"]

        messages = []

        if (messages == []):
            for word in greeting:
                if word in msg:
                    messages = bot_greeting
                    break
        if (messages == []):
            for word in dumb:
                if word in msg:
                    messages = bot_dumb
                    break
        if (messages == []):
            messages = bot_default
        
        embed = discord.Embed(
            description=random.choice(messages),
            color=colorTheme
        )

        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Chatbot(bot))