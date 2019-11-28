from bs4 import BeautifulSoup
import requests
import re
import discord
from auth import token

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
        
        # Find player op.gg page where stats are located
        url = 'https://na.op.gg/summoner/userName=' + args[1]

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        # Ensure player exists
        if soup.find('div', class_="SummonerNotFoundLayout") != None:
            print("Invalid player!")
            await message.channel.send("Player not found!")
            return

        # Get name
        name = soup.find('span', class_= "Name")
        if name != None:
            name = name.text
        else:
            print("No name")
            name = "N/A"
            
        # Get url to profile icon
        profile_icon = soup.find('img', class_= "ProfileImage")
        if profile_icon != None:
            profile_icon = profile_icon['src']
        else: 
            print("No profile icon")
            profile_icon = "N/A"

        # Get level
        level = soup.find('div', class_= "ProfileIcon").span
        if level != None:
            level = level.text
        else:
            print("No level")
            level = "N/A"

        # Get url to tier icon
        tier_icon = soup.find('div', class_= "SummonerRatingMedium").div.img
        if tier_icon != None:
            tier_icon = tier_icon['src']
        else: 
            print("No tier icon")
            tier_icon = "N/A"        

        # Player Tier Info
        tier = soup.find('div', class_= "TierRankInfo")
        if tier != None:

            # Get tier rank
            tier_rank = tier.find('div', class_= "TierRank").text
            # if tier_rank != None:
                # tier_rank = re.sub('\s+', '', tier_rank.text)    # remove whitespace

            # Get League Points
            lp = tier.find('span', class_= "LeaguePoints")
            if lp != None:
                lp = re.sub('\s+', '', lp.text)
                lp = re.sub('[^0-9]', '', lp)
            else:
                print("No lp")
                lp = "N/A"

            # Get wins
            wins = tier.find('span', class_="wins")
            if wins != None:
                wins = re.sub('[^0-9]', '', wins.text)          # remove non-numbers
            else:
                print("No wins")
                wins = "N/A"

            # Get losses
            losses = tier.find('span', class_="losses")
            if losses != None:
                losses = re.sub('[^0-9]', '', losses.text)
            else:
                print("No losses")
                losses = "N/A"

            # Get win/loss ratio
            winratio = tier.find('span', class_="winratio")
            if winratio != None:
                winratio = re.sub('[^0-9]', '', winratio.text)
                winratio = winratio + "%"
            else:
                print("No winratio")
                winratio = "N/A"

        # Embed to display player stats
        embed = discord.Embed(
            color = discord.Color.teal()
        )
        embed.set_author(name = name, url = url, icon_url = "https:" + profile_icon)
        embed.set_thumbnail(url = "https:" + tier_icon)
        embed.add_field(name = "Level", value = level, inline = True)
        embed.add_field(name = "Tier Rank", value = tier_rank, inline = True)
        embed.add_field(name = "League Points", value = lp, inline = True)
        embed.add_field(name = "Wins", value = wins, inline = True)
        embed.add_field(name = "Losses", value = losses, inline = True)
        embed.add_field(name = "Win/Loss", value = winratio, inline = True)
        embed.set_footer(text = "Stats found at op.gg")

        await message.channel.send(embed = embed)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


