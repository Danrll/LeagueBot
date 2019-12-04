from bs4 import BeautifulSoup
import requests
import re
import discord
from auth import token
from Commands.PlayerStats import PlayerStats
from Commands.Meta import Meta

TOKEN = token

client = discord.Client()

@client.event
async def on_message(message):
    print(message.content) # Now every message sent will be await message.channel.sended to the console

@client.event
async def on_message(message):
    
    args = message.content.split()

    if args[0] == '!hello':
        await message.channel.send("Hi") # If the user says !hello we will send back hi

    # Prints the LoL stats of a specified player as an embed
    if args[0] == '!stats':
    
   

        # Ensure there is only 1 argument (name of player)
        if len(args) != 2:
            print("Invalid arguments!")
            await message.channel.send("Invalid arguments!")
            return

        # Create an object that contains player stats
        player = PlayerStats(args[1])

        if (player.url == "Error"):
            await message.channel.send("Player not found!")
            return

        # Embed to display player stats
        embed = discord.Embed(
            color = discord.Color.teal()
        )
        embed.set_author(name = player.name, url = player.url, icon_url = "https:" + player.profile_icon)
        embed.set_thumbnail(url = "https:" + player.tier_icon)
        embed.add_field(name = "Level", value = player.level, inline = True)
        embed.add_field(name = "Tier Rank", value = player.tier_rank, inline = True)
        embed.add_field(name = "LP", value = player.lp, inline = True)
        embed.add_field(name = "Wins", value = player.wins, inline = True)
        embed.add_field(name = "Losses", value = player.losses, inline = True)
        embed.add_field(name = "Win/Loss", value = player.winratio, inline = True)
        embed.set_footer(text = "Stats found at op.gg")

        await message.channel.send(embed = embed)

    # prints the best champions for a specific role
    if args[0] == '!meta':                         
          
        # Ensure there is only 1 argument 
        if len(args) != 2:
            print("Invalid arguments!")
            await message.channel.send("Invalid arguments!")
            return

        if args[1] == 'top':
            # Create an object for each role
            role = args[1]
        elif args[1] == 'jungle':
             # Create an object for each role
            role = args[1]
        elif args[1] == 'mid':
             # Create an object for each role
            role = args[1]
        elif args[1] == ('adc') or args[1] == ('bottom'):
             # Create an object for each role
            role = args[1]
        elif args[1] == 'support':
             # Create an object for each role
            role = args[1]
        else: 
            print("incorrect role")
            await message.channel.send("incorrect role")
            return

        # List of champion objects
        c_list = []                      
        for rank in range(1, 4):
            c_list.append(Meta(role, rank))

            champion = c_list[rank - 1]
            embed = discord.Embed(
            color = discord.Color.teal(), 
            )
            embed.set_author(name = champion.name, url = champion.champ_url, icon_url = champion.tier)
            embed.set_thumbnail(url = champion.image)
            embed.add_field(name = "Rank", value = champion.rank, inline = True)
            embed.add_field(name = "Pick Rate", value = champion.pick_rate, inline = True)
            embed.add_field(name = "Win Rate", value = champion.win_rate, inline = True)
            embed.set_footer(text = "stats found on Op.gg")

            await message.channel.send(embed = embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


