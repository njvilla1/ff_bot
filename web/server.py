import os
import requests
import json
from flask import Flask, request, jsonify

BOT_ID = os.environ["BOT_ID"]
LEAGUE_ID = os.environ["LEAGUE_ID"]
YEAR = 2018

app = Flask("test bot")

@app.route('/receive_msg', methods=['POST'])
def hello_world():
    """
    msg body looks like:
    {
        "attachments": [],
        "avatar_url": "https://i.groupme.com/123456789",
        "created_at": 1302623328,
        "group_id": "1234567890",
        "id": "1234567890",
        "name": "John",
        "sender_id": "12345",
        "sender_type": "user",
        "source_guid": "GUID",
        "system": false,
        "text": "Hello world ☃☃",
        "user_id": "1234567890"
    } 
    """
    content = request.json
    print("New message: {}".format(content))

    return 'Hello, World!'

def write_message(msg):
    # need to POST msg like :'{"bot_id":"BOT_ID","text":"This is my message"}'
    template = {
            "bot_id": BOT_ID,
            "text": msg,
            "attachments": []
            }
    headers = {'content-type': 'application/json'}

    r = requests.post("https://api.groupme.com/v3/bots/post", data=json.dumps(template), headers=headers)