import os

from authy.api import AuthyApiClient
from flask import Flask, request, redirect, url_for, render_template, session, Response
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from game_logic import Game

sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
authy_api_key = os.environ['AUTHY_API_KEY']


api = AuthyApiClient(authy_api_key)

client = Client(sid, auth_token)
app = Flask(__name__)
app.secret_key = 'random'

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
                          'Alternatively, type hi to view the welcome message again'

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

# Lets refine for the user regs
# Most of the code based on the twilio blog (credit to them)
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")

        session['country_code'] = country_code
        session['phone_number'] = phone_number

        api.phones.verification_start(phone_number, country_code, via=method)

        return redirect(url_for("verify"))

    return render_template("index.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        token = request.form.get("token")

        phone_number = session.get("phone_number")
        country_code = session.get("country_code")

        verification = api.phones.verification_check(phone_number,
                                                     country_code,
                                                     token)

        if verification.ok():
            return Response("<h1>You are now verified!</h1>")

    return render_template("verify.html")



if __name__ == "__main__":
    app.run(debug=True)
