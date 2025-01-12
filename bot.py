
with open('bot.key') as f:
    key = f.read()

print(f"key is {key}")

import asyncio
import logging
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import discord

# Initialize the bot with all intents enabled
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), )


# def initialize_event_loop():
#     try:
#         # Get the current event loop or create one if none exists
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         # No running loop, create a new one (useful for threads or non-async contexts)
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         logger.info("Event Loop Initialized")



class BOTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")


@bot.event
async def on_ready():
    """Notify when the bot is ready."""
    print(f"Logged in as {bot.user}!")
    print("------")
    print([c.name for c in bot.commands])

async def setup_hook():
    """Set up the bot's cogs."""
    await bot.add_cog(BOTC(bot))
bot.setup_hook = setup_hook



logger.info("Starting async event loop")
bot.run(key)