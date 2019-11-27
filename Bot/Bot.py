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
    if message.content.find("!hello") != -1:
        await message.channel.send("Hi") # If the user says !hello we will send back hi

    if message.content.find("!stats") != -1:
        
        url = 'https://na.op.gg/summoner/userName=Dan12326'

        source = requests.get(url).text

        soup = BeautifulSoup(source, 'lxml')

        name = soup.find('span', class_= "Name").text

        profile_icon = soup.find('img', class_= "ProfileImage")

        level = soup.find('div', class_="ProfileIcon").span.text

        tier = soup.find('div', class_= "TierRankInfo")

        tier_rank = tier.find('div', class_= "TierRank").text

        lp = re.sub('\s+', '', tier.find('span', class_= "LeaguePoints").text)
        lp = re.sub('[^0-9]', '', lp)

        wins = tier.find('span', class_="wins").text
        wins = re.sub('[^0-9]', '', wins)

        losses = tier.find('span', class_="losses").text
        losses = re.sub('[^0-9]', '', losses)

        winratio = tier.find('span', class_="winratio").text
        winratio = re.sub('[^0-9]', '', winratio)
        winratio = winratio + "%"

        await message.channel.send("Name: " + name)
        await message.channel.send("Profile Image: " + profile_icon['src'])
        await message.channel.send("Level: " + level)
        await message.channel.send("Tier Rank: "  + tier_rank)
        await message.channel.send("LP: " + lp)
        await message.channel.send("Wins: " + wins)
        await message.channel.send("Losses: " + losses)
        await message.channel.send("Win ratio: " + winratio)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


