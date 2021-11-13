from requests_oauthlib import OAuth1Session
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import datetime

# loading us the path so we can get to the token down below
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# all the keys and tokens we need to sign in
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# the paramters of each tweet we would like
def get_params():
    return {"tweet.fields": "created_at"}



# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# gets us the url with the value inputed to correct destination
def get_url(value):
    url = "https://api.twitter.com/2/users/{}/tweets".format(value)
    response = oauth.get(
    url, params=get_params()
    )
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    json_response = response.json()
    return json_response



# gets all the python tweets from the past X hours, parses the data so we can keep track of date efficently in datetime, and returns the text and date
def get_language_tweets(user_ids):
    fun = {}
    for key , value in user_ids.items():
        json_response = get_url(value)

        fun[key] = []
        for x in range(len(json_response['data'])):
            a = json_response['data'][x]['text']
            b = json_response['data'][x]['created_at'].split('T')
            c = b[1].split('.')
            c = c[0].split(':')
            b = b[0].split('-')
            b = datetime.datetime(int(b[0]),int(b[1]),int(b[2]),int(c[0]),int(c[1]),int(c[2]))
            now = datetime.datetime.now()
            hours = 12

            hours_sub = datetime.timedelta(hours = hours)
            future_date_and_time = now - hours_sub
            if b > future_date_and_time:
                e = {a:b}
                # print(e)
                fun[key].append(e)
                print('hi')
 
    return fun   

# gets all of my tweets with their dates
def get_my_tweets():
    value = 1458580045702873089
    json_response = get_url(value)
    lst = []
    for x in range(len(json_response['data'])):
        a = json_response['data'][x]['text']
        b = json_response['data'][x]['created_at'].split('T')
        c = b[1].split('.')
        c = c[0].split(':')
        b = b[0].split('-')
        b = datetime.datetime(int(b[0]),int(b[1]),int(b[2]),int(c[0]),int(c[1]),int(c[2]))
        e = [a,b]
        lst.append(e)
    return lst        

# Posts a new tweet for us
def new_tweet(txt):
    payload = {"text": txt}
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    # Saving the response as JSON
    json_response = response.json()
