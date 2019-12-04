from bs4 import BeautifulSoup
import requests
import re
import discord
from discord.ext import commands
from auth import token
from Commands.PlayerStats import PlayerStats
from Commands.Meta import Meta
import asyncio

TOKEN = token

client = discord.Client()

@client.event
async def on_message(message):
    
    print("Message is: " + str(message) + " " + str(message.author)) # Message Info

    args = message.content.split()

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


        # List of champion info embeds
        pages = [] 
        # Create embeds of top 25 champions, add to pages              
        for rank in range(1, 26):
            # Call Meta() to gather champion data
            champion = Meta(role, rank) 

            # Create embed
            embed = discord.Embed(color = discord.Color.teal())
            embed.set_author(name = champion.name, url = champion.champ_url, icon_url = champion.tier)
            embed.set_thumbnail(url = champion.image)
            embed.add_field(name = "Rank", value = champion.rank, inline = True)
            embed.add_field(name = "Pick Rate", value = champion.pick_rate, inline = True)
            embed.add_field(name = "Win Rate", value = champion.win_rate, inline = True)
            embed.set_footer(text = "stats found on Op.gg")

            # Add embed to pages
            pages.append(embed)
        
        # Send first embed (of #1 in role)
        msg = await message.channel.send(embed = pages[0])

        # Add reactions under embed that act as buttons to go through pages
        await msg.add_reaction('\u23ee')            # ⏮ (go to first)
        await msg.add_reaction('\u25c0')            # ◀  (prev)
        await msg.add_reaction('\u25b6')            # ▶  (next)
        await msg.add_reaction('\u23ed')            # ⏭ (go to last)

        i=0                                         # index for pages
        emoji=''                                    # emoji

        while True:
            if emoji=='\u23ee':                     # ⏮ (go to first)
                i=0
                await msg.edit(embed=pages[i])
            if emoji=='\u25c0':                     # ◀  (prev)
                if i>0:
                    i-=1
                    await msg.edit(embed=pages[i])  
            if emoji=='\u25b6':                     # ▶  (next)
                if i<24:
                    i+=1
                    await msg.edit(embed=pages[i])  
            if emoji=='\u23ed':                     # ⏮ (go to first)
                i=24
                await msg.edit(embed=pages[i])      

            # If user clicks on emojis, then continue loop, else end
            # See documentation for wait_for(): https://discordpy.readthedocs.io/en/latest/api.html
            def check(reaction, user):
                return user == message.author and (str(reaction.emoji) == '\u23ee' or str(reaction.emoji) == '\u25c0' or str(reaction.emoji) == '\u25b6' or str(reaction.emoji) == '\u23ed')
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                break                                       # Timeout -> break loop
            else:
                emoji = str(reaction.emoji)                 # Set emoji for next iteration through loop
                await msg.remove_reaction(emoji, user)      # Reset reaction counters

        await msg.clear_reactions()                         # Remove all reactions (end of interaction)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


