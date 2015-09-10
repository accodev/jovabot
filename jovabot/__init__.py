# coding=utf-8

import os
import datetime
import importlib
from . import modules
import logging
import socket

import telegram
from flask import Flask, request, abort


# ordered by priority
ENABLED_MODULES = [
    'jovabot.modules.horoscope',
    'jovabot.modules.addressbook',
    'jovabot.modules.learn',
    'jovabot.modules.random',
    'jovabot.modules.lyrics'
]

LOADED_MODULES = []

bot = None
webapp = Flask(__name__)

# config section - change these as you like
TOKEN = '1234567890abcdefgh'
TOKEN_PATH = 'key.token'
CERTIFICATE_PATH = '/etc/nginx/ssl/nginx.crt'

logging.basicConfig(filename='jovabot.log', level=logging.DEBUG)


def extract_token(filename):
    with open(filename, "r") as f:
        token = f.readline()
    return token


def jova_replace(s):
    return s \
        .replace('s', 'f') \
        .replace('x', 'f') \
        .replace('z', 'f') \
        .replace('S', 'F') \
        .replace('X', 'F') \
        .replace('Z', 'F')


def jova_do_something(message):
    if message.text:
        if 'jova' in message.text.lower():  # jova, I choose you!
            logging.info(
                "[{0}] [from {1}] [message ['{2}']]".format(datetime.datetime.now().isoformat(), message.from_user,
                                                            message.text))
            chat_id = message.chat_id
            answer = jova_answer(message.text.lower())
            if answer:
                if isinstance(answer, tuple):
                    if answer[1]:
                        answer = jova_replace(answer[0])
                    else:
                        answer = answer[0]
                else:
                    answer = jova_replace(answer)
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text=answer, reply_to_message_id=message.message_id)


def jova_answer(message):
    global LOADED_MODULES

    for mod in LOADED_MODULES:
        answer = mod.get_answer(message)
        if answer:
            return answer
    return None


def load_modules():
    global LOADED_MODULES
    global ENABLED_MODULES

    for p in ENABLED_MODULES:
        mod = importlib.import_module(p, 'jovabot.modules')
        if mod:
            LOADED_MODULES.append(mod)
            logging.info('loaded module {0}'.format(mod))


def init_modules():
    global LOADED_MODULES
    for m in LOADED_MODULES:
        m.init()


@webapp.route('/telegram/<token>', methods=['POST'])
def telegram_hook(token):
    if token == TOKEN:
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        # do something, man!
        jova_do_something(update.message)

        # jova return something ffs!
        return "ok", 200
    else:
        return "ko", 400


@webapp.route('/')
def hello():
    return "jovabot was here!"


@webapp.route('/webhook/<command>')
def webhook(command):
    if command == 'set':
        res = webhook_set()
    elif command == 'delete':
        res = webhook_delete()
    else:
        res = 'unsupported command {0}'.format(command)
        abort(400)

    logging.info(res)

    return res, 200


def webhook_set():
    # use your nginx.crt man!
    with open(CERTIFICATE_PATH) as c:
        webhook_url = socket.gethostname() + '/jovabot/telegram/' + TOKEN
        res = bot.setWebhook(webhook_url=webhook_url, certificate=c.buffer)
    return res


def webhook_delete():
    res = bot.setWebhook('')
    return res


@webapp.before_first_request
def main():
    logging.info("starting up")

    # processid file - useful to track jovabot
    pid = str(os.getpid())
    pidfile = "jovabot.pid"

    with open(pidfile, "w") as p:
        p.write(pid)

    # load jovabot modules - crazy stuff
    load_modules()
    init_modules()

    # telegram bot api token
    global TOKEN
    TOKEN = extract_token(TOKEN_PATH)

    global bot
    bot = telegram.Bot(token=TOKEN)


if __name__ == '__main__':
    webapp.run()
