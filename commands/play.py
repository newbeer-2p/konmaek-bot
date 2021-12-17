import discord
from discord import channel
from discord.ext import commands
from settings import *
from modules import *

from discord.utils import get
from youtube_dl import YoutubeDL

class Play(commands.Cog, name="Play"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def play(self, ctx, url=""):
        channel = ctx.author.voice.channel
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None:
            await ctx.channel.send("Joined")
            await channel.connect()
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        
        YDL_OPTIONS = {'format' : 'bestaudio/best',"noplaylist" : True, 'default_search': 'auto'}
        FFMPEG_OPTIONS = { 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        if not voice_client.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice_client.is_playing()
        else:
            await ctx.channel.send("Already playing song")
            return

def setup(bot: commands.Bot):
    bot.add_cog(Play(bot))