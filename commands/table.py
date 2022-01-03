import discord
from discord.ext import commands, tasks
from settings import *
from modules import *
from firebase_admin import db

from datetime import datetime

class Table(commands.Cog, name="Table"):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.check_table_schedule.start()

    @tasks.loop(minutes=1)
    async def check_table_schedule(self):
        date = datetime.now()
        dates = date.strftime("%w:%X").split(":")
        day = dates[0]
        hour = dates[1]
        minute = dates[2]
        for guild in self.bot.guilds:
            chn_db = db.reference(f"/guilds/{guild.id}/announce/")
            if chn_db.get() is None or chn_db.get()["id"] is None or chn_db.get()["id"] not in [ch.id for ch in guild.channels]:
                announce_ch = await guild.create_text_channel("☁️📢 Konmaek Announcement 📢☁️")
                chn_db.update({"id" : announce_ch.id})
                announce_id = announce_ch.id
            else:
                announce_id = chn_db.get()["id"]
            announce_mems = db.reference(f"/guilds/{guild.id}/announce/members/").get()
            if announce_mems is not None:
                for id in announce_mems:
                    for table_name_id in announce_mems[id]:
                        if table_name_id == "name":
                            continue
                        table_name = announce_mems[id][table_name_id]["table"]
                        tables = db.reference(f"/members/{id}/tables/{table_name}/").get()
                        for sub in tables:
                            if sub != "name":
                                sub_hour, sub_minute = tables[sub]["time"].split("-")[0].split(".")
                                if int(tables[sub]["day"]) == int(day) and int(hour) == int(sub_hour) and int(minute) == int(sub_minute):
                                    embed = discord.Embed(
                                        title=f"ก๊อกๆ คุณ {announce_mems[id]['name']}\nตอนนี้เวลา {hour}:{minute} น. แล้วว",
                                        description=f"**วิชา {tables[sub]['name']}**\nเรียนที่ **{tables[sub]['at']}**",
                                        color=themeColor
                                    )
                                    await self.bot.get_channel(announce_id).send(embed=embed)
                                    # user = await self.bot.wait_for("message", check=self.bot.fetch_user(int(id)))
                                    # print(user.name)
                                    # await self.bot.get_channel(announce_id).send(content="Yes!")
    
    @commands.command()
    async def table(self, ctx, cmd="", name="", *, attr=""):
        table_db = db.reference(f"/members/{ctx.author.id}/tables/")
        tables = table_db.get()
        if name == ".":
            name = tables["default"]
        if cmd == "announce":
            if name == "" or len(attr.split()) != 1 or attr.lower() not in ["on", "off"]:
                await error_text(ctx, "table")
                return
            if tables is not None and await check_table(ctx, name.lower()):
                return

            announce_db = db.reference(f"/guilds/{ctx.guild.id}/announce/members/{ctx.author.id}/")
            announces = announce_db.get()
            if attr.lower() == "on":
                if name in [announces[table] for table in announces]:
                    announce_db.update({
                        "name" : ctx.author.display_name
                    })
                    announce_db.push({
                        "table" : name
                    })
                embed = discord.Embed(
                    title=f"เปิดการแจ้งเตือนตาราง {to_beauty_str(name)} สำเร็จ",
                    color=greenColor
                )
            else:
                if announces is not None:
                    done = False
                    for table in announces:
                        if table != "name" and announces[table] == name:
                            db.reference(f"/guilds/{ctx.guild.id}/announce/members/{ctx.author.id}/{table}").delete()
                            done = True
                            break
                    if done:
                        embed = discord.Embed(
                            title=f"ปิดการแจ้งเตือนตาราง {to_beauty_str(name)} สำเร็จ",
                            color=greenColor
                        )
                    else:
                        embed = discord.Embed(
                            title=f"ปิดการแจ้งเตือนตาราง {to_beauty_str(name)} ไม่สำเร็จ",
                            color=redColor
                        )
        elif cmd in ["create", "c"]:
            if name == "":
                await error_text(ctx, "table")
                return
            if tables is not None and await check_table(ctx, name.lower()):
                return
            
            table_db.update({
                "default" : name.lower()
            })
            create_table_db = db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/")
            create_table_db.update({
                "name": to_beauty_str(name)
            })
            embed = discord.Embed(
                title="สร้างตารางเรียน สำเร็จ",
                description=f"ทำการเพิ่มตาราง {to_beauty_str(name)} เรียบร้อย",
                color=greenColor
            )
        elif cmd in ["add", "a"]:
            if name == "" or len(attr.split()) != 4:
                await error_text(ctx, "table")
                return
            if tables is not None and await check_table(ctx, name.lower()):
                return
            
            attrs = attr.split()
            sub_name = attrs[0]
            day = attrs[1]
            if not is_day(day):
                await validate_failed(ctx, "table","กรุณาใส่วันเป็นตัวเลข 0-6 โดย 0 คือวันอาทิตย์")
                return
            day = int(attrs[1])
            time = attrs[2]
            if not (is_time(time.split("-")[0]) and is_time(time.split("-")[1])):
                await validate_failed(ctx, "table","กรุณาใส่เวลาให้ถูกต้องโดย ex. 00.00-00.01")
                return
            at = attrs[3]
            add_table_db = db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/{sub_name.lower()}")
            if add_table_db.get() is None:
                add_table_db.update({
                    "name": to_beauty_str(sub_name),
                    "day": day,
                    "time": time,
                    "at": at
                })
                embed = discord.Embed(
                    title="เพิ่มวิชา สำเร็จ",
                    description=f"เพิ่มวิชา **{to_beauty_str(sub_name)}**\nทุกๆ **{days[day]}**\nเวลา **{time}**\nสถานที่ **{at}**\nลงในตาราง {tables[name.lower()]['name']}",
                    color=greenColor
                )
            else:
                embed = discord.Embed(
                    title="เพิ่มวิชา ไม่สำเร็จ",
                    description=f"เนื่องจากมีชื่อวิชา {to_beauty_str(sub_name)} ซ้ำในตาราง {tables[name.lower()]['name']}",
                    color=redColor
                )

        elif cmd in ["remove", "rm"]:
            if name == "" or len(attr.split()) != 1:
                await error_text(ctx, "table")
                return
            if tables is not None and await check_table(ctx, name.lower()):
                return

            remove_tables = db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/").get()

            removed = False
            for sub in remove_tables:
                if sub != "name" and sub.lower() == attr.lower():
                    db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/{attr.lower()}").delete()
                    removed = True
                    break
            if removed:
                embed = discord.Embed(
                    title=f"ลบวิชา **{attr}** เสร็จสิ้น",
                    description=f"ลบวิชา {attr} ออกจากตาราง {tables[name.lower()]['name']} แล้ว",
                    color=greenColor
                )
            else:
                embed = discord.Embed(
                    title=f"ลบวิชา **{attr}** ไม่เสร็จสิ้น",
                    description=f"เนื่องจากวิชา **{attr}** ไม่อยู่ในตาราง {tables[name.lower()]['name']}",
                    color=redColor
                )
        elif cmd in ["edit", "e"]:
            if tables is not None and await check_table(ctx, name.lower()):
                return
            
            if name == "" or len(attr.split()) != 3 or attr.split()[1] not in ["name", "day", "time", "at"]:
                await error_text(ctx, "table")
                return

            edit_table_db = db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/")
            attrs = attr.split()

            edited = False

            if attrs[1].lower() == "day" and not is_day(attrs[2]):
                await validate_failed(ctx, "table","กรุณาใส่วันเป็นตัวเลข 0-6 โดย 0 คือวันอาทิตย์")
                return
            elif attrs[1].lower() == "time" and not (is_time(attrs[2].split("-")[0]) and is_time(attrs[2].split("-")[1])):
                await validate_failed(ctx, "table","กรุณาใส่เวลาให้ถูกต้องโดย ex. 00.00-00.01")
                return

            for sub in edit_table_db.get():
                if attrs[1].lower() == "name" and sub.lower() == attrs[0].lower():
                    data_sub_db = db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/{attrs[0].lower()}")
                    data_sub_db.update({"name" : to_beauty_str(attrs[2])})
                    db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/{attrs[2].lower()}").update(data_sub_db.get())
                    data_sub_db.delete()
                    edited = True
                    break
                elif sub != "name" and sub.lower() == attrs[0].lower():
                    db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/{attrs[0].lower()}").update({
                        attrs[1].lower() : attrs[2]
                    })
                    edited = True
                    break
            if edited:
                embed = discord.Embed(
                    title=f"แก้ไขรายละเอียดของวิชา **{attrs[0]}** เสร็จสิ้น",
                    description=f"แก้ไขรายละเอียดของวิชา {attrs[0]} ของตาราง {tables[name.lower()]['name']} แล้ว",
                    color=greenColor
                )
            else:
                embed = discord.Embed(
                    title=f"แก้ไขรายละเอียดของวิชา **{attrs[0]}** ไม่เสร็จสิ้น",
                    description=f"เนื่องจากวิชา **{attrs[0]}** ไม่อยู่ในตาราง {tables[name.lower()]['name']}",
                    color=redColor
                )
        elif cmd in ["reset", "rs"]:
            if name == "":
                await error_text(ctx, "table")
                return
            if tables is not None and await check_table(ctx, name.lower()):
                return
            
            db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}").set({"name" : to_beauty_str(name)})
            
        elif cmd in ["default", "df"]:
            if name == "":
                embed = discord.Embed(
                    title=f"ตารางปัจจุบันก็คือ {tables[tables['default']]['name']}",
                    description=f"สามารถตั้งค่าตารางปัจจุบันใหม่โดยคำสั่ง ```{prefix}table default [ชื่อตาราง]```",
                    color=themeColor
                )
            elif name.lower() in [table for table in tables]:
                table_db.update({
                    "default": name.lower()
                })
                embed = discord.Embed(
                    title="ตั้งค่าตารางปัจจุบันเสร็จสิ้น",
                    description=f"ตั้งค่าตาราง {to_beauty_str(name)} เรียบร้อยแล้ว",
                    color=greenColor
                )
            else:
                embed = discord.Embed(
                    title="ตั้งค่าตารางปัจจุบัน ไม่สำเร็จ",
                    description=f"ไม่พบเจอตาราง {name.lower()} นี้",
                    color=redColor
                )
        elif cmd in ["list", "l"]:
            embed = discord.Embed(
                title="ตารางเรียนทั้งหมดมี :",
                color=themeColor
            )
            for table_name in tables:
                if table_name != "default":
                    embed.add_field(name=tables[table_name]["name"], value=f"มีทั้งหมด {len(tables[table_name])} วิชา", inline=False)
        elif cmd in ["settablename", "st"]:
            if attr not in [table for table in tables]:
                settablename_db = db.reference(f"/members/{ctx.author.id}/tables/{name.lower()}/")
                old_table = settablename_db.get()["name"]
                settablename_db.update({"name" : to_beauty_str(attr)})
                data_table = settablename_db.get()
                settablename_db.delete()
                db.reference(f"/members/{ctx.author.id}/tables/{attr.lower()}/").update(data_table)
                if tables["default"] == old_table.lower().replace(" ", ""):
                    table_db.update({
                        "default" : attr.lower()
                    })
                embed = discord.Embed(
                        title=f"แก้ไขชื่อ **{attr}** เสร็จสิ้น",
                        description=f"แก้ไขชื่อตารางจาก {old_table} เป็น {to_beauty_str(attr)} เรียบร้อย",
                        color=greenColor
                    )
            else:
                embed = discord.Embed(
                    title=f"แก้ไขชื่อ **{attr[0]}** ไม่เสร็จสิ้น",
                    description=f"เนื่องจากวิชา **{attr[0]}** ไม่อยู่ในตาราง {tables[name]['name']}",
                    color=redColor
                )
        else:
            if tables is None or tables["default"] is None:
                embed = discord.Embed(
                    title="เหมือนยังไม่มีตารางเลยนะ",
                    description=f"ลองสร้างตารางดูสิ ```{prefix}table create ชื่อตาราง```หรือ```{prefix}table default ชื่อตาราง```",
                    color=redColor
                )
            else:
                embed = discord.Embed(
                    title=f"ตารางเรียน {tables[tables['default']]['name']}",
                    description=f"รายละเอียดตามนี้เลย",
                    color=greenColor
                )
                my_table = db.reference(f"/members/{ctx.author.id}/tables/{tables['default']}").get()
                days_emoji = {0: "❤️", 1: "💛", 2:"💗", 3:"💚", 4:"🧡", 5:"💙", 6:"💜"}
                for day in range(7):
                    detail = []
                    for sub in my_table:
                        if sub != "name" and int(my_table[sub]["day"]) == day:
                            detail += [f"\nวิชา : {my_table[sub]['name']}\nเวลา : {my_table[sub]['time']}\nสถานที่ : {my_table[sub]['at']}"]
                    embed.add_field(name=f"{days_emoji[day]}\t{days[day]}\t{days_emoji[day]}", value="```"+"\n".join(detail)+" ```", inline=False)
        await ctx.channel.send(embed=embed)

async def check_table(ctx, name):
    if name not in [table_name for table_name in db.reference(f"/members/{ctx.author.id}/tables/").get()]:
        embed = discord.Embed(
            title="ดำเนินการไม่สำเร็จ",
            description="เนื่องจากไม่มีตารางนี้",
            color=redColor
        )
        await ctx.channel.send(embed=embed)
        return True
    return False

def setup(bot: commands.Bot):
    bot.add_cog(Table(bot))