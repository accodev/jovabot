# coding=utf-8

import unittest

from modules import learn


class TestLearnModule(unittest.TestCase):
    def setUp(self):
        learn.init()
        learn.clear()

    def test_learn_one(self):
        resp_ = learn.get_answer('jova se ti dico miao tu rispondi ciao')
        self.assertEqual(resp_[1], 'sticker')

    def test_do_not_learn_this(self):
        resp_ = learn.get_answer('jova non imparare questo')
        self.assertEqual(resp_[0], None)

    def test_learn_and_repeat_one(self):
        self.assertEqual(learn.get_answer('jova se ti dico miao tu rispondi ciao')[1], 'sticker')
        self.assertEqual(learn.get_answer('jova miao')[0], "ciao")

    def test_learn_and_repeat_two(self):
        self.assertEqual(learn.get_answer('jova se ti dico miao tu rispondi ciao')[1], 'sticker')
        self.assertEqual(learn.get_answer('jova se ti dico miao tu rispondi bau')[1], 'sticker')
        self.assertTrue(learn.get_answer('jova miao')[0] in ["ciao", "bau"])

    def test_learn_one_with_space_in_trigger(self):
        self.assertEqual(learn.get_answer('jova se ti dico ciao mamma tu rispondi ciao')[1], 'sticker')
        self.assertEqual(learn.get_answer('jova ciao mamma')[0], "ciao")

    def test_learn_one_with_spaces(self):
        self.assertEqual(learn.get_answer('jova se ti dico ciao mamma tu rispondi guarda come mi diverto')[1], 'sticker')
        self.assertEqual(learn.get_answer('jova ciao mamma')[0], "guarda come mi diverto")

    def test_learn_one_with_symbols(self):
        self.assertEqual(learn.get_answer('jova se ti dico scazzi? tu rispondi si puppa!')[1], 'sticker')
        self.assertEqual(learn.get_answer('jova scazzi?')[0], "si puppa!")

    def test_learn_multiple_with_aphostrophe(self):
        self.assertEqual(learn.get_answer("jova se ti dico ma guercio? tu rispondi come va con l'HC?")[1], 'sticker')
        self.assertEqual(learn.get_answer("jova se ti dico ma guercio? tu rispondi Guercio? Puppaaa!")[1], 'sticker')

        expected_ = ["come va con l'HC?", "Guercio? Puppaaa!"]

        self.assertEqual(learn.get_all("ma guercio?"), expected_)

    def test_key_not_found(self):
        self.assertEqual(learn.get_answer('jova scazzi?')[0], None)

    def test_learn_one_trigger_not_precise(self):
        self.assertEqual(learn.get_answer('jova se ti dico perla tu rispondi abito non fa il monaco')[1], 'sticker')
        self.assertEqual(learn.get_answer('jova una perla?')[0], "abito non fa il monaco")


if __name__ == '__main__':
    unittest.main()
