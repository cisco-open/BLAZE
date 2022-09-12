# -*- coding: utf-8 -*-
"""This module contains a template MindMeld application"""
from mindmeld import Application
import requests
import os

def api(endpoint):
    return f'http://localhost:3000{endpoint}'

app = Application(__name__)

__all__ = ['app']


@app.handle(default=True)
def default(request, responder):
    """This is a default handler."""
    responder.reply('Sorry, I don\'t understand your request.')


@app.handle(intent='greet')
def greet(request, responder):
    responder.reply('Hello, how can I help you?')


@app.handle(intent='exit')
def exit(request, responder):
    responder.reply('Goodbye!')


@app.dialogue_flow(intent='get_summary')
def get_summary(request, responder):
    responder.reply('Which file are we sumarizing?')
    r = requests.get(api('/files/all_datasets'))
    responder.reply(', '.join(r.json['datasets_search']))

@get_summary.handle(default=True)
def summary_loop(request, responder):
    file = request.text
    try:
        r = requests.get(api('/files/file'), json={'file': file})
        r.raise_for_status()
        content = r.json()['content']
    except requests.exceptions.HTTPError:
        responder.reply('That file was not found')
        return
    try:
        r = requests.get(api('/models/summary'), json={'model': 'T5', 'content': content})
        r.raise_for_status()
        summary = r.json()['result']
    except requests.exceptions.HTTPError:
        responder.reply('Something went wrong with the summarization')
        return
    
    responder.reply(summary)
    responder.reply('Was this answer helpful?')
    responder.params.target_dialogue_state = 'provide_feedback'
    responder.exit_flow()




@app.handle(intent='ask_question')
def ask_question(request, responder):
    """Send the question to the question-answerer"""
    try:
        #r = requests.post(api('/models/initialize'), json={'model': 'ElasticBERT'})
        r = requests.get(api('/models/search'), json={'model': 'ElasticBERT', 'query': request.text})
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        responder.reply('Sorry, I wasn\'t able to answer your question')
        responder.slots['error'] = err
        responder.reply('{error}')
    else:
        responder.slots['answer'] = r.json()['result']
        responder.reply('I found the answer to your query: {answer}')
    finally:
        responder.reply('Was this answer helpful?')
        responder.params.target_dialogue_state = 'provide_feedback'


@app.dialogue_flow(intent='upload_data')
def upload_dataset(request, responder):
    responder.reply('Please enter the file location')
    responder.frame['count'] = 0


@upload_dataset.handle(default=True)
def upload_loop(request, responder):
    """
    Gets the location of the dataset(s) to upload.
    Gives the user 3 attempts before leaving this dialogue flow.
    """
    location = request.text
    count = responder.frame['count'] + 1
    if count <= 3:
        location = os.path.expanduser(location)
        if os.path.exists(location):  # TODO: May want more robust checking for security
            responder.frame['location'] = location
            if _upload_files(location):
                responder.reply('Upload successful')
            else:
                responder.reply('Upload unsuccessful')
            responder.exit_flow()
        else:
            responder.slots['count'] = count
            responder.frame['count'] = count
            responder.reply('That is not a valid location. Please try again ({count}/3)')
    else:  # After 3 failed attempts
        responder.reply('Sorry, these locations do not appear to work.')
        responder.exit_flow()


@upload_dataset.handle(intent='exit', exit_flow=True)
def upload_exit(request, responder):
    responder.reply('Goodbye')


@app.handle(targeted_only=True)
def provide_feedback(request, responder):
    try:
        r = requests.post(api('/feedback'), json={'feedback': request.text})
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        responder.reply('Something went wrong with the feedback')
    else:
        responder.reply('Thank you for your feedback!')


def _upload_files(location):
    """
    Attempts to upload the given file or all files in the given directory

    Returns True if all operations succeed with a good status code.
    Returns False if any request fails.
    """
    try:
        if os.path.isfile(location):  # single file
            with open(location, 'r') as f:
                file = os.path.split(location)[1]
                r = requests.post(api('/files/upload'), json={'file': file, 'content': f.read()})
            r.raise_for_status()
        elif os.path.isdir(location):  # directory -> multiple files
            for file in os.path.listdir(location):
                file_loc = os.path.join(location, file)
                if os.path.isfile(file_loc):
                    with open(file_loc, 'r') as f:
                        r = requests.post(api('/files/upload'), json={'file': file, 'content': f.read()})
                    r.raise_for_status()
    except requests.exceptions.HTTPError:
        return False
    else:
        return True


def _kb_fetch(kb_index, kb_id):
    """
    Retrieve the detailed knowledge base entry for a given ID from the specified index.

    Args:
        index (str): The knowledge base index to query
        id (str): Identifier for a specific entry in the index

    Returns:
        dict: The full knowledge base entry corresponding to the given ID.
    """
    return app.question_answerer.get(index=kb_index, id=kb_id)[0]
