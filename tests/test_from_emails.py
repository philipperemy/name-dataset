import unittest

from names_dataset import NameDataset
from names_dataset.emails import extract_names_from_email


class TestEmail(unittest.TestCase):

    def test_1(self):
        inputs = [
            'info@skysense.jp',
            'isabelle.remy.fr@gmail.com',
            'philippe.remy@example.com',
            'philipperemy@example.com',
            'philippe.d@example.com',
            'p.remy123@example.com',
            'philippe@example.com',
            'philippe_remy@example.com',
            'remy.philippe@example.com',
            'remyphilippe@example.com',
            'j_remy@example.com',
            'philippe.remy123@example.com',
            'philippe.d@example.com',
            'philippe.d@example.com',
            'j.remy@example.com',
            'remyphilippe123@example.com',
            'philippe-d@example.com',
            'remy_j@example.com',
            'j_remy123@example.com',
            'philippe.remy1@example.com',
        ]
        inputs2 = []
        for i in inputs:
            inputs2.append(i.split('@')[0])

        outputs = [
            [None, None],
            ['isabelle', 'remy'],
            ['philippe', 'remy'],
            ['philippe', 'remy'],
            ['philippe', None],
            [None, 'remy'],
            ['philippe', None],
            ['philippe', 'remy'],
            ['philippe', 'remy'],
            ['philippe', 'remy'],
            [None, 'remy'],
            ['philippe', 'remy'],
            ['philippe', None],
            ['philippe', None],
            [None, 'remy'],
            ['philippe', 'remy'],
            ['philippe', None],
            ['remy', None],
            [None, 'remy'],
            ['philippe', 'remy'],
        ]

        nd = NameDataset()
        for input_, output_ in zip(inputs2, outputs):
            first_name, last_name = extract_names_from_email(nd, input_)
            print(input_)
            self.assertEqual(output_[0], first_name)
            self.assertEqual(output_[1], last_name)
            print('[OK]')
