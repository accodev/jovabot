# coding=utf-8

import unittest

from modules import addressbook


class TestAddressbookModule(unittest.TestCase):
    def setUp(self):
        addressbook.init()

    def test_cerca_pizza_a_roma(self):
        resp_ = addressbook.get_answer('jova cercami pizza a roma')
        print(resp_)
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_slash_command(self):
        resp_ = addressbook.get_answer('/cerca')
        self.assertIsNone(resp_)

    def test_trovami_persona_a_roma(self):
        resp_ = addressbook.get_answer('jova trovami rossi a roma')
        print(resp_)
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_non_ho_trovato_nessuno(self):
        resp_ = addressbook.get_answer('jova trovami sarcazzi a digione in francia e pure uno scappellamento a dx')
        print(resp_)
        self.assertIsInstance(resp_, tuple)
        self.assertEqual(resp_[0], 'non ho trovato nessuno')


if __name__ == '__main__':
    unittest.main()
