## For data handling:
import pandas as pd
import numpy as np
import json

## For regular expressions:
import re

## For the scrape:
from bs4 import BeautifulSoup as BShtml
import urllib.request as ur
from pprint import pprint

## Bring states' two-letter abbreviations
states = pd.read_csv('StateAbbreviations.csv')

## Grab data
result_set = []

for index, row in states.iloc[0:49].iterrows():
    url = "http://edition.cnn.com/ELECTION/2008/primary/json/county/" + row['Abbreviation'] + "p1.html?time=21&csiID=csi2"
    r = ur.urlopen(url).read()
    soup = BShtml(r, "html.parser")
    soup = soup.textarea
    results = json.loads(soup.text)
    pages = (results['totalPages']+1) # Setting up a var which equals the number of pages for each county
    for pnum in range(1,pages):
        url = "http://edition.cnn.com/ELECTION/2008/primary/json/county/" + row['Abbreviation'] + "p" + str(pnum) + ".html?time=21&csiID=csi2"     
        r = ur.urlopen(url).read()
        soup = BShtml(r, "html.parser")
        soup = soup.textarea
        results = json.loads(soup.text)
        result_set.append(results)
        print(results)

## Transform nested JSON dictionary into Pandas df
emptydata = pd.DataFrame({"county_name":[], "race":[], "first_name":[], "last_name":[], "id":[], "votes":[], "vote_percent":[], "party":[], "election_date":[], "unknown_data":[], "percent_reporting":[], "poll_close":[], "poll_type":[], "primary_type":[], "status":[]})
for p in result_set:
    for i in p['counties']:
        for e in i['races']:
            for o in e['candidates']:
                    new_result = pd.DataFrame({
                            "county_name":[i['name']],
                            "race":[e['race']],
                            "first_name":[o['fname']],               
                            "last_name":[o['lname']],                   
                            "id":[str(o['id'])],               
                            "votes":[o['cvotes']], 
                            "vote_percent":[str(o['vpct'])],
                            "party":[e['party']],
                            "election_date":[str(e['electiondate'])],
                            "unknown_data":[str(e['opcountyresults'])],
                            "percent_reporting":[str(e['pctsrep'])],
                            "poll_close":[str(e['pollclose'])],
                            "poll_type":[e['polltype']],
                            "primary_type":[e['primarytype']],
                            "status":[e['status']]
                        })
                    emptydata = emptydata.append(new_result)
