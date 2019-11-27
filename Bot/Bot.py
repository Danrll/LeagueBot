

import discord

TOKEN = 'TOKEN'

client = discord.Client()

@client.event
async def on_message(message):
    print(message.content) # Now every message sent will be printed to the console

@client.event
async def on_message(message):
    if message.content.find("!hello") != -1:
        await message.channel.send("Hi") # If the user says !hello we will send back hi




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


