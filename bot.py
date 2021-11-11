import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter
from twitter import get_my_tweets,get_python_tweets
import datetime, time


# sets up path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# set up Flask
app = Flask(__name__)

# sets up slack so we can use the code
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

a = True
# need this loop bc it constantly allows us to check our if statement and if it matches the time
while a:

    #  constantly checking time and if it matches then it sends out the hourly reminder
    now = datetime.datetime.now()
    if datetime.datetime.now().minute == 7 and  0 <= datetime.datetime.now().second <= 5  :
        client.chat_postMessage(channel='#api', text = f'your Hourly reminder at {now}') 
        time.sleep(5)   


    # allows us to count messages per user
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

    # lets us print out the hour message whenever we would like
    @app.route('/hour-message', methods =['POST'])
    def hour_message(): 
        print("Doing stuff...")
        date = datetime.datetime.now()
        client.chat_postMessage(channel='#api', text = f'your Hourly reminder at {date}')    
        return Response(), 200
        
    # tells us how many messages we have sent out
    @app.route('/message-count', methods =['POST'])
    def message_count():
        data = request.form
        user_id = data.get('user_id')
        channel_id = data.get('channel_id')
        message_count = message_counts.get(user_id,0)
        client.chat_postMessage(channel=channel_id, text = f'message: {message_count}')
        return Response(), 200

    # Sends us all tweets from these endpoints if we request them
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
                        client.chat_postMessage(channel=channel_id, text = f'{key}s tweets   {k}, time {v}')
        return Response(), 200


    # Sends all my new tweets out, and keeps track of my oldest tweet
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
                client.chat_postMessage(channel=channel_id, text = f'my new tweet - {tweet[0]}')
                time_since['time'] = tweet[1]
            else:
                1    
        return Response(), 200


    time.sleep(1)
    if __name__ == "__main__":
        app.run(debug=True)