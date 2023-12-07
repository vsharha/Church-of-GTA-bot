import csv
import os
import random as r
from datetime import datetime as dt
import cv2
from pytz import timezone as tz

import discord
from discord.ext import commands

from gta_keywords import gta_keywords
from keep_alive import keep_alive

token = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("pr ", "PR ", "Pr ", "pR "), case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    print("Initiated.")

help_command_values = (
    ("pr help", "Show this message"),
    ("pr pray", "See the current time in some server members' timezones"),
    ("pr gta6", "Get an accurate Trailer 2 release date prediction"),
    ("pr trailer 1-5", "Get random frames from Trailer 1"),
    ("pr [sam/lucia/jason] 1-10", "Get random pictures of Sam Houser, Lucia or Jason"),
)


class my_help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(description="**List of available commands:**",
                              color=discord.Color.dark_green())
        for i in help_command_values:
            embed.add_field(name=f"• `{i[0]}`", value=i[1], inline=False)
        embed.set_footer(text="pr help")
        await self.context.send(embed=embed)


bot.help_command = my_help()


def get_date(timezone):
    now = dt.now(tz(timezone))
    date_str = now.strftime("%dth of %B, %I:%M %p"+(" (%H:%M)" if now.strftime('%H') > now.strftime('%I') else ""))
    if date_str[0] == "0":
        date_str = date_str[1:]
    if not 11 <= now.day <= 13:
        check = now.day % 10
        if 1 <= check <= 3:
            date_str = date_str.replace(
                "th", "st" if check == 1 else "nd" if check == 2 else "rd")
    return date_str

def get_valid_range(num, maxi):
    try:
        num = int(num)
    except:
        return 1
        
    if num <= 0:
        return 1
    if num > maxi:
        return maxi
    return num

async def send_random_photo_from_dir(ctx, dir, arg1):
    arg1 = get_valid_range(arg1, 10)
        
    for i in range(arg1):
        file = discord.File(f"img/{dir}/{r.choice(os.listdir('img/'+dir))}")
    
        embed = discord.Embed(description=f"**{dir.capitalize()} image{f' #{i+1}' if arg1 > 1 else ''}:**",
                              color=discord.Color.teal())
        embed.set_image(url = "attachment://" + file.filename)
        embed.set_footer(
            text=f"pr {dir} - Let me know if you have any suggestions!")
        
        await ctx.channel.send(file = file, embed = embed)

def get_users_file_names():
    with open("users_file_names.csv", "r") as f:
        csv_reader = csv.DictReader(f)
        return {int(row['ID']):f"users/{row['File name']}.csv" for row in csv_reader}

async def send_random_frame(ctx, arg1, vid_file_name):
    arg1 = get_valid_range(arg1, 5)

    vidcap = cv2.VideoCapture(vid_file_name)
    n_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    for i in range(arg1):
        random_frame_ind = r.randint(10, n_frames)
        # set frame position
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_ind)
        success, image = vidcap.read()

        file_name = f"temp/{ctx.message.id}.jpg"
        if success and not os.path.exists(file_name):
            cv2.imwrite(file_name, image)
            file = discord.File(file_name)

            embed = discord.Embed(description=f"**Random frame{f' #{i+1}' if arg1 > 1 else ''}:**",
                                  color=discord.Color.purple())
            embed.set_image(url = "attachment://" + file.filename)
            embed.set_footer(
                text=f"pr trailer - Let me know if you have any suggestions!")

            await ctx.channel.send(file = file, embed = embed)
            os.remove(file_name)

@bot.event
async def on_message(message):
    if "trust" in message.content.casefold():
        file = discord.File("img/trust.gif")
        await message.channel.send(file=file)

    elif bot.user.mentioned_in(message) and "real" in message.content.casefold():
        await message.channel.send("Real.")

    await bot.process_commands(message)

@bot.command()
async def trailer(ctx, arg1=1):
    await send_random_frame(ctx, arg1, "img/trailer1.mp4")
            
@bot.command()
async def pray(ctx):
    file_names = get_users_file_names()

    if ctx.guild.id not in file_names.keys():
        embed = discord.Embed(
            description="**Server not registered**",
            color=discord.Color.red())
        embed.set_footer(text="pr pray - Contact me to add your server!")
        await ctx.channel.send(embed=embed)
        return
        
    embed = discord.Embed(
        description="**Current time for some server members:**",
        color=discord.Color.teal())

    with open(file_names[ctx.guild.id], "r") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
             embed.add_field(name=get_date(row['Timezone']),
                        value=f"<@{row['ID']}>",
                        inline=True)
    embed.set_footer(text="pr pray - Let me know if you have any suggestions!")
    await ctx.channel.send(embed=embed)

@bot.command()
async def gta7(ctx):
    chosen = {key:r.choice(value) for key, value in gta_keywords.items()}

    # if not chosen["Title"].isupper():
    #     chosen["Number"] = chosen["Number"].lower()

    # prefix = 'the trailer for ' if r.choice([True, False]) else ''
        
    # postfix = ''
    # if not prefix:
    #     postfix = ' trailer'

    prefix = ''
    postfix = ' Trailer 2'
    
    timeline = chosen["Random timeline"]() if r.choice([True, False]) else chosen["Timeline"]

    final_string = f"{chosen['Company']} will {chosen['Release']} \"{prefix}{chosen['Title']} {chosen['Number']}{postfix}\" {timeline}, {chosen['Affirmation']} {chosen['Bro']}"

    embed = discord.Embed(
        description="**Accurate GTA VI reveal date predicition:**",
        color=discord.Color.purple())
    embed.add_field(
        name=final_string,
        value=chosen['Denial'],
        inline=False
    )
    embed.set_footer(text="pr gta6")
    await ctx.channel.send(embed=embed)

@bot.command()
async def gta6(ctx):
    await gta7(ctx)

@bot.command()
async def lucia(ctx, arg1=1):
    await send_random_photo_from_dir(ctx, "lucia", arg1)

@bot.command()
async def sam(ctx, arg1=1):
    await send_random_photo_from_dir(ctx, "sam", arg1)

@bot.command()
async def jason(ctx, arg1=1):
    await send_random_photo_from_dir(ctx, "jason", arg1)

#KEEPING THE BOT RUNNING
keep_alive()

try:
    bot.run(token)
except discord.errors.HTTPException as HTTPException:
    if HTTPException.status == 429:
        print("The bot is being rate limited, trying to restart")
        os.system("kill 1")
        os.system("python restarter.py")
    else:
        raise