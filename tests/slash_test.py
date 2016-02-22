# coding=utf-8

import unittest

from modules import slash


class TestSlashModule(unittest.TestCase):
    def setUp(self):
        slash.init()

    def test_unknown_slash_command(self):
        resp_ = slash.get_answer('/unknownSlashCommand')
        self.assertNotIsInstance(resp_, tuple)
        self.assertIsNone(resp_, None)

    def test_unknown_slash_command_with_botname_attached(self):
        resp_ = slash.get_answer('/unknownSlashCommand@botname')
        self.assertNotIsInstance(resp_, tuple)
        self.assertIsNone(resp_, None)

    def test_help_slash_command(self):
        resp_ = slash.get_answer('/help')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_about_slash_command(self):
        resp_ = slash.get_answer('/about')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_help_slash_command_with_botname_attached(self):
        resp_ = slash.get_answer('/help@botname')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_about_slash_command_with_botname_attached(self):
        resp_ = slash.get_answer('/about@botname')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_slash_command_with_strange_characters(self):
        resp_ = slash.get_answer('/about@dd@dd@dd')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)


if __name__ == '__main__':
    unittest.main()
