import discord
from discord.ext import commands
from settings import *
from modules import *
import random

class Food(commands.Cog, name="Food"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def food(self, ctx, cmd=""):
        data = load_json('database/food.json')
        if cmd in ["random", "r"]:
            random_food = random.choice(data)
            embed = discord.Embed(
                title=random_food["name"],
                description=f'({random_food["eng_name"]})',
                color=colorTheme
            )
            if len(random_food['meat']) != 0:
                embed.add_field(
                    name="เนื้อสัตว์",
                    value=f"```{' '.join(random_food['meat'])}```"
                )
            else:
                embed.add_field(
                    name="เนื้อสัตว์",
                    value=f"```ไม่มี```"
                )
            if random_food['avg_calories'] != None:
                embed.add_field(
                    name="แคลอรี่เฉลี่ย",
                    value=f"```{random_food['avg_calories']}```"
                )
            else:
                embed.add_field(
                    name="แคลอรี่เฉลี่ย",
                    value=f"```ไม่ทราบ```"
                )
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"เมนูทั้งหมดที่เค้ามีคือ {len(data)} เมนู",
                color=colorTheme
            )
            for food in data:
                embed.add_field(
                    name=f"📜 {food['name']} 📜",
                    value=f"({food['eng_name']})"
                ,inline=False)
            await ctx.channel.send(embed=embed)

        
def setup(bot: commands.Bot):
    bot.add_cog(Food(bot))