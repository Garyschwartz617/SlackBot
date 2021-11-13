import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter
from twitter import get_my_tweets,get_language_tweets,new_tweet
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
        client.chat_postMessage(channel='#api', text = f'Your hourly reminder at {now}') 
        time.sleep(5)   


    # allows us to count messages per user
    @slack_event_adapter.on('message')
    def message(payload):
        event = payload.get('event', {})
        channel_id = event.get('channel')
        text = event.get('text')
        if text.startswith('Tweet this:'):
            twt =text.replace('Tweet this:', '')
            new_tweet(twt)
            client.chat_postMessage(channel=channel_id, text= 'Your tweet has been tweeted')


    # lets us print out the hour message whenever we would like
    @app.route('/hour-message', methods =['POST'])
    def hour_message(): 
        print("Doing stuff...")
        date = datetime.datetime.now()
        client.chat_postMessage(channel='#api', text = f'Your hourly reminder At {date}')    
        return Response(), 200
        
    # Sends us all tweets from these endpoints if we request them
    @app.route('/python-tweets', methods =['POST'])
    def python_tweets():
        language_ids ={'Python Weekly':373620985, 'Real Python' : 745911914, 'Full Stack Python' :  2996502625}
        data = request.form
        channel_id = data.get('channel_id')
        find_tweets(language_ids, channel_id)
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
                client.chat_postMessage(channel=channel_id, text = f'My new tweet - {tweet[0]}')
                time_since['time'] = tweet[1]
            else:
                1    
        return Response(), 200


    # You chose the coding language and we will pull the tweets for you
    @app.route('/coding-tweets', methods =['POST'])
    def coding_tweets():
        data = request.form
        channel_id = data.get('channel_id')
        text = data.get('text')
        languages ={'python' : {'Python Weekly':373620985, 'Real Python' : 745911914, 'Full Stack Python' :  2996502625}, 'javascript' : {'Java Script':539345368, 'JavaScript Daily' : 459275531, 'RunJS_App' :  1102660016660713472}, 'c++' : {'Standard C++' : 547159483, 'Hacking C ++' : 1235847275840016384, 'C++' :  77373122}, 'csharp' : { 'CSharpStack' : 1710706759}
        }
        if text.lower() in languages.keys():
            language_ids = languages[text.lower()]
        else:
            client.chat_postMessage(channel=channel_id, text = f'Sorry We dont have that language yet! stay Tuned!')
            return Response(), 200  
        find_tweets(language_ids, channel_id)
        return Response(), 200

    # loops f=though all languages then all Twitterhandlers to post tweets
    def find_tweets(language_ids, channel_id):
        tweets = get_language_tweets(language_ids)
        for key , values in tweets.items():
            if values == []:
                1
                client.chat_postMessage(channel=channel_id, text = f'NO new tweets for {key}')
            else:
                for value in values:
                    for k, v in value.items():
                        client.chat_postMessage(channel=channel_id, text = f'{key}s Tweets:   {k}, time {v}')

    time.sleep(1)
    if __name__ == "__main__":
        app.run(debug=True)