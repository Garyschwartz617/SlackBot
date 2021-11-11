import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

import asyncio,datetime



async def some_function():
    date = datetime.datetime.now()

    client.chat_postMessage(channel='#api', text = f'your Hourly reminder at {date}')

    # asynchronous sleep of 1 second

async def forever():
    while True:
        await asyncio.sleep(10)

        await some_function()

loop = asyncio.get_event_loop()
loop.run_until_complete(forever())






# async def hour_reminder():
#     print('Hello')
#     date = datetime.datetime.now()

#     client.chat_postMessage(channel='#api', text = f'your Hourly reminder at {date}')

#     # asynchronous sleep of 1 second
#     await asyncio.sleep(10)
#     print('World')

# loop = asyncio.get_event_loop()
# # we run our coroutine in the event loop until it is completed
# loop.run_forever(hour_reminder())
# # close the event loop
# # loop.close()



# import sched, time, datetime
# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc): 
#     print("Doing stuff...")
#     date = datetime.datetime.now()
#     client.chat_postMessage(channel='#api', text = f'your Hourly reminder at {date}')
#     s.enter(60, 1, do_something, (sc,))

# s.enter(60, 1, do_something, (s,))
# s.run()

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






if __name__ == "__main__":
    app.run(debug=True)