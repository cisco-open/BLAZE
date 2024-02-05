from urllib import response
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import json
from dotenv import load_dotenv
from external_apps.panoptica_utils.panoptica_utils import RunFunction, InitilizeSwaggerFunctions, GetAPIKeys
 

load_dotenv()
functions = InitilizeSwaggerFunctions()
api_keys = GetAPIKeys()
     
app = App(token=api_keys["config"]["SLACK_BOT_TOKEN"])



@app.event("app_mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
def mention_handler(body, say):
        words = body["event"]["text"].split()
        message = ' '.join(words[1:])
        res = RunFunction(message, functions)
        print(res)
        say(str(res))


if __name__ == "__main__":
        handler = SocketModeHandler(app, api_keys["config"]["SLACK_APP_TOKEN"])
        handler.start()

        