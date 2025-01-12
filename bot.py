from discord.ext import commands
import discord


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def hello(ctx, *args):
    await ctx.send(f"Hello! Argument = {args}")

with open('bot.key') as f:
    key = f.read()    

bot.run(key)