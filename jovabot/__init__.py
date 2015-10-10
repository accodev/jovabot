# coding=utf-8

import os
import datetime
import importlib
from . import modules
import logging
import socket
import traceback
import sys

import telegram
from flask import Flask, request, abort


# ordered by priority
ENABLED_MODULES = [
    'jovabot.modules.slash',
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
TOKEN_PATH = 'key.token'
CERTIFICATE_PATH = '/etc/nginx/ssl/nginx.crt'

logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=logging.DEBUG, format='%(asctime)-15s|%(levelname)-8s|%(process)d|%(name)s|%(module)s|%(message)s')


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
        if 'jova' in message.text.lower() or '/' in message.text[0]:  # jova, I choose you!
            logging.info(
                "[from {0}] [message ['{1}']]".format(str(message.from_user).encode('utf-8'), message.text.encode('utf-8')))
            chat_id = message.chat_id
            answer = jova_answer(message.text.lower())
            md = False
            if answer:
                if isinstance(answer, tuple):
                    if answer[1]:
                        if answer[1] == 'markdown':
                            md = True
                        answer = answer[0]
                else:
                    answer = jova_replace(answer)
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                if md:
                    parse_mode = telegram.ParseMode.MARKDOWN
                else:
                    parse_mode = None
                bot.sendMessage(chat_id=chat_id, text=answer, reply_to_message_id=message.message_id,
                                parse_mode=parse_mode)


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
    #if token == webapp.config['TOKEN']:
    if token == extract_token(TOKEN_PATH):
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        # do something, man!
        try:
            jova_do_something(update.message)
        except Exception as e:
            if 'CREATOR_CHAT_ID' in webapp.config.keys():
                bot.sendMessage(chat_id=webapp.config['CREATOR_CHAT_ID'], text='Jova rotto!')
            logging.exception('Something broke\n{0}', e)

        # jova return something ffs!
        return "ok", 200
    else:
        logging.critical('Token not accepted => token={0} - TOKEN[{1}]'.format(token, TOKEN))
        return "ko", 403


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
        abort(403)

    logging.info(res)

    return 'ok', 200


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

    # load jovabot modules - crazy stuff
    load_modules()
    init_modules()

    # telegram bot api token
    try:
        webapp.config['TOKEN'] = os.environ['JOVABOT_API_TOKEN']
    except Exception as e:
        logging.exception('failed to get JOVABOT_API_TOKEN', e)
        webapp.config['TOKEN'] = extract_token(TOKEN_PATH)

    # creator chat id - send exceptions to its chat_id
    try:
        webapp.config['CREATOR_CHAT_ID'] = os.environ['JOVABOT_CREATOR_CHAT_ID']
    except Exception as e:
        logging.exception('failed to get JOVABOT_CREATOR_CHAT_ID', e)
        webapp.config['CREATOR_CHAT_ID'] = 0

    global bot
    bot = telegram.Bot(token=webapp.config['TOKEN'])

    logging.debug(webapp.config)


if __name__ == '__main__':
    webapp.run()
