print("Booting up...")

# Modules
from discord.ext import commands, tasks
import discord
import sys
import os
import asyncio
import random
import psutil
import platform
# Do not modify the below statement, this is
# to check whether this REPL has been forked
# or not. Feel free to remove these checks if
# you know what you are doing.

# Secret
#        (⛔ DO NOT PUT YOUR DISCORD BOT'S TOKEN HERE! ⛔)
my_secret = "DiscordToken"  # Follow these examples for better understanding: https://pbs.twimg.com/media/Fm9A39vXEAEhV7R?format=png  (legacy screenshot: https://pbs.twimg.com/media/Fe5Ik9eXkAAr20r?format=png)

# Set up some intents
intents = discord.Intents.default()
intents.message_content = True

banned_users = {"": "", "": ""}

# Variables
bot = commands.Bot(
    intents=intents,  # Required
    command_prefix="?",
    case_insensitive=True,  # e.g. !hElP
    strip_after_prefix=True, # e.g. ! help
    debug = False
)

# Dictionary to store the channel IDs for each guild
guild_channels = {}

bot.remove_command("help")

from itertools import cycle

guildss = len(bot.guilds)
userss = sum(guild.member_count for guild in bot.guilds)

statuses = cycle([f"Type ?help for commands!", "?help", "watching the support server", "none"])

cooldown = 120

bot_status = "🟡 Loading..."


@bot.command(help="Show bot statistics - Model CPU, Platform CPU, Use CPU, etc.", aliases=["status"])
async def stats(ctx):
    # CPU information
    cpu_info = f"Model CPU : {platform.processor()}\n"
    cpu_info += f"Platform CPU : {platform.system()} {platform.release()}\n"
    cpu_info += "Use CPU :\n"
    cpu_info += f"  CPU : {psutil.cpu_percent()}%\n"
    cpu_info += f"  RAM : {psutil.virtual_memory().percent}%\n"
    cpu_info += f"  Memory : {psutil.disk_usage('/').percent}%\n"

    # Version and other info
    version = ":tada: 1.4.0"
    made_with = "Python"
    created = "April 04, 2023"
    developer = "kno"
    ping = f"{bot.latency*1000:.0f}"
    client_id = bot.user.id
    client_tag = bot.user

    # Create the embed message
    embed = discord.Embed(title="Bot Statistics", color=0x00ff00)
    embed.add_field(name="CPU info", value=f"```{cpu_info}```", inline=False)
    embed.add_field(name="Version", value=version, inline=True)
    embed.add_field(name="Made with", value=made_with, inline=True)
    embed.add_field(name="Created", value=created, inline=False)
    embed.add_field(name="Developer", value=developer, inline=True)
    embed.add_field(name="Ping", value=f"{ping} ms", inline=True)
    embed.add_field(name="Client ID", value=client_id, inline=True)
    embed.add_field(name="Client Tag", value=f"{client_tag.name}#{client_tag.discriminator}", inline=True)
    embed.set_footer(text=bot_status)

    await ctx.send(embed=embed)


@bot.command(help="Change the bot status message", aliases=["changestatus"])
@commands.has_role(1093587741708656690)
async def change_status(ctx, *, new_status):
    global bot_status
    bot_status = new_status
    await ctx.send(f"Bot status has been updated to '{new_status}'")


@tasks.loop(seconds=40)
async def update_bot_status():
    global bot_status
    ping = f"{bot.latency*1000:.0f}ms"
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    if cpu_percent > 70:
        bot_status = "🔴 High CPU usage"
    elif memory_percent > 70:
        bot_status = "🔴 High memory usage"
    elif disk_percent > 70:
        bot_status = "🔴 High disk usage"
    else:
        bot_status = f"🟢 Working fast - {ping}"

    activity = discord.Game(name=bot_status)
    await bot.change_presence(activity=activity)


# Gateway Events
@bot.event
async def on_ready():
# Load coins data from coins.json
# with open("coins.json", "r") as f:
#    bot.currency = json.load(f)
    update_bot_status.start()
    print(f"✅ {bot.user}")
    await bot.change_presence(activity=discord.Game(name="?help"))
# Initialize the dictionary with the IDs of all guilds the bot is in
    for guild in bot.guilds:
        guild_channels[guild.id] = None
# Load coins data from coins.json

    while True:
        await bot.change_presence(activity=discord.Game(next(statuses)))
        await asyncio.sleep(cooldown)
    try:
        with open('suggestions_state.json', 'r') as f:
            data = json.load(f)
            for guild_id, enabled in data.items():
                guild = bot.get_guild(int(guild_id))
                if guild is not None:
                    suggestions_enabled[guild.id] = enabled
                    if enabled:
                        suggestion_channel[guild.id] = guild.text_channels[0]
                    else:
                        suggestion_channel[guild.id] = None
    except FileNotFoundError:
        print('File not found.')

@bot.event
async def on_disconnect():
    with open('suggestions_state.json', 'w') as f:
        data = {str(guild_id): enabled for guild_id, enabled in suggestions_enabled.items()}
        json.dump(data, f)

@bot.event
async def on_message(message):
    if not message.author.bot:
        # Increase the user's coin balance by 10 for every message they send
        bot.currency.setdefault(str(message.author.id), {"balance": 0})
        bot.currency[str(message.author.id)]["balance"] += 10
        # Save the updated currency data to the JSON file
        with open("currency.json", "w") as f:
            json.dump(bot.currency, f)
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    print("hooray")
    category = discord.utils.get(member.guild.categories, name='Welcome')
    welcome_channel = discord.utils.get(category.channels, name='welcome')
    await welcome_channel.send(f':wave: Hey there, {member.mention}!')

@bot.event
async def on_member_remove(member):
    category = discord.utils.get(member.guild.categories, name='Welcome')
    goodbye_channel = discord.utils.get(category.channels, name='goodbye')
    await goodbye_channel.send(f':sob: Goodbye, {member}!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        # Ignore errors for commands that do not exist 
        await ctx.send("<:error:1093315720626057299> That command does **not** exist!!")
        return

    # Send an error message to the user if a command has any other error
    await ctx.send(f"<:error:1093315720626057299> An error occurred. Try again later. For developers,```{error}```")




@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    guild = ctx.guild
    category = await guild.create_category('Welcome')

    welcome_channel = await guild.create_text_channel('welcome', category=category)
    await welcome_channel.send('Welcome channel created!')

    goodbye_channel = await guild.create_text_channel('goodbye', category=category)
    await goodbye_channel.send('Goodbye channel created!')


# Bot Commands
# List of bad words
bad_words = [
    "fuck", "shit", "bitch", "cunt", "nigga", "nigger", "suka", "rape", "dick",
    "cock", "sex", "danono", "daddy", "fvck",   "https://tenor.com",
  "https://giphy.com",
  "https://media.giphy.com",
  "https://media.tenor.com",
  "https://i.giphy.com",
  "https://i.tenor.com", "/view/chelsea-charms-boobs-milk-bigtits-breasts-gif-17946703", "breast", "boobs", "tits", "tit"
]


@bot.command(help="| Repeat what you want to say. /say urtexthere", aliases=["repeat", "talk"])
async def say(ctx, *, message):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Replace bad words with asterisks
    for word in bad_words:
        message = message.replace(word, "****" * len(word))
        
    # Censor parts of URLs
    for word in message.split():
        if "/" in word:
            word_parts = word.split("/")
            if len(word_parts) > 1:
                word_parts[1] = "*" * len(word_parts[1])
                message = message.replace(word, "/".join(word_parts))
    
    await ctx.send(message)
    say.usage = "?say {message}"
    say.example = "?say Hello!"


@bot.command(help="| Greet a user. /hey @user")
async def hey(ctx, *, user):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Check if user input is a mention of the bot itself
    if user == '<@1091789159556993217>':
        await ctx.send("Hey there, myself. Lol!")
    else:
        # Convert user input to lowercase
        user_input = user.lower()

        # Search for member in member list by converting name to lowercase
        member = next(
            (m for m in ctx.guild.members if m.name.lower() == user_input),
            None)

        # Check if user input is a mention or a member in the member list
        if member is not None:
            await ctx.send(f"Hey there, {member.mention}!")
        else:
            try:
                member = await commands.MemberConverter().convert(ctx, user)
                await ctx.send(f"Hey there, {member.mention}!")
            except commands.MemberNotFound:
                await ctx.send("Sorry, I couldn't find that user.")


@bot.command(help="| Ping a specific role. /mention @role")
async def mention(ctx, *, ping):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Check if ping is valid
    if ping in ["@everyone", "@here"] or ping.startswith("<@&"):
        await ctx.send(f"Pinging the {ping} role!")
    else:
        await ctx.send("Sorry, I couldn't find that role.")


import datetime


@bot.command(help="| Current Time")
async def time(ctx):
    now = datetime.datetime.now()
    await ctx.send(f"Current date and time is: {now}")


@bot.command()
async def age(ctx, birthdate):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) <
                                         (birthdate.month, birthdate.day))
    await ctx.send(f"Your age is: {age}")


@bot.command(help="| Kick a user from the server. /kick @user")
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    try:
        await member.kick()
        await ctx.send(f"{member.mention} has been kicked.")
    except discord.Forbidden:
        await ctx.send("I need the **Administrator** permissions to do that.")


@bot.command(help="| Shows all the permissions the bot has in this guild")
@commands.has_permissions(administrator=True)
async def permissions(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    permissions = ctx.guild.me.guild_permissions
    perms_list = []
    for perm, value in permissions:
        if value:
            perms_list.append(perm)
    await ctx.send(f"My permissions in this guild are: {', '.join(perms_list)}"
                   )


# Checks if the Secret exists in the Secrets tab



@bot.command(help="| Display the developers of the bot.")
async def devs(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    embed = discord.Embed(title="Developers",
                          color=random.randint(0, 0xFFFFFF))
    embed.add_field(name="kno#6139", value="<:bot_dev:1092900416863338647>")
    embed.add_field(name="adityaREDFLAG#5836",
                    value="<:utube:1092900378871353434>")
    await ctx.send(embed=embed)

@bot.command(help="| Owner Only")
async def botstatus(ctx, status: str = None, *, activity: str = None):
    if ctx.author.id != 681670759671791682:
        return await ctx.send("This command is only available to the bot owner.")
    if not status or not activity:
        return await ctx.send("<:error:1093315720626057299> Please provide the new status and activity")
    if status not in ["online", "idle", "dnd", "invisible"]:
        return await ctx.send("Invalid status. Please choose from: online, idle, dnd, invisible")
    await bot.change_presence(status=discord.Status[status], activity=discord.Game(name=activity))
    print(f"✅ Bot status set to {status} with activity: {activity}")
    await ctx.send(f"Bot status set to {status} with activity: {activity}")


@bot.command()
async def shutdown(ctx):
    if ctx.author.id != 681670759671791682:
        return await ctx.send("This command is only available to the bot owner.")
    await ctx.send("Shutting down the bot...")
    await ctx.send("<:success:1093315717832659065> Bot shutdown.")
    print("✅ Bot shutdown succesfully.")
    await bot.close()


import traceback

@bot.command()
async def debug(ctx):
  if ctx.author.id == 681670759671791682:
    try:
        # Set debug mode on or off
        bot.debug = not bot.debug
        
        # Send confirmation message
        if bot.debug:
            await ctx.send("<:success:1093315717832659065> Debug mode enabled.")
        else:
            await ctx.send("<:success:1093315717832659065> Debug mode disabled.")
    except Exception as e:
        # Send error message
        traceback.print_exc()
        await ctx.send(f"<:error:1093315720626057299> Error: {str(e)}")

@bot.command()
async def eval(ctx, *, code):
  if ctx.author.id == 681670759671791682:
    try:
        await ctx.send("Working...")
        # Evaluate the provided Python code
        result = eval(code)
        
        # Send the result as a message
        await ctx.send(result)
    except Exception as e:
        # Send error message
        traceback.print_exc()
        await ctx.send(f"<:error:1093315720626057299> Error: {str(e)}")
      
@bot.command()
async def embed(ctx, titler='ZONO Autofill', description='ZONO Autofill', author='ZONO Autofill', color=None, thumbnail=None, footer=None):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    if color:
        try:
            color = discord.Color(int(color, 16))
        except ValueError:
            color = discord.Color(random.randint(0, 0xFFFFFF))
    else:
        color = discord.Color(random.randint(0, 0xFFFFFF))
        
    embed = discord.Embed(title=titler, description=description, color=color)
    embed.set_author(name=author)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if footer:
        embed.set_footer(text=footer)
    await ctx.send(embed=embed)

ALLOWED_DOMAINS = ["forms.office.com", "www.qualtrics.com", "docs.google.com", "www.surveymonkey.com", "www.typeform.com", "qualtrics.com", "google.com", "surveymonkey.com", "typeform.com", "forms.google.com", "forms.gle"]
DISCORD_DOMAINS = ["http://", "https://", "discord"]

import idna

@bot.command(help="| Create a form embed")
@commands.has_permissions(administrator=True)
async def forms(ctx, form_url, timeout=60):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        # Check if the URL is safe
        if not is_url_safe(form_url):
            raise ValueError("<:error:1093315720626057299> An error occurred. That URL might possibly not be the one of the following: ```" + ", ".join(ALLOWED_DOMAINS) + "```")
        
        # Create the embed and button
        embed = discord.Embed(title="Discord Forms", description="Click the button below to fill out the form!", color=discord.Color.red())
        message = await ctx.send(embed=embed, view=discord.ui.View(timeout=timeout))
        button = discord.ui.Button(style=discord.ButtonStyle.green, label="Open Form", url=form_url)
        view = discord.ui.View()
        view.add_item(button)
        await message.edit(view=view)

        # Wait for a response from the user
        await bot.wait_for('message', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await message.edit(view=None)
        await ctx.send("Timed out!")
    except ValueError as e:
        await ctx.send(str(e))
    except:
        await ctx.send("<:error:1093315720626057299> An error occurred. That URL might possibly not be the one of the following: ```" + ", ".join(ALLOWED_DOMAINS) + "```")

def is_url_safe(url):
    # Check if the URL starts with "http", "https", or "discord"
    if not url.startswith(tuple(DISCORD_DOMAINS)):
        return False
    
    # Check if the URL contains an allowed domain
    for domain in ALLOWED_DOMAINS:
        if domain in url:
            return True
    
    # Return False if the URL does not contain an allowed domain
    return False


@bot.command(help="| Show bot info", aliases=["info", "information"])
async def botinfo(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    process = psutil.Process(os.getpid())
    ram_usage = process.memory_full_info().uss / 1024 ** 2
    guilds = len(bot.guilds)
    users = sum(guild.member_count for guild in bot.guilds)

    embed = discord.Embed(title="<:info:1095311626586046465> ZONO Bot Information", color=0xFFD700)
    embed.add_field(name="RAM Usage (MB)", value=f"{ram_usage:.2f}")
    embed.add_field(name="Guilds", value=str(guilds))
    embed.add_field(name="Users", value=str(users))
    embed.add_field(name="Support", value="<:email:1095314581385125888> Email: Zono.Bot@courvix.com\n[<:roadblox:1095311889896058943> View My Roblox Profile](https://www.roblox.com/users/4507594963/profile)", inline=False)
    embed.add_field(name="About", value="<:py:1095314624548704426> I am a bot programmed fully in Python. I can do many things, but not exactly everything.")

    await ctx.send(embed=embed)

@bot.command(help="| Show info on a user")
async def userinfo(ctx, user: discord.Member):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    if user is None:
        await ctx.send("<:error:1093315720626057299> Please mention a user")
        return
    embed = discord.Embed(title="User Info", color=0xFFD700)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Name", value=user.name)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Status", value=str(user.status).title())
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%m/%d/%Y, %H:%M:%S"))
    embed.add_field(name="Created Account", value=user.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
    await ctx.send(embed=embed)


@bot.command()
async def roles(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    if ctx.author.guild_permissions.manage_roles:
        embed = discord.Embed(title="Server Roles", color=0xFFD700)
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                members = len(role.members) if len(role.members) > 0 else "Failed to load Members"
                embed.add_field(name=role.name, value=f"{role.mention}\nMembers: {members}", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="<:error:1093315720626057299> Error", description="You don't have the required permissions to use this command. ", color=0xFF0000)
        await ctx.send(embed=embed)

@bot.command(help="| Click the button to reveal a surprise!")
async def surprise(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    surprise_button = discord.ui.Button(style=discord.ButtonStyle.red, label="Click me!")
    surprise_view = discord.ui.View()
    surprise_view.add_item(surprise_button)
    
    message = await ctx.send("Click the button to reveal a surprise!", view=surprise_view)
    
    def check(res):
        return res.user == ctx.author and res.channel == ctx.channel
    
    try:
        interaction = await bot.wait_for("button_click", check=check, timeout=30.0)
        await interaction.respond(content="🎉 SURPRISE! 🎉", type=discord.InteractionType.ChannelMessageWithSource)
    except asyncio.TimeoutError:
        await ctx.send(content="Sorry, you took too long to click the button!")
    except discord.InteractionException:
        await message.edit(content="Something went wrong with the button interaction.")
    finally:
        surprise_view.clear_items()
        surprise_view.stop()

@bot.command()
@commands.has_permissions(administrator=True)
async def newrole(ctx, name, color: discord.Color):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Create a new role with the given color and name
    new_role = await ctx.guild.create_role(name=name, color=color)

    # Add the new role to the author's roles
    author = ctx.author
    await author.add_roles(new_role)

    await ctx.send(f"New role created with color {color} and added to {author.mention}")

@bot.command()
async def quote(ctx, aliases=["focus"]):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    quotes = [
        "Be yourself; everyone else is already taken. ― Oscar Wilde",
        "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe. ― Albert Einstein",
        "You only live once, but if you do it right, once is enough. ― Mae West",
        "Be the change that you wish to see in the world. ― Mahatma Gandhi",
        "In three words I can sum up everything I've learned about life: it goes on. ― Robert Frost"
    ]
    quote = random.choice(quotes)

    embed = discord.Embed(title="Random Quote", description=quote, color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(help="| Show info about the server")
async def serverinfo(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    guild = ctx.guild
    roles = [role for role in guild.roles if not role.is_bot_managed()]
    online = len([member for member in guild.members if not member.bot and member.status != discord.Status.offline])
    total_members = guild.member_count - len([member for member in guild.members if member.bot])
    bots = len([member for member in guild.members if member.bot])
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    
    owner = await guild.fetch_member(guild.owner_id)

    embed = discord.Embed(title="Server Information", color=0xFFD700)
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Name", value=guild.name, inline=False)
    embed.add_field(name="Owner", value=owner.mention)
    embed.add_field(name="Roles", value="Please use the /roles command.")
    embed.add_field(name="Members", value=f"{total_members} members\n{bots} bots\nFailed to load online")
    embed.add_field(name="Channels", value=f"{text_channels} text channels\n{voice_channels} voice channels")
    embed.add_field(name="Created On", value=guild.created_at.strftime("%m/%d/%Y, %H:%M:%S"), inline=False)

    await ctx.send(embed=embed)

import requests

@bot.command(help="| Sends a random meme from the internet")
async def meme(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    url = "https://meme-api.com/gimme"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        meme_url = data['url']
        meme_title = data['title']
        meme_subreddit = data['subreddit']
        meme_author = data['author']
        
        embed = discord.Embed(title=meme_title, color=0xFF4500)
        embed.set_image(url=meme_url)
        embed.set_footer(text=f"From r/{meme_subreddit} by u/{meme_author}")
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("<:error:1093315720626057299> Couldn't fetch a meme. Try again later.")

@bot.command(help="| Sends a random meme from the internet at a user-defined frequency", aliases=["automemer", "memerauto"])
async def automeme(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send("How frequently do you want to receive memes? Enter a number between 2 and 30.")
    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        freq = int(msg.content)
        if freq < 2 or freq > 30:
            await ctx.send("<:error:1093315720626057299> Invalid input. Please enter a number between 2 and 30.")
            return
    except asyncio.TimeoutError:
        await ctx.send("<:error:1093315720626057299> Timed out. Please try again later.")
        return
    except ValueError:
        await ctx.send("<:error:1093315720626057299> Invalid input. Please enter a number between 2 and 30.")
        return
    
    await ctx.send(f"<:success:1093315717832659065> You will now receive memes every {freq} minutes. Use the `stop` command to stop receiving memes.")
    
    while True:
        url = "https://meme-api.com/gimme"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            meme_url = data['url']
            meme_title = data['title']
            meme_subreddit = data['subreddit']
            meme_author = data['author']
            
            embed = discord.Embed(title=meme_title, color=0xFF4500)
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"From r/{meme_subreddit} by u/{meme_author}")
            embed.set_author(name="Automeme")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:error:1093315720626057299> Couldn't fetch a meme. Try again later.")
        
        await asyncio.sleep(freq * 60)

@bot.command(help="| Tells a random joke", aliases=["funny", "fun"])
async def joke(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Fetch a random joke from the API
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        joke_setup = data['setup']
        joke_punchline = data['punchline']

        # Create an embed to send the joke
        embed = discord.Embed(title="Joke", description="Here's a random joke for you", color=0xFF4500)
        embed.add_field(name="Setup", value=joke_setup, inline=False)
        embed.add_field(name="Punchline", value=joke_punchline, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("<:error:1093315720626057299> Couldn't fetch a joke. Try again later.")

@bot.command(help="| Ask the 8ball a question", aliases=["ask", "question", "8ball"])
async def eball(ctx, *, question):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    responses = ['no', 'yes', 'Ask one more time!', 'Hell no!', 'Why!', 'Hahha', 'Nah', 'Bruh', '69', "aaaaa"]
    response = random.choice(responses)
    
    embed = discord.Embed(title='8ball', description=f'Question: {question}\n My Answer: ||{response}||', color=0xFF4500)
    embed.set_footer(text='8ball has spoken!')
    
    await ctx.send(embed=embed)
    await ctx.send("<:success:1093315717832659065> 8ball has spoken!")

@bot.command(name="clear", aliases=["purge", "clean"])
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, num_messages: int):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    if num_messages <= 0:
        await ctx.send("<:error:1093315720626057299> I can't delete 0 messages.")
        return
    elif num_messages > 100:
        await ctx.send("<:error:1093315720626057299> I can't delete more than 100 messages at once!")
        return
    
    await ctx.message.delete()
    deleted_messages = await ctx.channel.purge(limit=num_messages)
    await asyncio.sleep(1)
    success_message = await ctx.send(f"<:success:1093315717832659065> Successfully deleted {len(deleted_messages)} message(s) :D")
    await asyncio.sleep(1)
    await success_message.delete(delay=5)

bot_admin_role_id = 1093587741708656690  # replace with your bot admin role ID
guild_id = 1093282183994675220  # replace with your guild ID

# Define success and error emojis
success_emoji = 'your-emoji-here'  # green check mark
error_emoji = 'your-emoji-here'  # red X mark

# Check if the user has the bot admin role
def is_bot_admin(ctx):
    bot_admin_role = discord.utils.get(ctx.guild.roles, id=bot_admin_role_id)
    return bot_admin_role in ctx.author.roles

# Define the bot panel command
@bot.command(name="botpanel", aliases=["panel", "admin"])
@commands.check(is_bot_admin)
async def botpanel(ctx):
  await ctx.send("unavaliable")

# Handle check failures
@botpanel.error
async def botpanel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"{error_emoji} You cannot use this command!")

@bot.command(help="See how fast the bot is.", aliases=["pingpong", "ping_pong"])
async def ping(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Send a message to the context channel and record the time
    before = discord.utils.utcnow()
    message = await ctx.send(':ping_pong:  Pong!')
    # Calculate the time difference between when the message was sent and when it was edited
    latency = discord.utils.utcnow() - before
    # Edit the original message to include the latency
    await message.edit(content=f':ping_pong: Pong! Latency: {latency.total_seconds():.1f} seconds')
    ping.usage = "?ping"
    ping.example = "?ping"

@bot.command(aliases=[" helphelp","helphelp","how","helphelphelphelp"])
async def help(ctx, command_name=None):
    if command_name:
        # If a command name is provided, try to find the command object
        command = bot.get_command(command_name)

        if not command:
            # If the command doesn't exist, send an error message
            await ctx.send(f"{ctx.author.mention} Command not found.")

        else:
            # If the command exists, create an embed with detailed information
            aliases = ", ".join(command.aliases) or "None"
            usage = command.usage or "None"
            example = f"{usage}\nExample: {usage.replace('<', '@').replace('>', 'Zono')}"
            embed = discord.Embed(title=f"Command: {command.name}", color=0xffd700)
            embed.add_field(name="Aliases", value=aliases[:1024], inline=False)
            embed.add_field(name="Usage", value=example[:1024], inline=False)
            embed.add_field(name="Description", value=command.help or "None", inline=False)
            await ctx.send(embed=embed)

    else:
        # If no command name is provided, list all available commands
        categories = {}

        # Loop through all the bot commands
        for command in bot.commands:
            # Check if the command is hidden or not
            if not command.hidden:
                # Get the command category
                category = command.cog_name or "No Category"

                # Check if the category already exists in the dictionary
                if category not in categories:
                    categories[category] = []

                # Add the command name and description to the category
                categories[category].append((command.name, command.help))

        # Create the embed
        embed = discord.Embed(title="Commands", color=0xffd700)

        # Loop through the command categories
        for category, commands in categories.items():
            # Create a list of commands with their descriptions
            command_list = "\n".join([f"**{name}** - {description}" for name, description in commands])

            # Add the command list to the embed
            embed.add_field(name=category, value=command_list[:1024], inline=False)

        # Send the embed
        await ctx.send(embed=embed)

@bot.command()
async def rblxsetup(ctx, channel: discord.TextChannel):
    try:
        # Create the webhook in the specified channel
        webhook = await channel.create_webhook(name="Bloxia Webhook | ZONO Connector")

        # Send the webhook URL to the user via DM
        try:
            await ctx.author.send(f"Webhook created successfully: {webhook.url}")
        except discord.errors.Forbidden:
            # If DMs are disabled, ping the user in the specified channel with the webhook URL
            await ctx.send(f"{ctx.author.mention}, Webhook created successfully: {webhook.url}")

    except discord.errors.Forbidden:
        # If the bot doesn't have permission to create webhooks, send an error message
        await ctx.send("I don't have permission to create webhooks in that channel.")


@bot.command(help="See how fast the bot is.", aliases=["pingpongauto", "ping_pong_auto"])
async def latencyauto(ctx):
    
    while True:
        # Send a message to the context channel and record the time
        before = discord.utils.utcnow()
        message = await ctx.send(':ping_pong:  Pong!')
        # Calculate the time difference between when the message was sent and when it was edited
        latency = discord.utils.utcnow() - before
        
        if latency.total_seconds() > 4:
            # Get the role object for the role with the ID 1093282588044574842
            role = ctx.guild.get_role(1093282588044574842)
            # Mention the role and send the message
            await ctx.send(f"{role.mention} Latency higher than expected!")
        
        # Edit the original message to include the latency
        await message.edit(content=f':ping_pong: Pong! Latency: {latency.total_seconds():.1f} seconds')
        
        # Pause the execution of the function for 5 seconds
        await asyncio.sleep(5)

@bot.command(help="Displays all command executions in all guilds")
@commands.has_role(1093587741708656690)
async def logs(ctx):
    # Update the dictionary with the new channel ID for all guilds
    for guild in bot.guilds:
        guild_channels[guild.id] = ctx.channel.id
    
    await ctx.send("<:success:1093315717832659065> Logging all command executions in all guilds...")

@bot.event
async def on_command(ctx):
    # Get the channel ID for the current guild from the dictionary
    channel_id = guild_channels.get(ctx.guild.id)
    
    if channel_id is not None:
        # Get the role object for the role with the ID 1093587741708656690
        role = ctx.guild.get_role(1093587741708656690)
        # Send a message to the specified channel with information about the user and the command executed
        await bot.get_channel(channel_id).send(f"<:fix:1095311747327463495> Command executed by {ctx.author} ({ctx.author.id}) in guild {ctx.guild.name} ({ctx.guild.id}): {ctx.message.content}")

@bot.command()
async def gamepass(ctx, *, username):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    api_url = f"https://api.roblox.com/users/get-by-username?username={username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        user_id = response.json().get("Id")
        gamepass_id = 161291841
        gamepass_url = f"https://www.roblox.com/game-pass/{gamepass_id}"
        gamepass_response = requests.get(gamepass_url, params={"userId": user_id})
        if gamepass_response.status_code == 200:
            if gamepass_response.json()["success"]:
                await ctx.send(f"{username} owns the gamepass!")
            else:
                await ctx.send(f"{username} does not own the gamepass.")
        else:
            await ctx.send(f"Failed to check gamepass for {username}.")
    else:
        await ctx.send(f"Failed to get user ID for {username}.")

@bot.command()
async def ticket(ctx):
    # Define a list of channel options to display in the select menu
    channel_options = [discord.SelectOption(label=c.name, value=str(c.id)) for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]

    # Create the select menu with the channel options
    select = discord.ui.Select(options=channel_options, placeholder="Please select a channel", min_values=1, max_values=1)

    # Create the embed with the select menu as an action row
    embed = discord.Embed(title="Ticket Setup", description="Please select a channel to create the ticket in")
    action_row = discord.ui.ActionRow(select)
    message = await ctx.send(embed=embed, components=[action_row])

    # Wait for the user to select a channel
    try:
        interaction = await bot.wait_for("select_option", check=lambda i: i.component == select and i.user == ctx.author, timeout=30.0)
    except asyncio.TimeoutError:
        await message.edit(content="Ticket setup timed out", components=[])
        return

    # Get the selected channel and remove the select menu
    channel = bot.get_channel(int(interaction.values[0]))
    await interaction.respond(content=f"You selected {channel.mention}", type=discord.InteractionType.UpdateMessage, components=[])

    # Create the ticket channel in the selected category
    category = discord.utils.get(ctx.guild.categories, name="Tickets")
    if category is None:
        category = await ctx.guild.create_category("Tickets")

    ticket_number = len(category.channels) + 1
    ticket_channel = await category.create_text_channel(f"ticket-{ticket_number}", topic=f"Ticket created by {ctx.author.name}")
    await ticket_channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ticket_channel.set_permissions(ctx.author, send_messages=True)

    # Send a message to the ticket channel to confirm it was created
    confirmation_message = f"Ticket channel {ticket_channel.mention} has been created for {ctx.author.mention}"
    await ticket_channel.send(confirmation_message)

    # Send a message in the selected channel to confirm the ticket was created
    confirmation_message = f"Ticket channel {ticket_channel.mention} has been created for {ctx.author.mention}"
    await channel.send(confirmation_message)

    # Optionally, you can also send a message in the original ticket setup message to confirm the ticket was created
    # await message.edit(content="Ticket channel created", components=[])



# Load warning counts from file on startup
import json
import os

# Check if user has the 'administrator' permission before allowing them to use the warn command

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

if os.path.exists("warnings.json"):
    with open("warnings.json") as f:
        warnings = json.load(f)
else:
    warnings = {}

# Save warning counts to file whenever they are updated
def save_warnings():
    with open("warnings.json", "w") as f:
        json.dump(warnings, f)

@bot.command(aliases=["warning","give_warning","givewarning","givewarn"])
@commands.check(is_admin)
async def warn(ctx, member: discord.Member, *, reason: str):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    if member.id == ctx.author.id:
        await ctx.send(f"{error_emoji} You cannot warn yourself.")
        return

    if member.id == bot.user.id:
        await ctx.send(f"{error_emoji} I cannot warn myself.")
        return

    if str(member.guild.id) not in warnings:
        warnings[str(member.guild.id)] = {}

    if str(member.id) not in warnings[str(member.guild.id)]:
        warnings[str(member.guild.id)][str(member.id)] = 0

    warnings[str(member.guild.id)][str(member.id)] += 1
    save_warnings()

    try:
        await member.send(f"<:locked:1095311711814299648> Greetings, {member.name}. You have been warned in the server **{ctx.guild.name}**. The reason is **{reason}**. Warned by {ctx.author.name}.")
    except discord.errors.HTTPException:
        await ctx.send(f"{error_emoji} I cannot DM that user. The warning still has been given, though!")

    await ctx.send(f"{success_emoji} {member.mention} has been warned for **{reason}**. They now have **{warnings[str(member.guild.id)][str(member.id)]}** warnings.")

@bot.command(aliases=["checkwarnings","check_warnings","checkwarn"])
async def checkwarns(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    if member.id == bot.user.id:
        await ctx.send(f"{error_emoji} I don't have any warnings.")

    elif str(member.guild.id) in warnings and str(member.id) in warnings[str(member.guild.id)]:
        await ctx.send(f"{member.display_name} has **{warnings[str(member.guild.id)][str(member.id)]}** warnings.")

    else:
        await ctx.send(f"{member.display_name} has no warnings.")

@bot.command(aliases=["clearwarnings","clear_warnings","warningsclear","warnings_clear"])
@commands.check(is_admin)
async def clearwarns(ctx, member: discord.Member):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    if str(member.guild.id) in warnings and str(member.id) in warnings[str(member.guild.id)]:
        warnings[str(member.guild.id)].pop(str(member.id))
        save_warnings()
        await ctx.send(f"{success_emoji} {member.display_name}'s warnings have been cleared.")
    try:
        await member.send(f":tada: Greetings, {member.name}. Your warnings have been cleared in the server **{ctx.guild.name}** by {ctx.author.name}.")
    except discord.errors.HTTPException:
        await ctx.send(f"{error_emoji} I cannot DM that user. The warning still has been given, though!")

    else:
        await ctx.send(f"{error_emoji} {member.display_name} has no warnings to clear, or this bot is just misunderstanding.")


@bot.command()
async def fact(ctx):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    data = response.json()

    fact = data['text']

    embed = discord.Embed(title="Random Fact", description=fact, color=0x00ff00)

    await ctx.send(embed=embed)

@bot.command()
async def roblox_user_lookup(ctx, username):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    # Send a request to the Roblox API
    response = requests.get(f'https://users.roblox.com/v1/users/search?keyword={username}')
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Check if any results were found
        if len(data['data']) > 0:
            # Get the user ID of the first result
            user_id = data['data'][0]['id']
            
            # Send a request to the Roblox API to get the user's details
            response = requests.get(f'https://users.roblox.com/v1/users/{user_id}')
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                
                # Create an embed to display the user's details
                embed = discord.Embed(title=f"Roblox user lookup for '{username}'")
                embed.add_field(name='Username', value=data['name'])
                embed.add_field(name='Display Name', value=data['displayName'])
                embed.add_field(name='ID', value=data['id'])
                embed.add_field(name="Account Created", value=data["created"], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Error: {response.status_code} - {response.reason}")
        else:
            await ctx.send(f"No results found for '{username}'")
    else:
        await ctx.send(f"Error: {response.status_code} - {response.reason}")

@bot.command(help="Sets a reminder that will notify the user after the specified time.", aliases=['timer', 'setreminder', "remindme", "remind_me", "reminder"])
async def remind(ctx, time: int, *, reminder: str):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    await ctx.send("<:9904clock:1098351659807158413> Ok, I have set the reminder.")
    await asyncio.sleep(time)
    await ctx.send(f"<:9904clock:1098351659807158413> {ctx.author.mention}, here's your reminder: {reminder}")
    print(f"{ctx.author}'s reminder for `{reminder}` has been sent after {time} second(s)!")

@bot.command(help="Creates a poll with a question and options. Usage: !poll \"<question>\" <option1> <option2> ... <optionN>", aliases=['createpoll', 'startpoll', 'newpoll'])
@commands.has_permissions(administrator=True)
async def poll(ctx, *, question_and_options: str):
    if str(ctx.author.id) in banned_users:
        await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
    elif not ctx.author.guild_permissions.administrator:
        await ctx.send("<:error:1093315720626057299> You do not have the `Administrator` permissions to use this command!")
    else:
        question_and_options = question_and_options.split('"')
        question = question_and_options[1].strip()
        options = [option.strip() for option in question_and_options[2].strip().split(' ') if option]
        if not question:
            await ctx.send(f"{error_emoji} You need to provide a question for the poll!")
            return
        if len(options) < 2:
            await ctx.send(f"{error_emoji} You need to provide at least two options for the poll!")
            return
        if len(options) > 10:
            await ctx.send(f"{error_emoji} You cannot provide more than 10 options for the poll!")
            return
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", ]
        poll_text = f"{question}\n\n"
        for i, option in enumerate(options):
            poll_text += f"{reactions[i]} {option}\n"
        embed = discord.Embed(title="Poll", description=poll_text, color=random.randint(0, 0xFFFFFF))
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        embed.set_footer(text=f"ZONO Systems by knopka_01#6139 | {timestamp}")
        poll_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await poll_message.add_reaction(reaction)



bot.currency = {}

from PyDictionary import PyDictionary

@bot.command()
async def define(ctx, word: str):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    dictionary=PyDictionary()
    definition = dictionary.meaning(word)
    if not definition:
        await ctx.send(f"Sorry, I couldn't find a definition for '{word}'.")
    else:
        embed = discord.Embed(title=f"Definition of '{word}':")
        embed.set_footer(text="📖 Powered by PyDictionary")
        for part_of_speech, definition_list in definition.items():
            embed.add_field(name=part_of_speech.capitalize(), value="\n".join(definition_list), inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def weather(ctx, *, query: str):
  if str(ctx.author.id) in banned_users:
    await ctx.send("<:error:1093315720626057299> You are blocked from using our system!")
  else:
    url = f"http://api.weatherapi.com/v1/current.json?key=key-goes-here&q={query}&aqi=no"

    try:
        response = requests.get(url)
        data = response.json()

        location = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        localtime = data["location"]["localtime"]
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        condition_text = data["current"]["condition"]["text"]
        condition_icon = data["current"]["condition"]["icon"]

        # Create an embed with weather information
        embed = discord.Embed(title=f"Weather for {location}, {region} ({country})", description=f"As of {localtime}", color=0x3498db)
        embed.add_field(name="Temperature", value=f"{temp_c}°C ({temp_f}°F)", inline=False)
        embed.add_field(name="Condition", value=condition_text, inline=False)
        embed.set_thumbnail(url=f"https:{condition_icon}")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"{error_emoji} Sorry, I couldn't find any weather information for that location.")

import animec
import aiohttp

jikan_url = "https://api.jikan.moe/v4"

@bot.command()
async def anime(ctx, *, anime_title):
    anime_title = anime_title.lower()
    search_url = f"{jikan_url}/search/anime?q={anime_title}"
    search_response = requests.get(search_url)
    search_data = search_response.json()["data"]
    if not search_data:
        await ctx.send(f"No anime found with title {anime_title}")
        return
    anime_id = search_data[0]["id"]
    anime_url = f"{jikan_url}/anime/{anime_id}"
    anime_response = requests.get(anime_url)
    anime_data = anime_response.json()["data"]
    anime_title = anime_data["title"]
    anime_synopsis = anime_data["synopsis"]
    anime_rating = anime_data["score"]
    anime_episodes = anime_data["episodeCount"]
    anime_url = anime_data["url"]
    anime_image_url = anime_data["mainImage"]["medium"]
    embed = discord.Embed(title=anime_title, url=anime_url, description=anime_synopsis, color=0x00ff00)
    embed.set_thumbnail(url=anime_image_url)
    embed.add_field(name="Rating", value=anime_rating)
    embed.add_field(name="Episodes", value=anime_episodes)
    await ctx.send(embed=embed)



import openai

# Set up OpenAI API credentials
openai.api_key = "key-here"

@bot.command(name="chat", aliases=["ai","askgpt","ask-gpt","ask_gpt","chatgpt","chat-gpt","chat_gpt"])
async def chat(ctx, *, message: str):
    # Call OpenAI's GPT-3 API to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Send the response back to Discord
    await ctx.send(response.choices[0].text)

@bot.command(name="tod", aliases=["tord","truth","dare","truth_or_dare"])
async def tod(ctx):
   embed = discord.Embed(title="Truth Or Dare Website", description="[Truth Or Dare](https://legendary-twilight-b6d7c9.netlify.app) is the website made by kno for Truth Or Dare.", color=random.randint(0, 0xFFFFFF))
   await ctx.send(embed=embed)

@bot.command()
@commands.check(is_bot_admin)
async def countdown(ctx, seconds: int, reason):
    # Define the embed
    embed = discord.Embed(title="Countdown", description=f"Starting countdown for {seconds} seconds!", color=0x00ff00)

    # Send the embed message
    message = await ctx.send(embed=embed)

    # Loop through the countdown and update the embed message
    for i in range(seconds, 0, -1):
        embed.description = f"Countdown: {i} seconds remaining!"
        await message.edit(embed=embed)
        await asyncio.sleep(1)

    # Update the embed message when the countdown is finished
    embed.description = f"Countdown finished for {reason} :eyes:!"
    await message.edit(embed=embed)
    await ctx.send("<@&1093282588044574842> ^^")

@bot.command()
async def rps(ctx, choice=None):
    emojis = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️',
        'kno': 'kno `..- ... . / .-..-. ..--.. ..- -. .-.. --- -.-. -.- / -- --- .-. ... . .-..-. / - --- / ..- -. .-.. --- -.-. -.- / ... --- -- . - .... .. -. --. / ... .--. . -.-. .. .- .-..` :shushing_face:'
    }
    
    if choice is None:
        await ctx.send(f"{error_emoji} What's your move??")
        return
    
    valid_options = ['rock', 'paper', 'scissors', 'kno']
    if choice.lower() not in valid_options:
        await ctx.send(f"{error_emoji} Invalid choice. Choose either 'rock', 'paper', 'scissors'.")
        return
    
    bot_choice = random.choice(valid_options)
    result = None
    
    if choice.lower() == bot_choice:
        result = 'tie'
    elif choice.lower() == 'rock' and bot_choice == 'scissors':
        result = 'user'
    elif choice.lower() == 'paper' and bot_choice == 'rock':
        result = 'user'
    elif choice.lower() == 'scissors' and bot_choice == 'paper':
        result = 'user'
    elif choice.lower() == 'kno' and bot_choice == 'rock':
        result = 'user'
    elif choice.lower() == 'kno' and bot_choice == 'scissors':
        result = 'user'
    elif choice.lower() == 'kno' and bot_choice == 'paper':
        result = 'user'
    else:
        result = 'bot'
    
    await ctx.send(f"You choose {emojis.get(choice.lower(), '`invalid choice`')}")
    await ctx.send(f"I choose {emojis.get(bot_choice)}")
    
    if result == 'tie':
        await ctx.send('It\'s a tie!')
    elif result == 'user':
        await ctx.send(f'{emojis.get(choice.lower())} wins!')
    else:
        await ctx.send(f'{emojis.get(bot_choice)} wins!')

@bot.command()
async def unlock(ctx, code=None):
    if code is None:
        await ctx.send(f"{error_emoji} What's the secret code?")
        return

    if code == "morse":
        role_name = "Gold Secret Holder"
        role_color = discord.Color.gold()
        existing_role = discord.utils.get(ctx.guild.roles, name=role_name)
        if existing_role:
            role = existing_role
        else:
            role = await ctx.guild.create_role(name=role_name, color=role_color)
            await role.edit(hoist=True, mentionable=True)

        await ctx.author.add_roles(role)
        embed = discord.Embed(title="Congratulations!",
                              description=f"You have claimed the Gold Secret Holder role with code '{code}'! Enjoy your new shiny role!",
                              color=role_color)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{error_emoji} Sorry, the code you entered is invalid.")

@bot.command()
async def report(ctx, *, report=None):
    if report is None:
        await ctx.send(f"{error_emoji} What's your report?")
        return

    # Create the JSON payload to send to the webhook
    payload = {
        "content": report,
        "username": str(ctx.author),
        "avatar_url": str(ctx.author.avatar.url)
    }

    # Send the report to the webhook
    webhook_url = "webhook"
    msg = f"{success_emoji} Report sent successfully!; Sorry for the trouble caused! I have sent a report to developers. If it doesn't get fixed in the next 7 days or so, please join our support server and refer to a staff member there. https://discord.gg/BJDVEwAnjv"
    response = requests.post(webhook_url, json=payload)
    embed = discord.Embed(title="Report Statistics", color=0x00ff00, description=msg)
    # Confirm the report was sent
    if response.status_code == 204:
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{error_emoji} Error sending report: {response.status_code}")


import keep_alive #don't forget to import the file!
keep_alive.keep_alive()

# Run the bot

# Run the bot
bot.run(os.getenv(my_secret))
