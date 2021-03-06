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
    if intent_name == "MadlibsIntent":
        return getResponse(intent, session)
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
    card_title = "Mad Libs"

    #Choosing the script
    questions = chooseScript()
    NUM_QUESTIONS = len(questions)

    # Save the questions in session attributes for later use
    sessionAttributes = {'questions': questions, 'index': 0}

    # Generate instruction output
    speech_output = "Let's play Mad Libs, I'm choosing an awesome script. I'm going to ask you " + str(NUM_QUESTIONS) + " questions. Let's begin."
    speech_output = speech_output + " Give me a noun."
    reprompt_text = "Give me a " + questions[index]

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getResponse(intent, session):
    """ We want to prompt the user for speicifc words
    """

    # initialization
    should_end_session = False
    session_attributes = {}
    card_title = 'Prompt'
    reprompt_text = "I am ready to read script."

    # if "questions" in session.get('attributes', {}):
        # Get attributes from the session
    questions = session['attributes']['questions']
    index = session['attributes']['index']

    if(index < len(questions)):
        # Get the user input answer
        answer = intent['slots']['Word']['value']
        speech_output = "You just said " + answer + "."

        # Re ask the question if necessary
        reprompt_text = "Give me a " + questions[index];

        # Update the state with the new responses
        questions[index] = answer
        index = index + 1

        # Check state
        if(index < len(questions)):
            speech_output = speech_output + "Please give me a " + questions[index]
            session_attributes = {'questions': questions, 'index': index}

        else:
            # You have already entered all of the words, time to read script
            should_end_session = True
            script = readScript(questions)
            speech_output = "Reading script. " + script + " Goodbye."

    else:
        speech_output = "index is less than length of questions " \
                    "Internal problem."
        reprompt_text = "I did not understand what you said."

    # else:
    #     speech_output = "I did not understand what you said " \
    #                     "Please try again."
    #     reprompt_text = "I did not understand what you said."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Chooses the script
def chooseScript():
    return getSubArray();

# Read the script based on the responses
def readScript(responses):
    return alexaSay(responses);

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

#---------------Helper Routines----------------#
def selectFile():
    global theFile;
    import random
    randomInt = random.randint(1,2)
    if randomInt == 1:
        theFile = "ML_1.txt"
    elif randomInt == 2:
        theFile = "ML_2.txt"
    return theFile;

i = 0;
q = 0;
theFile = "";
sub_array = [];
# Once file number is determined we open it.
lookup = '%';

def alexaSay(someArray):
    global theFile;

    lineBuffer = '';
    indexPos = 0;
    lineBuffer = open(theFile,'r').read();
    while lookup in lineBuffer:
        #Remove percents
        next_target = lineBuffer.find('%');
        lineBuffer = lineBuffer[:next_target] + someArray[indexPos] +lineBuffer[(next_target+3):]
        indexPos = indexPos + 1;
    return lineBuffer

def getSubArray():
    global sub_array
    with open(theFile) as myFile:
            sub_array = []
            for num, line in enumerate(myFile, 1):
               #num is the line number. an integer
                   #line is the line. a string
               #for i in enumerate (line, 1):

                if lookup in line:
                    index_of_percent = [i for i,x in enumerate(line) if x == lookup];
                    q=0;
                    for element in index_of_percent:
                        if(q < len(index_of_percent)):
                            sub_array.append(line[index_of_percent[q] + 1]);
                            i = i+1;
                            q = q+1;
                            continue
                        else:
                            break;
            item = 0
            for element in sub_array:
                if('n' in sub_array[item]):
                    sub_array[item] = 'noun';
                elif('v' in sub_array[item]):
                    sub_array[item] = 'verb';
                elif('a' in sub_array[item]):
                    sub_array[item] = 'adjective';

                item = item+1;
            return sub_array;
