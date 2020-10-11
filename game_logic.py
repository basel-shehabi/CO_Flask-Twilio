import os
import requests
import random

key = os.environ['MUSIX_API_KEY']  # Gets the saved API key generated from the MUSIX site


class Game():
    def __init__(self, artist_name=None, track=None):
        self.artist_name = artist_name
        self.track = track
        self.lyrics = self.get_song_snippet()
        self.lyrics_final = self.shuffle_questions()

    # Used to get the song ID. Nothing less, nothing more... (As per the API documentation)

    def get_song(self, artist_name, track):
        musix_url = "https://api.musixmatch.com/ws/1.1/track.search?apikey={}&q_artist={}&q_track={}" \
            .format(key, artist_name, track)
        r = requests.get(musix_url).json()  # Retrieves the track ID and stores it in the next function (Hard Coded)
        return r

    # Once we find the song_id needed from the database in get_song(), we can pass it onto this function
    # Again this is as per the API documentation for musix

    def get_song_snippet(self):
        song_id = [('Never Gonna Give You Up', 9081598), ('Thunderstruck', 31982183),
                   ('Smells Like Teen Spirit', 114888305), ('Bohemian Rhapsody', 106547390)]
        lyrics = {}

        for idx, song in song_id:
            song_url = "https://api.musixmatch.com/ws/1.1//track.snippet.get?track_id={}&apikey={}".format(song, key)
            s = requests.get(song_url).json()

            snippet = s['message']['body']['snippet']['snippet_body']
            lyrics.update({idx: snippet})

        return lyrics

    # Prevents repetition, allows to shuffle the questions everytime the function is called (or restarted)

    def shuffle_questions(self):
        temp_list = list(self.lyrics.items())
        random.shuffle(temp_list)
        lyrics = dict(temp_list)

        return lyrics

    # Testing game logic using terminal
    def play(self):

        print('Welcome to guess the 80s and 90s song! Lets start by guessing...')
        print('Enter the song name to guess right...')
        print('NOTE: The answers must be case sensitive! I.e. all the words begin with a capital letter')

        questions = self.lyrics_final
        score = 0

        for k, v in questions.items():
            print(questions[k])

            user_input = input()

            if user_input == k:
                score += 1
                print('Correct! Your score is now {}'.format(score))
                if score == 4:
                    print('Congratulations, You won the game!')
                else:
                    print('Wrong answer. Try again... Your score is still {}'.format(score))

        return score


