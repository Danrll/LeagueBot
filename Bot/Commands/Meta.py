from bs4 import BeautifulSoup
import requests
import re

class Meta(object):

    def __init__(self, role, rank):

        from bs4 import BeautifulSoup
        import requests
        import re

        # Find champion statistics page
        url = 'https://na.op.gg/champion/statistics'
                
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        # html is divided by role
        if role == "top":
            table = soup.find('tbody', class_= "tabItem champion-trend-tier-TOP")
        elif role == "jungle":
            table = soup.find('tbody', class_= "tabItem champion-trend-tier-JUNGLE")
        elif role == "mid":
            table = soup.find('tbody', class_= "tabItem champion-trend-tier-MID")
        elif role == "adc":
            table = soup.find('tbody', class_= "tabItem champion-trend-tier-ADC")
        else:
            table = soup.find('tbody', class_= "tabItem champion-trend-tier-SUPPORT")

        # Data of champion specified by rank
        row = table.findAll('tr')[rank - 1]
        column = row.findAll('td', class_ = "champion-index-table__cell champion-index-table__cell--value")

        # Champion url
        self.champ_url = 'https://na.op.gg/' + row.find('td', class_="champion-index-table__cell champion-index-table__cell--image").a['href']

        # Champion image is found on champion's page
        img_source = requests.get(self.champ_url).text
        img_soup = BeautifulSoup(img_source, 'lxml')

        # Champion image
        self.image = 'https:' + img_soup.find('div', class_= "champion-stats-header-info__image").img['src']

        # Champion name
        self.name = row.find('div', class_= "champion-index-table__name").text

        # Champion pick rate
        self.pick_rate = column[0].text

        # Champion win rate
        self.win_rate = column[1].text

        # Champion tier (image)
        self.tier = 'https:' + column[2].img['src']

        # Champion rank
        self.rank = rank

