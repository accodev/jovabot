# coding=utf-8
import telebot
import random
import time
from os import listdir
from os.path import isfile, join


jova_il_mondo = [ "Male...",
                  "Bene!" ]


tb = None
phrases_list = {}
conditions_list = {}

def extract_token(filename):
    t = open(filename, "r")
    token = t.readline()
    print "token is {0}".format(token)
    return token


def listener(*messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        msg = m
        chat_id = msg.chat.id
        if msg.content_type == 'text':
            if 'jova' in msg.text.lower(): #invocato il dio supremo
                #answer = jova_answer(msg.text.lower())
                answer = jova_answer_new(msg.text.lower())
                if answer:
                    try:
                        answer_decoded = answer.decode('utf-8')
                    except UnicodeDecodeError as e:
                        answer_decoded = answer
                    tb.send_chat_action(chat_id, 'typing')
                    words_count = count_words(answer_decoded)
                    words_per_sec = 0.08
                    time_to_write = words_count * words_per_sec
                    #print "word count {0} -> time to write {1} at {2} words per second".format(words_count, time_to_write, words_per_sec)
                    time.sleep(time_to_write)
                    tb.send_message(chat_id, answer_decoded)

swearing_conditions = [ "bestemmia", "porco dio", "porca madonna", "porchidii", "dio can", "dota", "doti", "ammazzati" ]
songs_conditions = [ "canta", "una canzone" ]
social_conditions = [ "selfie", "come va", "racconta", "cosa fai" ]
proverbs_conditions = [ "proverbio", "perla", "saggezza" ]

def jova_answer(message):
    plain_message = ""
    if 'selfie' in message: # swag over 9000
        plain_message = 'Facciamoci un selfie!!!'.lower()
    elif any(swearing_condition in message for swearing_condition in swearing_conditions):
        plain_message = random.choice(swearing_phrases).lower()
    elif any(song_condition in message for song_condition in songs_conditions):
        plain_message = random.choice(song_phrases).lower()
    elif any(social_condition in message for social_condition in social_conditions):
        plain_message = random.choice(social_phrases).lower()
    elif any(proverb_condition in message for proverb_condition in proverbs_conditions):
        plain_message = random.choice(proverb_phrases).lower()
    elif 'come va il mondo' in message:
        plain_message = random.choice(jova_il_mondo).lower()
    jova_message = plain_message.lower().replace('s', 'f').replace('x', 'f')
    return jova_message


def jova_answer_new(message):
    plain_message = ""
    for condition_file in conditions_list:
        cond = conditions_list.get(condition_file)
        if any(condition in message for condition in cond):
            phrase = phrases_list.get(condition_file)
            plain_message = random.choice(phrase)
            break
    jova_answer = plain_message.replace('s', 'f').replace('x', 'f')
    return jova_answer

def read_jova_phrases():
    global swearing_phrases
    with open("phrases/swearing.txt", "r") as swearing_file:
        swearing_phrases = swearing_file.read().splitlines()

    global social_phrases
    with open("phrases/social.txt", "r") as swearing_file:
        social_phrases = swearing_file.read().splitlines()

    global proverb_phrases
    with open("phrases/proverbs.txt", "r") as swearing_file:
        proverb_phrases = swearing_file.read().splitlines()

    global song_phrases
    with open("phrases/songs.txt", "r") as swearing_file:
        song_phrases = swearing_file.read().splitlines()


def read_jova_phrases_new():
    global phrases_list

    onlyfiles = [ f for f in listdir("phrases/") if isfile(join("phrases/",f)) ]
    for file in onlyfiles:
        with open('phrases/' + file) as f:
            phrases_list[file] = f.read().splitlines()


def read_jova_conditions():
    global conditions_list

    onlyfiles = [ f for f in listdir("conditions/") if isfile(join("conditions/",f)) ]
    for file in onlyfiles:
        with open('conditions/' + file) as f:
            conditions_list[file] = f.read().splitlines()


def count_words(phrase):
    return len(phrase.split(" "))


def main():
    token = extract_token("key.token")
    #read_jova_phrases()
    read_jova_phrases_new()
    read_jova_conditions()
    global tb
    tb = telebot.TeleBot(token)
    tb.set_update_listener(listener)
    tb.polling()

    while True:
        pass


if __name__ == '__main__':
    main()