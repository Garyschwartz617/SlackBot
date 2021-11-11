import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter
from twitter import get_my_tweets,get_python_tweets
import datetime


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']




message_counts = {}

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id != BOT_ID:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1
   
        client.chat_postMessage(channel=channel_id, text= text)

@app.route('/message-count', methods =['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id,0)
    client.chat_postMessage(channel=channel_id, text = f'message: {message_count}')
    return Response(), 200

@app.route('/python-tweets', methods =['POST'])
def python_tweets():

    data = request.form
    channel_id = data.get('channel_id')
    tweets = get_python_tweets()

    for key , values in tweets.items():
        if values == []:
            1
        else:
            for value in values:
                for k, v in value.items():
                    print(f'keys : {key} , value {k}')
                    client.chat_postMessage(channel=channel_id, text = f'{key}s tweets   {k}, time {v}')
    return Response(), 200


time_since  = {'time' :datetime.datetime(2000,1,1,0,0,0)}

@app.route('/my-tweets', methods =['POST'])
def my_tweets():
    

    data = request.form
    channel_id = data.get('channel_id')
    tweets = get_my_tweets()
    tweets.reverse()
    for tweet in tweets:
        print(f' tweets {tweet[1]}')
        if time_since['time'] < tweet[1]:
            print(f' time since {time_since}')

            print(f' tweets {tweet[0]}')
            client.chat_postMessage(channel=channel_id, text = f'my new tweet - {tweet[0]}')
            time_since['time'] = tweet[1]
        else:
            1    
    return Response(), 200



if __name__ == "__main__":
    app.run(debug=True)