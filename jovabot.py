# coding=utf-8
import telebot
import time
import importlib
import modules

# ordered by priority
ENABLED_MODULES = [
'modules.horoscope',
'modules.addressbook',
'modules.learn',
'modules.random',
]

LOADED_MODULES = []

tb = None

def extract_token(filename):
    t = open(filename, "r")
    token = t.readline()
    print("telegram bot api token is {0}".format(token))
    return token

def jova_replace(s):
    return s \
    .replace('s', 'f') \
    .replace('x', 'f') \
    .replace('z', 'f') \
    .replace('S', 'F') \
    .replace('X', 'F') \
    .replace('Z', 'F')

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
                    answer = jova_replace(answer)

                    tb.send_chat_action(chat_id, 'typing')
                    words_count = count_words(answer)
                    words_per_sec = 600
                    time_to_write = words_count / words_per_sec
                    # print "word count {0} -> time to write {1} at {2} words per second".format(words_count, time_to_write, words_per_sec)
                    time.sleep(time_to_write)
                    tb.send_message(chat_id, answer, reply_to_message_id=msg.message_id)


def jova_answer(message):
    global LOADED_MODULES

    for mod in LOADED_MODULES:
        answer = mod.get_answer(message)
        if answer:
            return answer
    return None

def count_words(phrase):
    return len(phrase.split(" "))


def load_modules():
    global LOADED_MODULES
    global ENABLED_MODULES

    for p in ENABLED_MODULES:
        mod = importlib.import_module(p, 'modules')
        if mod:
            LOADED_MODULES.append(mod)
            print('loaded module', mod)

def init_modules():
    global LOADED_MODULES
    for m in LOADED_MODULES:
        m.init()


def main():
    load_modules()
    init_modules()

    token = extract_token("key.token")
    global tb
    tb = telebot.TeleBot(token, True, 4)
    # tb = telebot.AsyncTeleBot(token)
    tb.set_update_listener(listener)
    tb.polling()

    while True:
        time.sleep(0)


if __name__ == '__main__':
    main()