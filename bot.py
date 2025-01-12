from discord.ext import commands
import discord
import pandas as pd

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)
    return bot

bot = create_bot()

# Load data
roles = pd.read_csv('data/The Drink.csv')
roles['Difficulty'] = roles['Difficulty'].astype(str).replace("nan","")

@bot.command()
async def hello(ctx, *args):

    await ctx.send(f"Hello! Argument = {type(args)}")

@bot.command()
async def glossary(ctx):
    working_script = roles


    groups = working_script.groupby('Alignment', sort=False)
    for name, group in groups:
        message = ""
        message += "\n"
        message += f"# **{name}**\n"
        for role in group.itertuples():
            message += f"**{role.Role}{role.Difficulty}** {role.Description}\n"
        await ctx.send(message)



with open('bot.key') as f:
    key = f.read()    

bot.run(key)