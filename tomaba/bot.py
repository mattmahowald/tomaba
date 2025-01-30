import os
import discord
import logging
import threading

import uvicorn
from fastapi import FastAPI
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

from tomaba.agent import MistralAgent


PREFIX = "!"

# Setup logging
logger = logging.getLogger("discord")

# Setup FastAPI app
app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok", "message": "Tomaba Discord bot is running!"}


# Load the environment variables
load_dotenv()

# Create the bot with all intents
# The message content and members intent must be enabled in the Discord Developer Portal for the bot to work.
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


# Import the Mistral agent from the agent.py file
agent = MistralAgent()


# Get the token from the environment variables
token = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    """
    Called when the client is done preparing the data received from Discord.
    Prints message on terminal when bot successfully connects to discord.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
    """
    logger.info(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message: discord.Message):
    """
    Called when a message is sent in any channel the bot can see.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_message
    """
    # Don't delete this line! It's necessary for the bot to process commands.
    await bot.process_commands(message)

    if message.channel.name != "tomaba":
        return

    # Ignore messages from self or other bots to prevent infinite loops.
    if message.author.bot or message.content.startswith("!"):
        return

    # Process the message with the agent you wrote
    # Open up the agent.py file to customize the agent
    logger.info(f"Processing message from {message.author}: {message.content}")
    response = await agent.run(message)

    # Ensure response is within Discord's 2000 character limit
    if len(response) > 1000:
        response = response[:997] + "..."

    # Send the response back to the channel
    await message.reply(response)


# Commands


# This example command is here to show you how to add commands to the bot.
# Run !ping with any number of arguments to see the command in action.
# Feel free to delete this if your project will not need commands.
@bot.command(name="ping", help="Pings the bot.")
async def ping(ctx, *, arg=None):
    if arg is None:
        await ctx.send("Pong!")
    else:
        await ctx.send(f"Pong! Your argument was {arg}")


def run_bot():
    """Runs the Discord bot in a separate thread."""
    bot.run(token)


if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Start FastAPI (will run in main thread)
    uvicorn.run(app, host="0.0.0.0", port=8080)
