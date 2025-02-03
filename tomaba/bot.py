import os
import discord
import logging
import asyncio
import httpx

from discord.ext import commands
from dotenv import load_dotenv

from models.recipe import Recipe, RecipeSummary

# Load environment variables
load_dotenv()

PREFIX = "!"
SERVER_URL = "http://localhost:8000/chat"

# Setup logging
logger = logging.getLogger("discord")

# Setup bot intents
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True


class DiscordBot(commands.Bot):
    """
    A lightweight Discord bot that listens for messages and forwards them to a FastAPI server.
    """

    def __init__(self, token: str):
        super().__init__(command_prefix=PREFIX, intents=intents)
        self.token = token

    async def on_ready(self):
        """Triggered when the bot successfully connects to Discord."""
        logger.info(f"{self.user} has connected to Discord!")

    async def on_message(self, message: discord.Message):
        """Forwards messages from the "tomaba" channel to the FastAPI server."""
        if message.author.bot or message.content.startswith("!"):
            return
        if message.channel.name != "tomaba":
            return

        # TODO: get prior messages between the bot and the user
        logger.info(f"Forwarding message from {message.author}: {message.content}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                SERVER_URL,
                json={"author": str(message.author), "content": message.content},
                timeout=120,
            )

        if response.status_code == 200:
            recipe = Recipe.from_json(response.json()["response"])
            recipe_summary = RecipeSummary(recipe)
            await message.reply(recipe_summary.summary)
            await message.reply(recipe_summary.ingredients)
            await message.reply(recipe_summary.steps)
        else:
            await message.reply("Error processing message.")

    def run_bot(self):
        """Runs the bot asynchronously."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.run(self.token)
