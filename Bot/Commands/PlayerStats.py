from bs4 import BeautifulSoup
import requests
import re

class PlayerStats(object):

    def __init__(self, playerName):

        # Find player op.gg page where stats are located
        self.url = 'https://na.op.gg/summoner/userName=' + playerName

        source = requests.get(self.url).text
        soup = BeautifulSoup(source, 'lxml')

        # Ensure player exists
        if soup.find('div', class_="SummonerNotFoundLayout") != None:
            print("Invalid player!")
            self.url = 'Error'
            return

        # Get name
        self.name = soup.find('span', class_= "Name")
        if self.name != None:
            self.name = self.name.text
        else:
            print("No name")
            self.name = "N/A"
            
        # Get url to profile icon
        self.profile_icon = soup.find('img', class_= "ProfileImage")
        if self.profile_icon != None:
            self.profile_icon = self.profile_icon['src']
        else: 
            print("No profile icon")
            self.profile_icon = "N/A"

        # Get level
        self.level = soup.find('div', class_= "ProfileIcon").span
        if self.level != None:
            self.level = self.level.text
        else:
            print("No level")
            self.level = "N/A"

        # Get url to tier icon
        self.tier_icon = soup.find('div', class_= "SummonerRatingMedium").div.img
        if self.tier_icon != None:
            self.tier_icon = self.tier_icon['src']
        else: 
            print("No tier icon")
            self.tier_icon = "N/A"        

        # Player Tier Info
        tier = soup.find('div', class_= "TierRankInfo")
        if tier != None:

            # Get tier rank
            self.tier_rank = tier.find('div', class_= "TierRank").text

            # Get League Points
            self.lp = tier.find('span', class_= "LeaguePoints")
            if self.lp != None:
                self.lp = re.sub('\s+', '', self.lp.text)
                self.lp = re.sub('[^0-9]', '', self.lp)
            else:
                print("No lp")
                self.lp = "N/A"

            # Get wins
            self.wins = tier.find('span', class_="wins")
            if self.wins != None:
                self.wins = re.sub('[^0-9]', '', self.wins.text)          # remove non-numbers
            else:
                print("No wins")
                self.wins = "N/A"

            # Get losses
            self.losses = tier.find('span', class_="losses")
            if self.losses != None:
                self.losses = re.sub('[^0-9]', '', self.losses.text)
            else:
                print("No losses")
                self.losses = "N/A"

            # Get win/loss ratio
            self.winratio = tier.find('span', class_="winratio")
            if self.winratio != None:
                self.winratio = re.sub('[^0-9]', '', self.winratio.text)
                self.winratio = self.winratio + "%"
            else:
                print("No winratio")
                self.winratio = "N/A"
            