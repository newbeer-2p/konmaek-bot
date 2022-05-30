import discord
from discord.ext import commands
from settings import *
import random
from firebase_admin import db

cog = commands.Cog

class rps(commands.Cog, name="rps"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def rps(self, ctx):
        rps = ["ค้อน", "กรรไกร", "กระดาษ"]
        embed = discord.Embed(
            title="เกมเป่ายิ้งฉุบ",
            description="ค้อน กรรไกร กระดาษ ออกอะไรดีน้าาาาา\n🇷 : ค้อน, 🇵 : กระดาษ, 🇸 : กรรไกร\nกดสติ๊กเกอร์ เพื่อเป่ายิ่งฉุบน้า",
            color=themeColor
        )
        embed.set_image(url="https://www.kindpng.com/picc/m/212-2122689_rock-paper-scissors-random-rock-paper-scissors-png.png")

        msg = await ctx.channel.send(embed=embed)
        rps_db = db.reference(f"/members/{ctx.author.id}/rps/")
        rps_db.update({
            "msg_id" : msg.id
        })

        for emoji in ["🇷", "🇵", "🇸"]:
            await msg.add_reaction(emoji)

    @cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.bot.user.id == user.id:
            return
        rps_db = db.reference(f"/members/{user.id}/rps/")
        msg_id = rps_db.get()
        if msg_id is None or msg_id["msg_id"] != reaction.message.id:
            await reaction.message.add_reaction(reaction.emoji)
            return
        print("On My God")
        rps_db.delete()
        rps = ["ค้อน", "กระดาษ", "กรรไกร"]
        rps_emoji = {"ค้อน": "🇷","กระดาษ": "🇵","กรรไกร": "🇸"}
        rps_name = {"🇷": "ค้อน","🇵": "กระดาษ","🇸": "กรรไกร"}
        rps_img = {
            "ค้อน" : "https://www.pinclipart.com/picdir/big/536-5360218_rock-paper-scissors-clipart-png-download-paper-rock.png",
            "กรรไกร" : "https://www.pinclipart.com/picdir/big/536-5360227_scissors-hand-rock-paper-scissors-png-clipart.png",
            "กระดาษ" : "https://www.pinclipart.com/picdir/big/536-5360310_transparent-rock-paper-scissors-clipart-rock-paper-scissors.png"
        }
        if self.bot.user.id != user.id:
            rand_rps = random.choice(rps)
            if reaction.emoji == rps_emoji[rand_rps]:
                embed = discord.Embed(
                    title="😙 เรา\"เสมอ\" 😙",
                    description="อะไรเนี่ย เราเสมอกันหรอ แย่จังเลยยย",
                    color=0xffffff
                )
            elif (reaction.emoji == "🇷" and rps_emoji[rand_rps] == "🇸") or \
                 (reaction.emoji == "🇸" and rps_emoji[rand_rps] == "🇵") or \
                 (reaction.emoji == "🇵" and rps_emoji[rand_rps] == "🇷"):
                embed = discord.Embed(
                    title="😲 เธอ\"ชนะ\" 😲",
                    description="แงงงง เธอชนะเค้าแล้ววว เดี๋ยวเค้ามาแก้มือทีหลัง",
                    color=0xffff00
                )
            else:
                embed = discord.Embed(
                    title="😁 เธอ\"แพ้\" 😁",
                    description="ว้ายยย เธอแพ้แล้ว ไว้มาแก้มือกันใหม่นะ อิอิ",
                    color=0xff00ff
                )
            embed.add_field(name="เค้าออก :", value=f"```{rand_rps}```")
            embed.set_image(url=rps_img[rand_rps])
            embed.set_thumbnail(url=rps_img[rps_name[reaction.emoji]])
            await reaction.message.edit(embed=embed)
            await reaction.message.clear_reactions()

def setup(bot: commands.Bot):
    bot.add_cog(rps(bot))