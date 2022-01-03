import json
import discord
from discord import embeds
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

async def validate_failed(ctx, cmd, text):
    embed = discord.Embed(
        title="❌\tใส่ข้อมูลผิด\t❌",
        description=f"{text}\nหรือ ตรวจสอบการใช้ชนิดข้อมูลโดย ```{prefix}help {cmd}```",
        color=redColor
    )
    await ctx.channel.send(embed=embed)

def is_time(time):
    if len(time.split(".")) == 2:
        time_attr = time.split(".")
    elif len(time.split(":")) == 2:
        time_attr = time.split(":")
    else:
        return False

    if time_attr[0].isdigit() and 0 <= int(time_attr[0]) <= 23:
        if time_attr[1].isdigit() and 0 <= int(time_attr[1]) <= 59:
            return True
    return False

def is_day(day):
    if str(day).isdigit() and 0 <= int(day) <= 6:
        return True
    return False

def to_beauty_str(str):
    new_str = ""
    for i in range(len(str)):
        if (i != 0 and str[i].isupper() and not str[i-1].isupper()) or (str[i].isdigit() and str[i-1].isalpha()) or (str[i-1].isdigit() and str[i].isalpha()):
            new_str += " "+str[i]
        else:
            new_str += str[i]
    return new_str.strip()