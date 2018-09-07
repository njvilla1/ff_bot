import os
import requests
import json
import re
from flask import Flask, request, jsonify

try:
    BOT_ID = os.environ["BOT_ID"]
    LEAGUE_ID = os.environ["LEAGUE_ID"]
except KeyError:
    BOT_ID = '1'
    LEAGUE_ID = '1'
YEAR = 2018

def write_message(msg):
    template = {
            "bot_id": BOT_ID,
            "text": msg,
            "attachments": []
            }
    headers = {'content-type': 'application/json'}

    requests.post("https://api.groupme.com/v3/bots/post", data=json.dumps(template), headers=headers)

class Router( object ):

    def __init__(self, routes):
        """ 
        routes will be in the form:
        [ (r'<regex_str>', handler_func), ... ]
        """
        self.routes = [(re.compile(r), h) for r, h in routes]

    def handle(self, groupme_msg):
        msg_text = groupme_msg['text']
        for (route, handler_func) in self.routes:
            if bool(route.match(msg_text)):
                response_text = handler_func(groupme_msg)
                write_message(response_text)
                return response_text

app = Flask("test bot")

def echo_handler(msg):
    return msg['text']

router = Router([
    (r'^@bot repeat.*$', echo_handler)
])

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
    #print("New message: {}".format(content))
    response = router.handle(content)
    if response:
        print('Wrote message in group: "{}"'.format(response))

    return 'Hello, World!'