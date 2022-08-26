import os
from mindmeld.components import NaturalLanguageProcessor
from mindmeld import configure_logs

"""
This module contains the Webex Bot Server component.
"""

import json
import logging

from webexteamssdk import WebexTeamsAPI, Webhook
from flask import Flask, request
import requests
from urllib.parse import urljoin
import re

from mindmeld.components.dialogue import Conversation

CISCO_API_URL = "https://webexapis.com/v1"
ACCESS_TOKEN_WITH_BEARER = "Bearer "
BAD_REQUEST_NAME = "BAD REQUEST"
BAD_REQUEST_CODE = 400
APPROVED_REQUEST_NAME = "OK"
APPROVED_REQUEST_CODE = 200

WEBHOOK_NAME = "ASKI_conversational"
WEBHOOK_URL_SUFFIX = "/events"
PORT_NUMBER = 8080

class WebexBotServerException(Exception):
    pass


class WebexBotServer:
    """
    A sample server class for Webex Teams integration with any MindMeld application
    """

    def __init__(self, name, app_path, nlp=None, webhook_url=None, access_token=None):
        """
        Args:
            name (str): The name of the server.
            app_path (str): The path of the MindMeld application.
            nlp (NaturalLanguageProcessor): MindMeld NLP component, will try to load from app path
              if None.
            ####webhook_id (str): Webex Team webhook id, will raise exception if not passed.
            access_token (str): Webex Team bot access token, will raise exception if not passed.
        """
        self.app = Flask(name)
        self.webhook_url = webhook_url
        self.access_token = access_token
        self.webhook_id = None  # Set when running
        if not nlp:
            self.nlp = NaturalLanguageProcessor(app_path)
            self.nlp.load()
        else:
            self.nlp = nlp
        self.conv = Conversation(nlp=self.nlp, app_path=app_path)

        self.logger = logging.getLogger(__name__)

        if not self.webhook_url:
            raise WebexBotServerException("WEBHOOK_URL not set")
        if not self.access_token:
            raise WebexBotServerException("BOT_ACCESS_TOKEN not set")

        self.teams_api = WebexTeamsAPI(access_token=self.access_token)

        @self.app.route(WEBHOOK_URL_SUFFIX, methods=["POST"])
        def handle_message():  # pylint: disable=unused-variable
            webhook_obj = Webhook(request.json)
            
            if webhook_obj.id != self.webhook_id:
                self.logger.debug("Retrieved webhook_id %s doesn't match", webhook_obj.id)
                payload = {"message": "WEBHOOK_ID mismatch"}
                return BAD_REQUEST_NAME, BAD_REQUEST_CODE, payload
            
            room = self.teams_api.rooms.get(webhook_obj.data.roomId)
            message = self.teams_api.messages.get(webhook_obj.data.id)
            person = self.teams_api.people.get(message.personId)

            # Ignore the bot's own responses
            me = self.teams_api.people.me()
            if message.personId == me.id:
                payload = {
                    "message": "Input query is the bot's previous message, \
                            so don't send it to the bot again"
                }
                return APPROVED_REQUEST_NAME, APPROVED_REQUEST_CODE, payload

            responses = []
            if message.files:
                file = message.files[0]
                r = requests.get(file, headers={'Authorization': f'Bearer {self.access_token}'})
                d = r.headers['content-disposition']
                fname = re.findall("filename=\"(.+)\"", d)[0]
                self.logger.info(f'Uploading file {fname}')
                if fname.endswith('.yaml'):
                    r = requests.post('http://localhost:3000/files/yaml', json={'file': fname, 'content': r.text})
                    responses.append(f"Dashboard generated: {r.json()['dash']}")
                else:
                    r = requests.post('http://localhost:3000/files/upload', json={'file': fname, 'content': r.text})
                    try:
                        r.raise_for_status()
                    except requests.exceptions.HTTPError:
                        self.logger.info('Failed to upload')
                        responses.append('Something went wrong with the file upload')
                    else:
                        self.logger.info('Upload succeeded')
                        responses.append('File uploaded successfully')

            if message.text:
                responses.extend(self.conv.say(message.text))
            
            for response in responses:
                new_message = self.teams_api.messages.create(roomId=room.id, text=response)
                self.logger.debug(new_message.text)

            payload = { "messages": responses }
            return APPROVED_REQUEST_NAME, APPROVED_REQUEST_CODE, payload

    def run(self, host="localhost", port=8080):
        self.logger.info(f'Running bot server on port {port}')
        self.delete_webhooks_with_name()
        self.create_webhooks(self.webhook_url)

        try:
            self.app.run(host=host, port=port)
        finally:
            self.logger.info('Cleaning webhooks')
            self.delete_webhooks_with_name()

    def delete_webhooks_with_name(self):
        """List all webhooks and delete webhooks created by this script."""
        for webhook in self.teams_api.webhooks.list():
            if webhook.name == WEBHOOK_NAME:
                self.logger.debug("Deleting Webhook:", webhook.name, webhook.targetUrl)
                self.teams_api.webhooks.delete(webhook.id)

    def create_webhooks(self, webhook_url):
        """Create the Webex Teams webhooks we need for our bot."""
        self.logger.info("Creating Message Created Webhook...")
        webhook = self.teams_api.webhooks.create(
            resource="messages",
            event="created",
            name=WEBHOOK_NAME,
            targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
        )
        self.webhook_id = webhook.id
        self.logger.debug(webhook)
        self.logger.info("Webhook successfully created.")

if __name__ == '__main__':
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
    ACCESS_TOKEN = os.environ.get('BOT_ACCESS_TOKEN')

    configure_logs()
    nlp = NaturalLanguageProcessor('.')

    server = WebexBotServer(
        name=__name__,
        app_path='.',
        nlp=nlp,
        webhook_url=WEBHOOK_URL,
        access_token=ACCESS_TOKEN
        )

    server.run(host='0.0.0.0', port=PORT_NUMBER)
