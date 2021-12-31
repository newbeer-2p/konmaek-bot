import discord
from discord.ext import commands
from settings import *
from firebase_admin import db

class Chat(commands.Cog, name="Chat"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def chat(self, ctx, cmd=""):
        
        ref = db.reference(f"/chats/")
        guild = ctx.guild

        no_chat_channel = True
        chn_id = int(db.reference(f"/chats/{guild.id}").get()["channel"])
        for chn in guild.text_channels:
            if chn.id == chn_id:
                channel = chn
                no_chat_channel = False
        if cmd == "setup":
            title = "สร้างช่องแชทของ ☁ น้อนก้อนเมฆ ☁"
            
            if no_chat_channel:
                try:
                    channel = await guild.create_text_channel("konmaek-chat")
                    ref.update({
                        guild.id: {
                            "name": guild.name,
                            "channel": channel.id
                        }
                    })
                    embed = discord.Embed(
                        title=title,
                        description=f"สำเร็จ! คุยกับเค้าได้ในนี้เลย {channel.mention}",
                        color=greenColor
                    )
                except:
                    embed = discord.Embed(
                        title=title,
                        description="ไม่สำเร็จ! เนื่องจาก Permission ไม่ถึง",
                        color=redColor
                    )
            else:
                embed = discord.Embed(
                    title=title,
                    description=f"ไม่สำเร็จ! เนื่องจาก มี {channel.mention} นี้อยู่แล้ว",
                    color=redColor
                )
        else:
            title="อยากคุยกับเค้าหรอ"
            if (no_chat_channel):
                embed = discord.Embed(
                        title=title,
                        description=f"แต่ยังไม่มีห้องเลยนะ ลองใช้คำสั่งนี้ก่อนนะ ```{prefix}chat setup``` ",
                        color=themeColor
                    )
            else:
                embed = discord.Embed(
                        title=title,
                        description=f"มาคุยในห้องนี้เลย {channel.mention}",
                        color=themeColor
                    )
        await ctx.channel.send(embed=embed)

    

def setup(bot: commands.Bot):
    bot.add_cog(Chat(bot))