from discord.ext import commands
import discord
import pandas as pd
from pandas.util import capitalize_first_letter


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

@bot.command()
async def load(ctx, script):
    global working_script, script_name
    script_name = script
    working_script = pd.read_csv(f"./data/{script}.csv")
    working_script['Difficulty'] = working_script['Difficulty'].astype(str).replace("nan", "")
    await ctx.send(f"Loaded script: {script_name}")

@bot.command()
async def current(ctx):
    await ctx.send(f"Current script: {script_name}")

@bot.command()
async def glossary(ctx):
    await ctx.send(f"# **{script_name} - Specific Roles Glossary**")
    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        message += "\n"
        message += f"# **{name}**\n"
        for role in group.itertuples():
            # Length check
            if len(message + f"**{role.Role}{role.Difficulty}** {role.Description}\n") >= 2000:
                await ctx.send(message)
                message = ""
            message += f"**{role.Role}{role.Difficulty}** {role.Description}\n"
        await ctx.send(message)

@bot.command()
async def outline(ctx):
    await ctx.send(f"# **{script_name}** - Outline")
    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        message += "\n"
        message += f"# **{name}**\n"
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
    script_name = script
    working_script = roles[roles['Role'].isin([arg.title() for arg in args])]
    await ctx.send(f"Created new script: {script_name}")



with open('bot.key') as f:
    key = f.read()

bot.run(key)