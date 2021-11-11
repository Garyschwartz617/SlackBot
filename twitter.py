from requests_oauthlib import OAuth1Session
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import datetime

# To set your enviornment variables in your terminal run the following line:
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


# You can adjust ids to include a single Tweets
# Or you can add to up to 100 comma-separated IDs
# id = "745911914"
# params = {"ids": id, "tweet.fields": "created_at"}

# fields = "created_at,description"
# params = {"usernames": "PythonWeekly,fullstackpython,realpython", "user.fields": fields}

# Tweet fields are adjustable.
# Options include:
# attachments, author_id, context_annotations,
# conversation_id, created_at, entities, geo, id,
# in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
# possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
# source, text, and withheld

# request_token_url = "https://api.twitter.com/oauth/request_token"
# oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# try:
#     fetch_response = oauth.fetch_request_token(request_token_url)
# except ValueError:
#     print(
#         "There may have been an issue with the consumer_key or consumer_secret you entered."
#     )

# resource_owner_key = fetch_response.get("oauth_token")
# resource_owner_secret = fetch_response.get("oauth_token_secret")
# print("Got OAuth token: %s" % resource_owner_key)

# # Get authorization
# base_authorization_url = "https://api.twitter.com/oauth/authorize"
# authorization_url = oauth.authorization_url(base_authorization_url)
# print("Please go here and authorize: %s" % authorization_url)
# verifier = input("Paste the PIN here: ")

# # Get the access token
# access_token_url = "https://api.twitter.com/oauth/access_token"
# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=resource_owner_key,
#     resource_owner_secret=resource_owner_secret,
#     verifier=verifier,
# )
# oauth_tokens = oauth.fetch_access_token(access_token_url)


# access_token = oauth_tokens["oauth_token"]
# access_token_secret = oauth_tokens["oauth_token_secret"]

# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")
# access_token = os.environ.get("ACCESS_TOKEN")
# access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# def create_url():
#     # Replace with user ID below
#     user_id = 2244994945
#     return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}



# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# response = oauth.get(
#     "https://api.twitter.com/2/users/by", params=params
# )

# response = oauth.get(
#     create_url(), params=get_params()
# )


# if response.status_code != 200:
#     raise Exception(
#         "Request returned an error: {} {}".format(response.status_code, response.text)
#     )

# print("Response code: {}".format(response.status_code))
# json_response = response.json()
# # print(json.dumps(json_response, indent=4, sort_keys=True))
# a = json_response['data'][0]['text']
# b = json_response['data'][0]['created_at'].split('T')
# c = b[1].split('.')
# c = c[0].split(':')
# b = b[0].split('-')
# b = datetime.datetime(int(b[0]),int(b[1]),int(b[2]),int(c[0]),int(c[1]),int(c[2]))
# e = [a,b]
# print(e)

def get_python_tweets():
    user_ids ={'Python Weekly ':373620985, 'Real Python' : 745911914, 'Full Stack Python' :  2996502625}
    fun = {}
    for key , value in user_ids.items():
        url = "https://api.twitter.com/2/users/{}/tweets".format(value)
        response = oauth.get(
        url, params=get_params()
        )
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )
        # print("Response code: {}".format(response.status_code))
        json_response = response.json()
        fun[key] = []
        for x in range(len(json_response['data'])):
            a = json_response['data'][x]['text']
            b = json_response['data'][x]['created_at'].split('T')
            c = b[1].split('.')
            c = c[0].split(':')
            b = b[0].split('-')
            b = datetime.datetime(int(b[0]),int(b[1]),int(b[2]),int(c[0]),int(c[1]),int(c[2]))
            now = datetime.datetime.now()
            hours = 5
            hours_sub = datetime.timedelta(hours = hours)
            future_date_and_time = now - hours_sub
            if b > future_date_and_time:
                e = {a:b}
                # print(e)
                fun[key].append(e)
    print(fun)    
 
    return fun            
print('HIiIIIIIII')
get_python_tweets()


def get_my_tweets():
    value = 1458580045702873089
    url = "https://api.twitter.com/2/users/{}/tweets".format(value)
    response = oauth.get(
    url, params=get_params()
    )
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    # print("Response code: {}".format(response.status_code))
    json_response = response.json()
    lst = []
    for x in range(len(json_response['data'])):
        a = json_response['data'][x]['text']
        b = json_response['data'][x]['created_at'].split('T')
        c = b[1].split('.')
        c = c[0].split(':')
        b = b[0].split('-')
        b = datetime.datetime(int(b[0]),int(b[1]),int(b[2]),int(c[0]),int(c[1]),int(c[2]))
        now = datetime.datetime.now()
        hours = 10
        hours_sub = datetime.timedelta(hours = hours)
        future_date_and_time = now - hours_sub
        if b > future_date_and_time:
            e = [a,b]
            lst.append(e)
            # print(e)
            
    print(lst)    
# get_my_tweets()
