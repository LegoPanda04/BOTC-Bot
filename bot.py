from discord.ext import commands
import discord
import pandas as pd
import os
import glob


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

# @bot.command()
# async def hello(ctx, *args):
#
#     await ctx.send(f"Hello! Argument = {type(args)}")


def load_whitelist():
    with open('whitelist.txt') as f:
        return {int(line.strip()) for line in f.readlines()}

whitelist = load_whitelist()

def is_whitelisted(user_id):
    return user_id in whitelist

@bot.command()
async def test_admin(ctx):
    if is_whitelisted(ctx.author.id):
        await ctx.send('Valid User')
    else:
        await ctx.send('Invalid User')

@bot.command()
async def load(ctx, script):
    global working_script, script_name
    script_name = script
    try:
        working_script = pd.read_csv(f"./data/{script}.csv")
        working_script['Difficulty'] = working_script['Difficulty'].astype(str).replace("nan", "")
        await ctx.send(f"Loaded script: {script_name}")
    except Exception:
        await ctx.send(f"Failed to load script: {script_name}\nExample syntax: $load 'Starter Script'")

@bot.command()
async def current(ctx):
    await ctx.send(f"Current script: {script_name}")

@bot.command()
async def glossary(ctx):
    await ctx.send(f"# **{script_name}{working_script['Difficulty'].max()} - Specific Roles Glossary**")
    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        # message += "\n"
        message += f"## **{name}**\n"
        for role in group.itertuples():
            # Length check
            if len(message + f"**{role.Role}{role.Difficulty}** {role.Description}\n") >= 2000:
                await ctx.send(message)
                message = ""
            message += f"**{role.Role}{role.Difficulty}** {role.Description}\n"
        await ctx.send(message)

@bot.command()
async def outline(ctx):
    await ctx.send(f"# **{script_name}{working_script['Difficulty'].max()} - Outline**")
    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        # message += "\n"
        message += f"## **{name}**\n"
        for role in group.itertuples():
            # Length check
            if len(message + f"**{role.Role}{role.Difficulty}**\n") >= 2000:
                await ctx.send(message)
                message = ""
            message += f"**{role.Role}{role.Difficulty}**\n"
        await ctx.send(message)

@bot.command()
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

@bot.command()
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
        print(current_roles)
        for arg in args:
            print(arg)
            print(current_roles)
            if arg in current_roles:
                current_roles.remove(arg)
            elif arg not in current_roles:
                current_roles.append(arg)
        print(current_roles)
        # Generate script file
        working_script = roles[roles['Role'].isin(current_roles)]
        working_script.to_csv(f"./data/{script_name}.csv", index=False, header=True)
        await ctx.send(f"Updated script: {script_name}")

@bot.command()
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