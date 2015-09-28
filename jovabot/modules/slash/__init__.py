# this module is used to handle slash commands (/about, /help, etc.)
import os

slash_commands = {}


def init():
    global slash_commands
    slash_commands = {
        'about': jova_about,
        'about@jovanottibot': jova_about,
        'help': jova_help,
        'help@jovanottibot': jova_help
    }


def get_answer(message):
    if message[0] == '/':
        return handle_slash_command(message[1:])
    return None


def jova_about():
    return 'Info about this bot @ github.com/shevraar/jovabot', 'plain-text'


def jova_help():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    help_path = os.path.join(package_directory, 'HELP.md')
    with open(help_path) as f:
        return f.read(), 'markdown'
    

def handle_slash_command(slash_command):
    func = slash_commands.get(slash_command, lambda: None)
    return func()


if __name__ == '__main__':
    # eventually put all of this shit under unit tests
    print(get_answer('/about'))
    print(get_answer('/help'))
    print(get_answer('test'))
    print(get_answer('////'))
    print(get_answer('test /slash'))
    init()
    print('after init')
    print(get_answer('/about'))
    print(get_answer('/help'))
    print(get_answer('test'))
    print(get_answer('////'))
    print(get_answer('test /slash'))
