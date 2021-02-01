import twitter
import dotenv
import os
import requests
import json
import random
import time
from state import save, check

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

T = twitter.Api(consumer_key= os.environ.get("BOT_CONSUMER_KEY"),
                  consumer_secret= os.environ.get("BOT_CONSUMER_SECRET"),
                  access_token_key= os.environ.get("BOT_ACCESS_TOKEN"),
                  access_token_secret= os.environ.get("BOT_ACCESS_TOKEN_SECRET"))


def run():
    r = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=11')
    obj = r.json()
    id = obj['objectIDs'][random.randint(0,2000)]
    if(not check(id)):
        save(id)
        id = str(id)
        r = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + id)
        obj = r.json()
        title = obj['title'] + '(' + obj['objectDate'] + ')'
        artist = obj['artistDisplayName'] + "(" + obj["artistBeginDate"] + "-" + obj['artistEndDate'] + ')'
        img = obj['primaryImageSmall']
        titleArt = title + ' - ' + artist
        T.PostUpdate(titleArt, img )
        print(titleArt)
        time.sleep(28800)
        run()
    else:
        run()
    


run()
