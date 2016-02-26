import jovabot
# noinspection PyUnresolvedReferences
from jovabot import webapp as app  # this import is for uwsgi

if __name__ == "__main__":
    jovabot.webapp.run()
