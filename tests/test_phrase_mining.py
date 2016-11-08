import unittest
from topmine import phrase_mining as pm


class TestTopmine(unittest.TestCase):

    corpus = [x.split(' ') for x in ['hola soy danny']]
    expected_counter = {'hola': 1, 'soy': 1, 'danny': 1,
                        'hola soy': 1, 'soy danny': 1,
                        'hola soy danny': 1
                       }

    def test_phrase_frequency(self):
        counter = pm.phrase_frequency(corpus=self.corpus, min_support=0)
        for phrase, count in self.expected_counter.items():
            with self.subTest(name=phrase):
                self.assertEqual(count, counter[phrase])

if __name__ == '__main__':
    unittest.main()
