#!/usr/bin/python3

import requests
# import json
from datetime import datetime as dt
import time
import os, sys

# This code isnt perfect by any means, I made it in an hour.
# If you dont like it, than fix it yourself.
#
# Author: Alec Girman
# Version: 1.5.1
# Version running on VM: 1.5.1
# File: covid.py
# Description: A COVID-19 tracker that updates every hour
# For best results, it is ideal to leave this script running 24/7.
# For that reason, it is a good idea to run this in on an
# AWS instance, Azure VM, or Google Cloud instance.
# 
# How to launch:
# To start the script to run indefinitely, run it without any arguments
#   python3 covid.py
# To run it just once, use the --once argument.
#   python3 covid.py --once

url = "https://covid19-us-api.herokuapp.com/"

# version 1.1: removed dependency for covid folder
# version 1.2: removed this because it broke in google cloud
# if 'covid' in os.listdir():
#     os.mkdir('covid')

# Version 1.4: Added 'Version running on VM info'

def get_county_stats():
    # get per county data
    response = requests.get(url + 'county?=')
    
    with open(filename + '.covid.county.json', 'w') as countyfile:
        countyfile.write(response.text)

    print('Saved county data for ' + dtstr)

def get_global_stats():
    # get global data
    response = requests.get(url + 'stats')
    
    with open(filename + '.covid.stats.json', 'w') as globalfile:
        globalfile.write(response.text)

    print('Saved global data for ' + dtstr)

def get_twitter_feed():
    # get twitter data
    response = requests.get(url + 'twitter')
    
    with open(filename + '.covid.twitter.json', 'w') as twitterfile:
        twitterfile.write(response.text)

    print('Saved twitter data for ' + dtstr)

def get_covid_news():
    # get covid related news
    response = requests.get(url + 'news')
    
    with open(filename + '.covid.news.json', 'w') as newsfile:
        newsfile.write(response.text)

    print('Saved news for ' + dtstr)

def run_all():
    # Version 1.5/1.5.1: Fixed a bug causing it to overwrite old files instead of making new ones
    dtstr = str(dt.now().date()) + '.' + str(dt.now().time())
    filename = 'covid/' + dtstr
    get_county_stats()
    get_global_stats()
    get_twitter_feed()
    get_covid_news()


def main():

    # Version 1.3: added the option to run it just once
    if '--once' in sys.argv:
        run_all()
    else:
        while True:
            run_all()
            print('recorded COVID-19 data for timestamp ' + dtstr)

            # data updated every 15 minutes
            # version 1.4: Changed from every 60 minutes to every 15 minutes
            time.sleep(90)

if __name__ == '__main__':
    main()
