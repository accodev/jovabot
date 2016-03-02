# this module is used to handle slash commands (/about, /help, etc.)
import os
import logging

slash_commands = {}


def init():
    global slash_commands
    slash_commands = {
        'about': jova_about,
        'help': jova_help,
        'start': jova_help
    }


def get_answer(message):
    if message.startswith('/'):
        return handle_slash_command(message[1:].split("@")[0])
    return None


def jova_about():
    return 'Info about this bot @ github.com/shevraar/jovabot', 'plain-text'


def jova_help():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    help_path = os.path.join(package_directory, os.pardir, os.pardir, 'HELP.md')
    with open(help_path) as f:
        return f.read(), 'markdown'


def handle_slash_command(slash_command):
    func = slash_commands.get(slash_command, lambda: None)
    if func:
        logging.info('slash_command requested => [{0}]'.format(slash_command))
    return func()
