# coding=utf-8
import telebot
import random
import time
from os import listdir
from os.path import isfile, join


tb = None
phrases_list = {}
conditions_list = {}


def extract_token(filename):
    t = open(filename, "r")
    token = t.readline()
    print "telegram bot api token is {0}".format(token)
    return token


def listener(*messages):
    # When new messages arrive TeleBot will call this function.
    print "message arrived"
    for m in messages:
        if m[0].content_type == 'text':
            msg = m[0] # perche'? 
            if 'jova' in msg.text.lower(): #invocato il dio supremo
                print "jova they are searching for you!"
                chat_id = msg.chat.id
                answer = jova_answer(msg.text.lower())
                if answer:
                    tb.send_chat_action(chat_id, 'typing')
                    words_count = count_words(answer)
                    words_per_sec = 600
                    time_to_write = words_count / words_per_sec
                    #print "word count {0} -> time to write {1} at {2} words per second".format(words_count, time_to_write, words_per_sec)
                    time.sleep(time_to_write)
                    tb.send_message(chat_id, answer)


def jova_answer(message):
    answer = ""
    if 'help' in message:
        answer = jova_help()
    else:
        answer = jova_answer_conditions(message)
    return answer


def jova_answer_conditions(message):
    plain_message = ""
    for condition_file in conditions_list:
        cond = conditions_list.get(condition_file)
        if any(condition in message for condition in cond):
            phrase = phrases_list.get(condition_file)
            plain_message = random.choice(phrase)
            break
    jova_answer = plain_message.lower().replace('s', 'f').replace('x', 'f')
    return jova_answer

def jova_help():
    plain_message = ""
    print "printing help..."
    for condition_file in conditions_list:
        print "printing conditions for {0} ->".format(condition_file)
        plain_message += condition_file + '\n'
        conditions = conditions_list.get(condition_file)
        for condition in conditions:
            print "\t{0}".format(condition)
            plain_message += '\t' + condition + '\n'
        plain_message += '--------\n'
    return plain_message

def read_jova_phrases():
    global phrases_list

    print "start reading jova phrases..."

    onlyfiles = [ f for f in listdir("phrases/") if isfile(join("phrases/",f)) ]
    for file in onlyfiles:
        with open('phrases/' + file) as f:
            phrases_list[file] = f.read().splitlines()
            print "\t{0} read ->\tlines {1}".format(file, len(phrases_list[file]))


def read_jova_conditions():
    global conditions_list

    print "start reading jova conditions..."

    onlyfiles = [ f for f in listdir("conditions/") if isfile(join("conditions/",f)) ]
    for file in onlyfiles:
        with open('conditions/' + file) as f:
            conditions_list[file] = f.read().splitlines()
            print "\t{0} read ->\tlines {1}".format(file, len(conditions_list[file]))


def count_words(phrase):
    return len(phrase.split(" "))


def main():
    read_jova_conditions()
    read_jova_phrases()
    token = extract_token("key.token")
    global tb
    tb = telebot.TeleBot(token)
    tb.set_update_listener(listener)
    tb.polling()

    while True:
        time.sleep(0.05)


if __name__ == '__main__':
    main()