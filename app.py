import tweepy
import os
import requests
import random
import time
from state import save, check

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# v1 twitter auth
auth = tweepy.OAuth1UserHandler(consumer_key=os.environ.get("BOT_CONSUMER_KEY"),
                                consumer_secret=os.environ.get("BOT_CONSUMER_SECRET"),
                                access_token=os.environ.get("BOT_ACCESS_TOKEN"),
                                access_token_secret=os.environ.get("BOT_ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)

# v2 twitter auth
client = tweepy.Client(bearer_token=os.environ.get("BOT_BEARER_TOKEN"),
                       consumer_key=os.environ.get("BOT_CONSUMER_KEY"),
                       consumer_secret=os.environ.get("BOT_CONSUMER_SECRET"),
                       access_token=os.environ.get("BOT_ACCESS_TOKEN"),
                       access_token_secret=os.environ.get("BOT_ACCESS_TOKEN_SECRET"),
                       wait_on_rate_limit=True)


def get_image(url):
    filename = "temp.jpg"
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)


def run():
    obj = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=11').json()
    id = random.choice(obj['objectIDs'])
    if (not check(id)):
        save(id)
        id = str(id)
        obj = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/' + id).json()
        title = obj['title']
        artist = obj['artistDisplayName']
        if obj["artistBeginDate"]:
            artist += " (" + obj["artistBeginDate"] + "-" + obj['artistEndDate'] + ')'
        img = obj['primaryImageSmall']
        get_image(img)
        media_id = api.media_upload(filename="temp.jpg").media_id_string
        print(f"Id do upload: {media_id}")
        titleArt = title + ' - ' + artist
        response = client.create_tweet(text=titleArt, media_ids=[media_id])

        print(titleArt)
        print(f"Endereço do post: https://twitter.com/user/status/{response.data['id']}")
        time.sleep(28800)
        run()
    else:
        run()


run()
