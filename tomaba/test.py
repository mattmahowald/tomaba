import os
import sys
from mistralai import Mistral
from dotenv import load_dotenv
import discord
import asyncio

# Load environment variables from .env
load_dotenv()

# Get API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # Ensure this is an integer

# Initialize Mistral API client
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
mistral_client = Mistral(api_key=api_key)


# Function to get chat response from Mistral
def get_chat_response():
    chat_response = mistral_client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Write a short victory message that testing was successful in the theme of a pirate",
            },
        ],
    )
    return chat_response.choices[0].message.content


# Set up Discord intents
intents = discord.Intents.default()
intents.messages = True  # Enable the intent to receive messages

# Create a Discord client
discord_client = discord.Client(intents=intents)


# Asynchronous function to send a message
@discord_client.event
async def on_ready():
    print(f"Logged in as {discord_client.user}")

    # Get the specified channel
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel is not None:
        # Send a message to the Discord channel
        username = os.getenv("USER")
        message_content = f"{get_chat_response()}\n\n{username}"
        await channel.send(message_content)
        print(f"Sent message: {message_content}")
    else:
        print("Channel not found or invalid channel ID.")

    await discord_client.close()


# Run the Discord client
discord_client.run(DISCORD_TOKEN)
