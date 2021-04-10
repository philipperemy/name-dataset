import os
import unittest

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

from names_dataset import NameDataset
from names_dataset import NameDatasetV1

nd1 = NameDatasetV1()
nd = NameDataset()


def read_dict_file(filename):
    with open(filename, 'r', encoding='utf8', errors='ignore') as r:
        lines = r.read().strip().lower().split('\n')
    return lines


class UnitTest(unittest.TestCase):

    def test_1(self):

        self.assertTrue(nd1.search_first_name('Rose', use_upper_case=True))
        self.assertTrue(nd1.search_first_name('Rose', use_upper_case=False))
        self.assertTrue(nd1.search_first_name('rose', use_upper_case=False))
        self.assertFalse(nd1.search_first_name('rose', use_upper_case=True))

        self.assertTrue(nd.search_first_name('Rose', use_upper_case=True))
        self.assertTrue(nd.search_first_name('Rose', use_upper_case=False))
        self.assertTrue(nd.search_first_name('rose', use_upper_case=False))
        self.assertFalse(nd.search_first_name('rose', use_upper_case=True))

        self.assertTrue(nd.search_first_name('영수'))
        self.assertTrue(nd.search_first_name('다은'))
        self.assertTrue(nd.search_first_name('은서'))
        self.assertTrue(nd.search_first_name('은영'))

        self.assertTrue(nd.search_first_name('Abbad'))
        self.assertTrue(nd.search_first_name('Abbad'))
        self.assertTrue(nd.search_first_name('Abbad'))
        self.assertTrue(nd.search_first_name('Abbad'))

        self.assertTrue(nd.search_first_name('محمد'))

    def test_2(self):
        current = os.path.dirname(__file__)
        names = read_dict_file(f'{current}/../eng_dictionary/names-from-forbes-wp_users.txt')
        not_names = read_dict_file(f'{current}/../eng_dictionary/google-10000-english-no-names.txt')
        not_names.extend(read_dict_file(f'{current}/../eng_dictionary/1000-no-names.txt'))

        names = sorted(set(names))
        not_names = sorted(set(not_names))

        # 0 => not a name
        # 1 => name

        for m in [nd, nd1]:

            targets = []
            predictions = []
            for q in names:
                score = m.search_first_name(q)
                if not isinstance(score, bool):
                    score = score > 0
                predictions.append(score)
                targets.append(True)

            for q in not_names:
                score = m.search_first_name(q)
                if not isinstance(score, bool):
                    score = score > 0
                predictions.append(score)
                targets.append(False)

            self.assertTrue(precision_score(y_true=targets, y_pred=predictions) > 0.9)
            self.assertTrue(recall_score(y_true=targets, y_pred=predictions) > 0.9)
            self.assertTrue(f1_score(y_true=targets, y_pred=predictions) > 0.9)
            self.assertTrue(accuracy_score(y_true=targets, y_pred=predictions) > 0.9)
