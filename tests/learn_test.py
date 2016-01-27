# coding=utf-8

import unittest
from jovabot.modules import learn

class TestLearnModule(unittest.TestCase):

    def setUp(self):
        learn.init()
        learn.clear()
        
    def test_learn_one(self):
        resp_ = learn.get_answer('jova se ti dico miao tu rispondi ciao')
        self.assertEqual(resp_, 'OK')
        
    def test_do_not_learn_this(self):
        resp_ = learn.get_answer('jova non imparare questo')
        self.assertEqual(resp_, None)
        
    def test_learn_and_repeat_one(self):
        self.assertEqual(learn.get_answer('jova se ti dico miao tu rispondi ciao'), "OK")
        self.assertEqual(learn.get_answer('jova miao'), "ciao")
        
    def test_learn_and_repeat_two(self):
        self.assertEqual(learn.get_answer('jova se ti dico miao tu rispondi ciao'), "OK")
        self.assertEqual(learn.get_answer('jova se ti dico miao tu rispondi bau'), "OK")
        self.assertTrue(learn.get_answer('jova miao') in ["ciao", "bau"])
        
    def test_learn_one_with_space_in_trigger(self):
        self.assertEqual(learn.get_answer('jova se ti dico ciao mamma tu rispondi ciao'), "OK")
        self.assertEqual(learn.get_answer('jova ciao mamma'), "ciao") 
        
    def test_learn_one_with_spaces(self):
        self.assertEqual(learn.get_answer('jova se ti dico ciao mamma tu rispondi guarda come mi diverto'), "OK")
        self.assertEqual(learn.get_answer('jova ciao mamma'), "guarda come mi diverto")
        
    def test_learn_one_with_symbols(self):
        self.assertEqual(learn.get_answer('jova se ti dico scazzi? tu rispondi si puppa!'), "OK")
        self.assertEqual(learn.get_answer('jova scazzi?'), "si puppa!")
        
    def test_learn_multiple_with_aphostrophe(self):
        self.assertEqual(learn.get_answer("jova se ti dico ma guercio? tu rispondi come va con l'HC?"), "OK")
        self.assertEqual(learn.get_answer("jova se ti dico ma guercio? tu rispondi Guercio? Puppaaa!"), "OK")
        
        expected_ = ["come va con l'HC?", "Guercio? Puppaaa!"]
       
        self.assertEqual(learn.get_all("ma guercio?"), expected_)
        
    def test_key_not_found(self):
        self.assertEqual(learn.get_answer('jova scazzi?'), None)     

if __name__ == '__main__':
    unittest.main()