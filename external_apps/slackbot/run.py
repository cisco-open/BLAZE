from urllib import response
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import json
from dotenv import load_dotenv
from slackbot_settings import SLACK_APP_TOKEN, SLACK_BOT_TOKEN
from help import RunFunction, InitilizeSwaggerFunctions, GetAPIKeys

load_dotenv()
functions = InitilizeSwaggerFunctions()
api_keys = GetAPIKeys()
if api_keys["response"]["config"].get("Swagger",None) is not None:
        swagger_config = api_keys["response"]["config"].get("Swagger")
        swagger_url = swagger_config["url"]

        
app = App(token=SLACK_BOT_TOKEN)

setting_block = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Enter Swagger Config",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "URL",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "HOST",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "API_KEY",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "API SECRET",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				}
			]
		}
	]

@app.event("app_mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
def mention_handler(body, say):
        if api_keys["response"]["config"].get("Swagger",None) is None:
                say(
            blocks=setting_block,
            text="Enter the config"
        )

        words = body["event"]["text"].split()
        message = ' '.join(words[1:])
        res = RunFunction(message, functions)
        print(res)
        say(str(res))


if __name__ == "__main__":
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()

        