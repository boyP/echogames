"""
This is an echo application for madlibs
"""

from __future__ import print_function

import requests
from fuzzywuzzy import fuzz, process


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return initializeGame()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MadlibsIntent":# TO BE CHANGED ON DEVELOPER.AMAZON!!!!!!
        return initializeGame()
    elif intent_name == "AMAZON.HelpIntent":
        return initializeGame()
    elif intent_name == "AMAZON.StopIntent":
        return stopGame()
    elif intent_name == "AMAZON.CancelIntent":
        return stopGame()
    else:
        print(intent_name)
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- My own helper functions --------------------------------------

def get_friends(access_token):
    """Get friends of the user corresponding to the access_token."""

    base_url = "https://graph.facebook.com/v2.0/me/friends?access_token={token}"
    url = base_url.format(token=access_token)

    response = requests.get(url).json()

    return {
        userinfo['name'] : userinfo['id'] for userinfo in response['data']
    }


def get_best_friend_match(to_match, choices):
    """Get the string in `choices` that most closely matches `to_match`."""
    name, _ = process.extract(to_match, choices, limit=1)[0]
    return name


def foo():
    access_token = 'ENTER ACCESS TOKEN HERE'
    friends_to_ids = get_friends(access_token)

    base_url = 'https://graph.facebook.com//v2.2/{userid}?access_token={token}'

    name = get_best_friend_match("Benson Qiu", friends_to_ids.keys())
    userid = friends_to_ids[name]

    url = base_url.format(
        userid=userid,
        token=access_token,
    )
    response = requests.get(url).json()

    string = "First name {firstname}, last name {lastname}, last active {updated_time}".format(
        firstname = response['first_name'],
        lastname = response['last_name'],
        updated_time = response['updated_time'],
    )
    return string

# --------------- Functions that control the skill's behavior ------------------

#Initialize madlibs game
def initializeGame():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    #card_title = intent['name']
    card_title = ''
    #speech_output = "Happy Birthday To You, Happy Birthday To You, Happy Birthday Dear Pratik, Happy Birthday To You "
    speech_output = foo()

    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, 'reprompt_text_string', should_end_session))

def promptWord():
    """ We want to prompt the user for speicifc words
    """

    session_attributes = {}
    card_title = "Let's play Mad Libs"
    speech_output = "Testing 1 2 3."

    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def stopGame():
    """ We want to quit the application
    """
    should_end_session = True

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
