# coding=utf-8
import telebot
import oroscopy
import paginebianche
import random
import re
import time
from os import listdir
from os.path import isfile, join


tb = None
phrases_list = {}
conditions_list = {}
learned = {}

def extract_token(filename):
    t = open(filename, "r")
    token = t.readline()
    print("telegram bot api token is {0}".format(token))
    return token


# @telebot.async()
def listener(*messages):
    # When new messages arrive TeleBot will call this function.
    print("message arrived")
    for m in messages:
        if m[0].content_type == 'text':
            msg = m[0]  # perche'?
            if 'jova' in msg.text.lower():  # invocato il dio supremo
                print("jova they are searching for you!")
                chat_id = msg.chat.id
                answer = jova_answer(msg.text.lower())
                if answer:
                    tb.send_chat_action(chat_id, 'typing')
                    words_count = count_words(answer)
                    words_per_sec = 600
                    time_to_write = words_count / words_per_sec
                    # print "word count {0} -> time to write {1} at {2} words per second".format(words_count, time_to_write, words_per_sec)
                    time.sleep(time_to_write)
                    tb.send_message(chat_id, answer, reply_to_message_id=msg.message_id)


def jova_answer(message):
    if 'help' in message:
        answer = jova_help()
    elif 'oroscopo' in message:
        answer = jova_oroscopo(message)
    elif 'se ti dico' in message:
        answer = jova_learn(message)
    elif 'cerca' in message:
        answer = jova_paginebianche(message)
    else:
        answer = jova_answer_learned(message) or jova_answer_conditions(message)
    return answer


def jova_answer_learned(message):
    rx = r'jova,?\s(.+)$'
    m = re.match(rx, message)
    if not m:
        return None

    try:
        k = m.groups(1)[0]
        print('search for', k)
        if k in learned:
            v = jova_replace(learned[k])
            print('answer learned message', v)
            return v
    except:
        pass

    return None


def jova_answer_conditions(message):
    plain_message = ""
    for condition_file in conditions_list:
        cond = conditions_list.get(condition_file)
        if any(condition in message for condition in cond):
            phrase = phrases_list.get(condition_file)
            plain_message = random.choice(phrase)
            break
    jova_answer = jova_replace(plain_message)
    return jova_answer


def jova_help():
    plain_message = ""
    print("printing help...")
    for condition_file in conditions_list:
        print("printing conditions for {0} ->".format(condition_file))
        plain_message += condition_file + '\n'
        conditions = conditions_list.get(condition_file)
        for condition in conditions:
            print("\t{0}".format(condition))
            plain_message += '\t' + condition + '\n'
        plain_message += '--------\n'
    return plain_message


def jova_replace(s):
    return s \
    .replace('s', 'f') \
    .replace('x', 'f') \
    .replace('z', 'f') \
    .replace('S', 'F') \
    .replace('X', 'F') \
    .replace('Z', 'F')


def jova_oroscopo(message):

    signes = [
    'ariete', 'toro', 'gemelli',
    'cancro', 'leone', 'vergine',
    'bilancia', 'scorpione', 'sagittario',
    'capricorno', 'acquario', 'pesci']

    found_signes = [x for x in signes if x in message]

    print("oroscopo richiesto per i segni: ", found_signes)

    if not len(found_signes):
        return None

    out = ''
    for o in oroscopy.get(found_signes):
        out += '{0}\n{1}\n'.format(o.sign, o.text)

    return jova_replace(out)


def jova_learn(message):
    global learned

    rx = r'jova,?\sse ti (?:dico|dicono)\s([\w\s\?\!]+)\stu rispondi\s([\w\s\?\!]+)'
    m = re.match(rx, message)

    if not m:
        print('mismatch', message)
        return None

    tokens = m.groups(1)
    if len(tokens) == 2:
        learned[tokens[0]] = tokens[1]
        return 'OK'
    return jova_replace('mi sa che non ho capito')


def jova_paginebianche(message):
    rx = r'jova,?\s(?:cerca|cercami|trova|trovami|paginebianche)\s([\w\s]+)\s(?:a|ad|in)\s([\w\s]+)'
    m = re.match(rx, message)

    if not m:
        print('mismatch', message)
        return None

    tokens = m.groups(1)
    if len(tokens) == 2:

        found = False
        out = 'ho trovato:\n'
        for o in paginebianche.search_wp(tokens[0], tokens[1]):
            out += "{0} tel: {1}\n{2}\n\n".format(o.name, o.tel, o.addr)
            found = True

        if not found:
            return jova_answer_conditions("insulta")

        return jova_replace(out)

    return jova_replace('mi sa che non ho capito')

def read_jova_phrases():
    global phrases_list

    print("start reading jova phrases...")

    onlyfiles = [f for f in listdir("phrases/") if isfile(join("phrases/", f))]
    for file in onlyfiles:
        with open('phrases/' + file, encoding="utf-8") as f:
            phrases_list[file] = f.read().splitlines()
            print("\t{0} read ->\tlines {1}".format(file, len(phrases_list[file])))


def read_jova_conditions():
    global conditions_list

    print("start reading jova conditions...")

    onlyfiles = [f for f in listdir("conditions/") if isfile(join("conditions/", f))]
    for file in onlyfiles:
        with open('conditions/' + file, encoding="utf-8") as f:
            conditions_list[file] = f.read().splitlines()
            print("\t{0} read ->\tlines {1}".format(file, len(conditions_list[file])))


def count_words(phrase):
    return len(phrase.split(" "))


def main():
    read_jova_conditions()
    read_jova_phrases()
    token = extract_token("key.token")
    global tb
    tb = telebot.TeleBot(token, True, 8)
    # tb = telebot.AsyncTeleBot(token)
    tb.set_update_listener(listener)
    tb.polling()

    while True:
        time.sleep(0)


if __name__ == '__main__':
    main()