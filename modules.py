import json
import discord
from settings import *

def load_json(path):
    with open(path, encoding='utf-8') as json_file:
        return json.load(json_file)

async def error_text(ctx, cmd):
    embed = discord.Embed(
        title="❌\tคำสั่งผิดพลาด\t❌",
        description=f"กรุณาใช้คำสั่งตามกำหนดผ่านคำสั่ง ```{prefix}help {cmd}```",
        color=redColor
    )
    await ctx.channel.send(embed=embed)