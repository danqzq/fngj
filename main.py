import discord
from discord.ext import commands, tasks
import asyncio
import random
from webserver import keep_alive
import os
from replit import db
from datetime import datetime

jamdate = datetime.strptime('Jan 18 2021  00:00', '%b %d %Y %H:%M')

def listToString(s):
    str1 = ""  
    for ele in s:  
        str1 += ele
    return str1

nowdate = datetime.now()
count = int((jamdate-nowdate).total_seconds())

days = count//86400
hours = (count-days*86400)//3600
minutes = (count-days*86400-hours*3600)//60
seconds = count-days*86400-hours*3600-minutes*60
print("{} days {} hours {} minutes {} seconds left".format(days, hours, minutes, seconds))

client = commands.Bot(command_prefix='!')

text_file = open("games.txt", "r")
lines = text_file.readlines()
fngj_games = listToString(lines).split()
text_file.close()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="people stress out for 3 hours straight"))


possible_color = [discord.Colour.red(), discord.Colour.green(), discord.Colour.blue()]

client.remove_command("help")

@client.command(name='help',
                aliases=['helpme'],
                pass_context=True)
async def help(context):
    channel = client.get_channel(752099416214601778)
    embed = discord.Embed(
        title="Command list:",
        description=("**ask** Answers from the beyond.\n\n **help** Shows this message.\n\n **jam** Sends the jam link.\n\n **lol** Shows how many times lol has been said.\n\n **lvl** Sends the level number of user.\n\n **removerole** Used for removing roles [unityhelper, godothelper, unrealhelper, streamwatcher or jammer]\n\n **role** Used for getting roles [unityhelper, godothelper, unrealhelper, streamwatcher or jammer]\n\n **xp** Sends the level number of user."),
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)

@client.command(name='ask',
                aliases=['ask-bot', 'askbot', 'askfridaynightbot'],
                pass_context=True)
async def eight_ball(context):
    channel = client.get_channel(752099416214601778)
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'YES',
        'No, never',
        'Probably not',
        'As I see it, yes',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don’t count on it',
        'It is certain',
        'It is decidedly so',
        'Most likely',
        'My reply is no',
        'My sources say no',
        'Signs point to yes',
        'Very doubtful',
        'Without a doubt',
        'Yes.',
        'Yes – definitely',
        'You may rely on it',
    ]
    embed = discord.Embed(
        description=(random.choice(possible_responses) + " " + context.message.author.mention),
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Jammer")
    await member.send(f"Welcome to the Friday Night Game Jam Discord Server, @{member}. Make sure to check out the #rules channel before sending messages to the text channels.")
    await member.add_roles(role)

@client.command(name='lvl',
                aliases=['level', 'user-level'],
                pass_context=True)
async def lvl(context):
    channel = client.get_channel(752099416214601778)
    embed = discord.Embed(
        description=("Your level is: {}".format(str(int(db[context.message.author.id] / 25) + 1) + " " + context.message.author.mention)),
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)

@client.command(name='xp',
                aliases=['exp', 'experience'],
                pass_context=True)
async def xp(context):
    channel = client.get_channel(752099416214601778)
    embed = discord.Embed(
        description=("Your experience is: {}".format(str(db[context.message.author.id]) + " " + context.message.author.mention)),
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)

@client.command(name='rank',
                aliases=['place'],
                pass_context=True)
async def rank(context):
    channel = client.get_channel(752099416214601778)
    i = 1
    usersLevels = []
    for member in db:
        if not member.isnumeric():
            continue
        usersLevels.append(db[member])
    usersLevels = sorted(usersLevels, reverse=True)
    for level in usersLevels:
        if level == db[context.message.author.id]:
            break
        else:
            i += 1
    place = ""
    if i % 10 == 1:
        place = str(i) + "st"
    elif i % 10 == 2:
        place = str(i) + "nd"
    elif i % 10 == 3:
        place = str(i) + "rd"
    else:
        place = str(i) + "th"
    embed = discord.Embed(
        description="You are in the " + place + " place!",
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)

@client.command(name='leaderboard',
                aliases=['lb', 'top5'],
                pass_context=True)
async def leaderboard(context):
    channel = client.get_channel(752099416214601778)
    i = 1
    usersLevels = []
    users = []
    for member in db:
        if not member.isnumeric():
            continue
        usersLevels.append(db[member])
        users.append(int(member))
    usersDict = dict(zip(usersLevels, users))
    usersLevels.sort(reverse=True)
    desc = ""
    for level in usersLevels:
        if i > 10:
            break
        desc += str(i) + f". {await client.fetch_user(usersDict[usersLevels[i - 1]])}" + f" - Level {str(int(usersLevels[i - 1] / 25) + 1)}" + "\n"
        i += 1
    embed = discord.Embed(
        title="Leaderboard",
        description=desc,
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)

@client.command(name='lol',
                aliases=['Lol', 'LOL', 'lel', 'lOL', 'LoL', 'loL'],
                pass_context=True)
async def lol(context):
    channel = client.get_channel(753245178499694743)
    embed = discord.Embed(
        title=("LOL has been said {} times".format(db["lol"])),
        colour= random.choice(possible_color)
    )
    await channel.send(embed=embed)

@client.command(name='role',
                aliases=['giverole'],
                pass_context=True)
async def giverole(context):
    channel = client.get_channel(752099416214601778)
    role = discord.utils.get(context.message.author.guild.roles, name="Jammer")
    if "unityhelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Unity Helper")
        await channel.send("{} was given the Unity Helper role!".format(context.message.author.mention))
    elif "godothelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Godot Helper")
        await channel.send("{} was given the Godot Helper role!".format(context.message.author.mention))
    elif "unrealhelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Unreal Helper")
        await channel.send("{} was given the Unreal Helper role!".format(context.message.author.mention))
    elif "streamwatcher" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Stream Watcher")
        await channel.send("{} was given the Stream Watcher role!".format(context.message.author.mention))
    elif "jammer" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Jammer")
        await channel.send("{} was given the Jammer role!".format(context.message.author.mention))
    elif "webdevhelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="WebDev Helper")
        await channel.send("{} was given the WebDev Helper role!".format(context.message.author.mention))
    await context.message.author.add_roles(role)

@client.command(name='removerole',
                aliases=['norole'],
                pass_context=True)
async def removerole(context):
    channel = client.get_channel(752099416214601778)
    role = discord.utils.get(context.message.author.guild.roles, name="Unity Helper")
    if "unityhelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Unity Helper")
        await channel.send("{} is not a Unity Helper anymore.".format(context.message.author.mention))
    elif "godothelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Godot Helper")
        await channel.send("{} is not a Godot Helper anymore.".format(context.message.author.mention))
    elif "unrealhelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Unreal Helper")
        await channel.send("{} is not a Unreal Helper anymore.".format(context.message.author.mention))
    elif "streamwatcher" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="Godot Helper")
        await channel.send("{} is not a Stream Watcher anymore.".format(context.message.author.mention))
    elif "webdevhelper" in context.message.content:
        role = discord.utils.get(context.message.author.guild.roles, name="WebDev Helper")
        await channel.send("{} is not a WebDev Helper anymore.".format(context.message.author.mention))
    await context.message.author.remove_roles(role)

@client.command(name='jam',
                aliases=['jamlink', 'gamejam', 'gamejamlink'],
                pass_context=True)
async def jam(context):
    channel = client.get_channel(752099416214601778)
    embed = discord.Embed(
        title=("{} days {} hours {} minutes {} seconds left".format(days, hours, minutes, seconds) + " until submissions close"),
        description=("https://itch.io/jam/friday-night-game-jam-2021-2"),
        colour= random.choice(possible_color)
    )
    embed.set_image(url="https://img.itch.zone/aW1hZ2UyL2phbS8xNzYxMi80MTMyMTI5LnBuZw==/original/QvwQAf.png")
    await channel.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "lol" in message.content.lower() or "lul" in message.content.lower() or "lel" in message.content.lower():
        db["lol"] = db["lol"] + 1
        if not message.channel.id == 753245178499694743:
            await message.add_reaction('🤣')

    if "indeed" in message.content.lower():
        if "suck" not in message.content.lower():
            await message.channel.send("Indeed!")

    if client.user.mentioned_in(message):
        await message.channel.send("Ay! Don't ping me, I'm watching **you**!")
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message.author.name))

    if "xd" in message.content.lower():
        await message.channel.send("XD")
        
    if "yeet" in message.content.lower():
        await message.channel.send("Yeet!")

    if "oof" in message.content.lower():
        embed = discord.Embed(colour= random.choice(possible_color))
        gif = ["https://media1.tenor.com/images/432261184122de5c0142153dbeac3387/tenor.gif", "https://media1.tenor.com/images/f9ef49b7c23c0bf3173ed6ec6e250e29/tenor.gif",
        "https://media.tenor.com/images/f7848864d04fb2be71cd890e9786f3f1/tenor.gif",
        "https://media.tenor.com/images/d158b92b24bae6c59fe60d2014bf01f4/tenor.gif",
        "https://media.tenor.com/images/3f487d1857dcc568a488fe40e79b0396/tenor.gif",
        "https://media.tenor.com/images/424b9f06757c1641d0f3495afd177e2e/tenor.gif",
        "https://media1.tenor.com/images/bb4ea4546c74488d8e1f2fa0a9ffdaf3/tenor.gif",
        "https://media1.tenor.com/images/66cf8ea326db942e2a5a882640676c1c/tenor.gif",
        "https://media.tenor.com/images/153e0f2d44b859b34a9877e67059bbbd/tenor.gif",
        "https://media.tenor.com/images/6bca13154e250cfe1cae7c2ba86ad39b/tenor.gif",
        "https://media1.tenor.com/images/f66dadf4c954d58dae44522284fdd8ca/tenor.gif",
        "https://media1.tenor.com/images/a1cbba015cc3601610268066628c8e80/tenor.gif",
        "https://media1.tenor.com/images/b76972d1e726e0f922534faa94a77db2/tenor.gif",
        "https://media1.tenor.com/images/593781b73bcd387855def06e71c8160f/tenor.gif"]
        embed.set_image(url=random.choice(gif))
        await message.channel.send(embed=embed)
        
    if "lmao" in message.content.lower():
        await message.channel.send("Lmao")

    if "please" in message.content.lower() or "pls" in message.content.lower():
        await message.channel.send("Yes please")

    if message.author.id not in db.keys():
        db[message.author.id] = 1
    db[message.author.id] = db[message.author.id] + 1
    if db[message.author.id] % 25 == 0 and db[message.author.id] > 24:
        channel = client.get_channel(752099416214601778)
        embed = discord.Embed(
                description=(message.author.mention + " has leveled up to level " + str(int(db[message.author.id] / 25) + 1) + "!"),
                colour= random.choice(possible_color)
            )
        await channel.send(embed=embed)

    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    if before.content != after.content:
        channel = client.get_channel(789039959301947392)
        msg = '**' + str(before.author) + ' edited a message in  '+ str(before.channel) + ' from**\n'+ str(before.content) + '** to **' + str(after.content)
        embed = discord.Embed(
        description = msg,
        colour = random.choice(possible_color)
        )
        await channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    channel = client.get_channel(789039959301947392)
    msg = '**' + str(message.author) + ' deleted a message in  '+ str(message.channel) + ':**\n'+ str(message.content)
    await channel.send(msg)

#@tasks.loop(hours=24)
#async def called_once_a_day():
#    channel = client.get_channel(748098949419630606)
#    await channel.send("**Game of the day:** " + random.choice(fngj_games))

#@called_once_a_day.before_loop
#async def before():
#    await client.wait_until_ready()
#    print("Game of the day has been announced.")

#called_once_a_day.start()

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)