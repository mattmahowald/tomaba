@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Add message to history
    message_history.append({
        "role": "user",
        "content": message.content
    })

    # Get response using conversation analysis
    response = await agent.analyze_conversation(message_history)
    
    # Add response to history
    message_history.append({
        "role": "assistant",
        "content": response
    })

    # Send response to Discord
    await message.channel.send(response) 