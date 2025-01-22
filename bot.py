from discord.ext import commands
import discord
import pandas as pd
import os
import glob

"""
TODO:
Add private messaging capabilities.

Lynn Ideas:
Bingo Bob (Demon) At the start of the game you are given a bingo board sheet. 
Bingo bob cannot kill and evil wins if the board is done. This is a freddy type role. 
Everyone can see the blank version of the bingo role which updates nightly. 
Everyone will also have a list of possible points (30-35).

Ash Ideas:
Vampire (Demon) There is no minion. The first two people you kill become evil, and know they are evil.
???
"""


def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)
    return bot

bot = create_bot()

# Load data
roles = pd.read_csv('./data/Roles.csv')
roles['Difficulty'] = roles['Difficulty'].astype(str).replace("nan","")
working_script = roles
script_name = "Roles"



def load_whitelist():
    with open('whitelist.txt') as f:
        return {int(line.strip()) for line in f.readlines()}

whitelist = load_whitelist()

def is_whitelisted(user_id):
    return user_id in whitelist

@bot.command(
    hidden=True
)
async def test_admin(ctx):
    if is_whitelisted(ctx.author.id):
        await ctx.send('Valid User')
    else:
        await ctx.send('Invalid User')

@bot.command(
    help="Loads a script to be the active script.\nExample syntax: $load \"Starter Script.\"",
    brief="Loads a script to be the active script."
)
async def load(ctx, script):
    global working_script, script_name
    script_name = script
    try:
        working_script = pd.read_csv(f"./data/{script}.csv")
        working_script['Difficulty'] = working_script['Difficulty'].astype(str).replace("nan", "")
        await ctx.send(f"Loaded script: {script_name}")
    except Exception:
        await ctx.send(f"Failed to load script: {script_name}\nThis command is case sensitive.")

@bot.command(
    help="Returns what the current active script is.",
    brief="Returns what the current active script is."
)
async def current(ctx):
    await ctx.send(f"Current script: {script_name}")

@bot.command(
    help="Makes a glossary given the current active script.",
    brief="Makes a glossary given the current active script."
)
async def glossary(ctx):
    await ctx.send(f"# **{script_name}{working_script['Difficulty'].max()} - Specific Roles Glossary**")
    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        message += f"## **{name}**\n"
        for role in group.itertuples():
            # Length check
            if len(message + f"**{role.Role}{role.Difficulty}** {role.Description}\n") >= 2000:
                await ctx.send(message)
                message = ""
            message += f"**{role.Role}{role.Difficulty}** {role.Description}\n"
        await ctx.send(message)

@bot.command(
    help="Makes an outline given the current active script.",
    brief="Makes an outline given the current active script."
)
async def outline(ctx):
    await ctx.send(f"# **{script_name}{working_script['Difficulty'].max()} - Outline**")
    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        message += f"## **{name}**\n"
        for role in group.itertuples():
            # Length check
            if len(message + f"{role.Role}, ") >= 2000:
                await ctx.send(message)
                message = ""
            message += f"{role.Role}, "
        message = message[:-2] # Remove last two characters
        await ctx.send(message)

@bot.command(
    help="Make a new script.\nThe script name is case sensitive, role names are not.\nExample syntax: $new \"New Script\" \"artist\" \"drunk\" \"poisoner\" \"imp\" \"scarlet woman\"",
    brief="Makes a new script."
)
async def new(ctx, script, *args):
    global working_script, script_name
    # Tamper prevention
    if not is_whitelisted(ctx.author.id):
        await ctx.send("Sorry, but you are not allowed to use this command.")
    elif script == "Roles":
        await ctx.send("Sorry, but you can not modify the master role list!")
    else:
        script_name = script
        working_script = roles[roles['Role'].isin([arg.title() for arg in args])]
        working_script.to_csv(f"./data/{script}.csv", index=False, header=True)
        await ctx.send(f"Created new script: {script_name}")

@bot.command(
    help="Edits an existing script.\nThe script name is case sensitive, role names are not.\nListing a role in the script will remove it, listing a role not in the script will add it\nExample syntax: $new \"New Script\" \"prisdelo\" \"scarlet woman\"",
    brief="Edits an existing script."
)
async def edit(ctx, *args):
    global working_script
    # Tamper prevention
    if not is_whitelisted(ctx.author.id):
        await ctx.send("Sorry, but you are not allowed to use this command.")
    elif script_name == "Roles":
        await ctx.send("Sorry, but you can not modify the master role list!")
    else:
        args = [arg.title() for arg in args]
        current_roles = list(working_script['Role'])
        for arg in args:
            if arg in current_roles:
                current_roles.remove(arg)
            elif arg not in current_roles:
                current_roles.append(arg)
        # Generate script file
        working_script = roles[roles['Role'].isin(current_roles)]
        working_script.to_csv(f"./data/{script_name}.csv", index=False, header=True)
        await ctx.send(f"Updated script: {script_name}")

@bot.command(
    help="List all scripts.\nThe Roles script does not allow for all functionality.",
    brief="List all scripts."
)
async def scripts(ctx):
    await ctx.send("Fetching scripts...")
    data_folder = "data"

    # Fetch all CSV file names in the folder
    csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

    # Add each file name
    message = ""
    for file in csv_files:
        message += f"*{os.path.splitext(os.path.basename(file))[0]}*\n"
    await ctx.send(message)



with open('bot.key') as f:
    key = f.read()

bot.run(key)