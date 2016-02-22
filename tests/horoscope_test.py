import unittest

from modules import horoscope


class TestHoroscopeModule(unittest.TestCase):
    def setUp(self):
        horoscope.init()

    def test_oroscopo_per_pesci(self):
        resp_ = horoscope.get_answer('jova l\'oroscopo per i pesci')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_oroscopo_invocato_con_slash(self):
        resp_ = horoscope.get_answer('/jova l\'oroscopo per stocazzo')
        self.assertIsNone(resp_)

    def test_oroscopo_per_piu_segni(self):
        resp_ = horoscope.get_answer('jova l\'oroscopo per i pesci il sagittario e il cancro')
        self.assertIsInstance(resp_, tuple)
        self.assertGreaterEqual(len(resp_[0]), 1)

    def test_oroscopo_per_segno_sconosciuto(self):
        resp_ = horoscope.get_answer('jova l\'oroscopo per l\'arcere')
        self.assertIsInstance(resp_, tuple)
        self.assertIsNone(resp_[0])

    def test_oroscopo_sgrammaticato(self):
        resp_ = horoscope.get_answer('jova orscopo per i pscie')
        self.assertIsNone(resp_)


if __name__ == '__main__':
    unittest.main()
