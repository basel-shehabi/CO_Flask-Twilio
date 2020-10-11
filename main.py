import os

from flask import Flask, request, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from game_logic import Game

sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(sid, auth_token)
app = Flask(__name__)


def process_input(input, user_number):

    if 'hi' in input.lower():
        varied_response = ('Hello Number: {}! You are now chatting to a bot powered by Twilio!'
                           ' Would you like to play a simple quiz to guess the name of the 80s/90s song based'
                           ' off the lyrics? It is powered by the Muisxmatch API that retrieves snippets'
                           ' of a song lyrics. To proceed, type yes to play or no to exit.'.format(user_number))

    elif 'yes' in input.lower():
        game = Game()
        questions = game.shuffle_questions()
        q_list = []

        for k, v in questions.items():
            q_list.append(questions[k])

        new_q_list = ('\n'.join(q_list))


        varied_response = ('Welcome to guess the 80s and 90s song! Lets start by guessing...'
                           ' Enter the song name to guess right... '
                           ' NOTE: You must separate the words with a comma or else you will get'
                           ' an invalid response!'
                           ' Here are the questions:' + '\n' + '\n' + new_q_list)

    elif ',' in input:
        result = input.replace(' ','').split(',')
        result = [song.lower() for song in result]


        if 'bohemianrhapsody' and 'smellsliketeenspirit' and 'thunderstruck' and 'nevergonnagiveyouup' in result:
            varied_response = 'Congratulations, you have guessed correctly!'

        else:
            varied_response = 'Oops! You guessed wrong. Please try again'

    elif 'no' in input.lower():
        varied_response = 'Very well, Have a good day then. See you later!'
    else:
        varied_response = 'This is not a valid choice. Choose from one of the available responses. ' \
                          'Alternatively, type hi or hello to view the welcome message again'

    return varied_response


def message(text):

    resp = MessagingResponse()
    msg = resp.message()
    msg.body("".join(text))

    return str(resp)


# SMS Route
@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    user_number = request.form['From']
    user_response = request.form['Body']

    text = process_input(user_response, user_number)
    final_response = message(text)

    return final_response


# Just for debugging/testing purposes
@app.route('/')
def index():
    return "Hello World! This is live from Ngrok!"


if __name__ == "__main__":
    app.run(debug=True)
