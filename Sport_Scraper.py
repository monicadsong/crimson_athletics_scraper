
import numpy as np
import pandas as pd
import csv
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.notebook_repr_html', True)
from bs4 import BeautifulSoup
import requests

# get all roster links
req = requests.get('http://www.gocrimson.com//sports/mcrew-lw/2017-18/roster')
page = req.text
soup = BeautifulSoup(page, 'html.parser')
roster_pages = []
for link in soup.findAll('a', href=True, text='Roster'):
    roster_pages.append('http://www.gocrimson.com/' + link['href'])

def get_house(link):
    req = requests.get(link)
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    bio = soup.find_all("table")[0]
    tags = bio.find_all('td')
    for i,x in enumerate(tags):
        if x.text == 'House Affiliation: ' or x.text == "House: : ":
            return (tags[i + 1].text)
            
def get_athlete_info(link):
    req = requests.get(link)
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    #isolate roster table
    roster = soup.find_all("table")[0]
    rows = [row for row in roster.find_all("tr")]
    
    all_athletes = []
    for tr in rows[1:]:
        links = []
        for link in tr.find_all('a'):
            links.append(link.get('href'))
        info = {}
        name = tr.findAll('td', {"data-title":"Name"})
        year = tr.findAll('td', {"data-title":"Yr."})
        info['name'] = name[0].text.strip()
        info['year'] = year[0].text.strip()
        info['link'] = 'http://www.gocrimson.com' + links[0]
        all_athletes.append(info)
    for x in all_athletes:
        x['house'] = get_house(x['link'])
    return all_athletes   

def write(data, name):
    f = open("{}.csv".format(name), "w")
    writer = csv.DictWriter(
        f, fieldnames=["name", 'year', 'house', "link"])
    writer.writeheader()
    writer.writerows(data)
    f.close()

def create_csv(roster_link):
    sport = roster_link[33:]
    name = sport.partition("/")[0]
    print ('getting {} data'.format(name))
    data = get_athlete_info(roster_link)
    write(data, name) 

if __name__ == "__main__":
    create_csv('http://www.gocrimson.com//sports/skiing/2017-18/roster')

