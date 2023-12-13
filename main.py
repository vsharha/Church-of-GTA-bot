import csv
import os
import random as r
from datetime import datetime as dt

import pytz

import discord
from discord.ext import commands

from gta_keywords import gta_keywords


# BOT SETTINGS


token = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("pr ", "PR ", "Pr ", "pR "), case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    # with open("users.csv", "r") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         print(get_date(row["Timezone"]), row["Name"])
        
    print("Initiated.")


# HELP COMMAND


help_command_values = (
    ("pr help", "Show this message"),
    ("pr pray", "See the current time for some server members"),
    ("pr gta6", "Get an accurate Trailer 2 release date prediction"),
    ("pr trailer (1-10)", "Get random frames from Trailer 1"),
    ("pr [sam/lucia/jason] (1-10)", "Get random pictures of Sam Houser, Lucia or Jason"),
    ("pr suggest (suggestion)", "Suggest a feature for the bot")
)

other_features_values = (
    ("Any message containing `trust`", "Responds with a gif from Trailer 1"),
    ("Any message containing a mention to the bot and `real` or `fake`", "Responds randomly with `Real`, `Fake` or `x% real`")
)

class my_help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(description="**List of available commands:**",
                              color=discord.Color.dark_green())
        for i in help_command_values:
            embed.add_field(name=f"• `{i[0]}`", value=i[1], inline=False)
        await self.context.send(embed=embed)

        embed = discord.Embed(description="**Other features of the bot:**",
                              color=discord.Color.dark_green())
        for i in other_features_values:
            embed.add_field(name=f"• {i[0]}", value=i[1], inline=False)
        add_embed_links(embed)
        embed.set_footer(text="pr help")
        await self.context.send(embed=embed)


bot.help_command = my_help()


# FUNCTIONS


def add_embed_links(embed):
    embed.add_field(name = "Links", value = "[Add Me to Your Server](https://discord.com/api/oauth2/authorize?client_id=997899986668888155&permissions=0&scope=bot) • [Join the Church of GTA](https://discord.gg/KUhB84NzHA)", inline = False)


def get_date(timezone):
    now = dt.now(pytz.timezone(timezone))
    date_str = now.strftime("%dth of %B, %I:%M %p"+(" (%H:%M)" if now.strftime('%H') != now.strftime('%I') else ""))
    if date_str[0] == "0":
        date_str = date_str[1:]
    if not 11 <= now.day <= 13:
        check = now.day % 10
        if 1 <= check <= 3:
            date_str = date_str.replace(
                "th", "st" if check == 1 else "nd" if check == 2 else "rd")
    return date_str


def get_date_international():
    now = dt.now(pytz.timezone("Etc/GMT"))
    return now.strftime("%y-%m-%d %H:%M:%S")


def get_valid_range(num, maxi):
    try:
        num = int(num)
    except ValueError:
        return 1
        
    if num <= 0:
        return 1
    if num > maxi:
        return maxi
    return num


async def send_random_photo_from_dir(ctx, dir, arg1, maxi=10):
    arg1 = get_valid_range(arg1, maxi)
        
    for i in range(arg1):
        file = discord.File(f"img/{dir}/{r.choice(os.listdir('img/'+dir))}")
    
        embed = discord.Embed(description=f"**{dir.capitalize()} image{f' #{i+1}' if arg1 > 1 else ''}:**",
                              color=discord.Color.teal())
        embed.set_image(url = "attachment://" + file.filename)
        embed.set_footer(
            text=f"pr {dir} - Let me know if you have any suggestions!")
        
        await ctx.channel.send(file=file, embed=embed)


@bot.event
async def on_message(message):
    msg_content = message.content.casefold()
    
    if "trust" in msg_content:
        file = discord.File("gif/trust.gif")
        await message.channel.send(file=file)
        return

    elif bot.user.mentioned_in(message) and ("real" in msg_content or "fake" in msg_content):
        match(r.randint(0,2)):
            case 0:
                msg = r.choice(["Real.", "Yeah."])
            case 1:
                msg = r.choice(["Fake.", "Nah."])
            case 2:
                msg = f"{r.randint(1,99)}% real."
        await message.channel.send(msg)
        return

    await bot.process_commands(message)


# COMMANDS


@bot.command()
async def pray(ctx):
    valid_users = 0
    
    if ctx.guild:
        embed = discord.Embed(
            description="**Current time for some server members:**",
            color=discord.Color.teal())
        
        with open("users.csv", "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                member = ctx.guild.get_member(int(row['ID']))
                if member:
                    valid_users += 1
                    try:
                        date = get_date(row['Timezone'])
                    except commands.errors.CommandInvokeError.UnknownTimeZoneError:
                        date = "Error"
                    embed.add_field(name=date, value=member.mention, inline=True)
                
    if not valid_users:
        embed = discord.Embed(
            description="**Server not registered**",
            color=discord.Color.red())
        embed.set_footer(text="pr pray - Contact me to add your server!")
        await ctx.channel.send(embed=embed)
        return
        
    add_embed_links(embed)
    embed.set_footer(text="pr pray - Let me know if you have any suggestions!")
    await ctx.channel.send(embed=embed)    


@bot.command(aliases=['gta7'])
async def gta6(ctx):
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
    # add_embed_links(embed)
    embed.set_footer(text="pr gta6")
    await ctx.channel.send(embed=embed)


@bot.command()
async def suggest(ctx, *args):
    if not args:
        embed = discord.Embed(description="**Error**", color=discord.Color.red())
        embed.add_field(name="No suggestion provided", value="Use this command again and provide a suggestion")
        embed.set_footer(text="pr suggest")
        await ctx.channel.send(embed=embed)
        return
        
    suggestion = " ".join(args)

    fieldnames = ("Date","ID","Name","Suggestion")

    file_path = "suggestions.csv"
    
    with open(file_path, "a+") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not os.path.getsize(file_path):
            writer.writeheader()            
        
        writer.writerow(dict(zip(fieldnames, [get_date_international(), ctx.message.author.id, ctx.message.author, suggestion])))

    embed = discord.Embed(description="**You are the best**", color=discord.Color.green())
    embed.add_field(name="Thank you for your suggestion", value="If you have any more, don't hesitate to use this command")
    embed.set_footer(text="pr suggest")
    await ctx.channel.send(embed=embed)


# Commands that are based on functions
@bot.command()
async def gta(ctx, arg1):
    arg1 = int(arg1)
    if arg1 in (6, 7):
        await gta6(ctx)


@bot.command()
async def trailer(ctx, arg1=1):
    # await send_random_frame(ctx, arg1, "vid/1080.mp4")
    await send_random_photo_from_dir(ctx, "trailer", arg1)


@bot.command()
async def lucia(ctx, arg1=1):
    await send_random_photo_from_dir(ctx, "lucia", arg1)


@bot.command()
async def sam(ctx, arg1=1):
    await send_random_photo_from_dir(ctx, "sam", arg1)


@bot.command()
async def jason(ctx, arg1=1):
    await send_random_photo_from_dir(ctx, "jason", arg1)


# RUNNING THE BOT


bot.run(token)


# Requires cv2


# async def send_random_frame(ctx, arg1, vid_file_name):
#     arg1 = get_valid_range(arg1, 5)

#     vidcap = cv2.VideoCapture(vid_file_name)
#     n_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
#     for i in range(arg1):
#         random_frame_ind = r.randint(10, n_frames)
#         # set frame position
#         vidcap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_ind)
#         success, image = vidcap.read()

#         file_name = f"{ctx.message.id}.jpg"
#         if success and not os.path.exists(file_name):
#             cv2.imwrite(file_name, image)
#             file = discord.File(file_name)

#             embed = discord.Embed(description=f"**Random frame{f' #{i+1}' if arg1 > 1 else ''}:**",
#                                   color=discord.Color.purple())
#             embed.set_image(url = "attachment://" + file.filename)
#             embed.set_footer(
#                 text="pr trailer - Let me know if you have any suggestions!")

#             await ctx.channel.send(file = file, embed = embed)
#             os.remove(file_name)
