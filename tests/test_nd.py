import unittest
from pathlib import Path

from names_dataset import NameDataset, NameWrapper

nd = NameDataset()
supported_country_codes = [
    'AE', 'AF', 'AL', 'AO', 'AR', 'AT', 'AZ', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BN',
    'BO', 'BR', 'BW', 'CA', 'CH', 'CL', 'CM', 'CN', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DJ',
    'DK', 'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FR', 'GB', 'GE', 'GH', 'GR',
    'GT', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IR', 'IS', 'IT',
    'JM', 'JO', 'JP', 'KH', 'KR', 'KW', 'KZ', 'LB', 'LT', 'LU', 'LY', 'MA', 'MD', 'MO',
    'MT', 'MU', 'MV', 'MX', 'MY', 'NA', 'NG', 'NL', 'NO', 'OM', 'PA', 'PE', 'PH', 'PL',
    'PR', 'PS', 'PT', 'QA', 'RS', 'RU', 'SA', 'SD', 'SE', 'SG', 'SI', 'SV', 'SY', 'TM',
    'TN', 'TR', 'TW', 'US', 'UY', 'YE', 'ZA'
]


class TestNd(unittest.TestCase):

    def test_country_codes(self):
        self.assertListEqual(supported_country_codes, nd.get_country_codes(alpha_2=True))
        self.assertListEqual(supported_country_codes, sorted([a.alpha_2 for a in nd.get_country_codes()]))
        # nd.get_top_names(country_alpha2='GB', gender='male')
        # print(json.dumps(nd.search('Mike'), indent=2))

    def test_get_top_names(self):
        tn = nd.get_top_names(n=101)
        self.assertListEqual(supported_country_codes, sorted(tn.keys()))
        for s in supported_country_codes:
            self.assertEqual(len(tn[s]['F']), 101)
            self.assertEqual(len(tn[s]['M']), 101)

    def test_get_top_names_gender_male(self):
        tn = nd.get_top_names(n=22, gender='male')
        self.assertListEqual(supported_country_codes, sorted(tn.keys()))
        for s in supported_country_codes:
            self.assertTrue('F' not in tn[s])
            self.assertTrue('M' in tn[s])
            self.assertEqual(len(tn[s]['M']), 22)

    def test_get_top_names_gender_female(self):
        tn = nd.get_top_names(n=11, gender='f')
        self.assertListEqual(supported_country_codes, sorted(tn.keys()))
        for s in supported_country_codes:
            self.assertTrue('F' in tn[s])
            self.assertTrue('M' not in tn[s])
            self.assertEqual(len(tn[s]['F']), 11)

    def test_get_top_names_gender_country(self):
        tn = nd.get_top_names(n=11, gender='f', country_alpha2='GB')
        self.assertListEqual(['GB'], sorted(tn.keys()))
        self.assertTrue('F' in tn['GB'])
        self.assertTrue('M' not in tn['GB'])
        self.assertEqual(len(tn['GB']['F']), 11)

    def test_get_top_names_country(self):
        tn = nd.get_top_names(n=33, country_alpha2='GB')
        self.assertListEqual(['GB'], sorted(tn.keys()))
        self.assertTrue('F' in tn['GB'])
        self.assertTrue('M' in tn['GB'])
        self.assertEqual(len(tn['GB']['M']), 33)
        self.assertEqual(len(tn['GB']['F']), 33)

    def test_get_top_names_country_last(self):
        tn = nd.get_top_names(n=33, country_alpha2='GB', use_first_names=False)
        tn_first = nd.get_top_names(n=33, country_alpha2='GB')
        self.assertListEqual(['GB'], sorted(tn.keys()))
        self.assertNotEqual(tn_first['GB']['F'], tn['GB'])
        self.assertNotEqual(tn_first['GB']['M'], tn['GB'])

    def test_get_top_names_invalid_input(self):
        self.assertRaises(ValueError, nd.get_top_names, n=-1)
        self.assertRaises(ValueError, nd.get_top_names, n=0)
        self.assertRaises(ValueError, nd.get_top_names, use_first_names=False, gender='M')
        self.assertRaises(ValueError, nd.get_top_names, use_first_names=False, gender='unknown')

    def test_search(self):
        s = nd.search('Mike')
        self.assertTrue('first_name' in s)
        self.assertTrue('last_name' in s)
        self.assertTrue('country' in s['first_name'])
        self.assertTrue('gender' in s['first_name'])
        self.assertTrue('rank' in s['first_name'])
        self.assertTrue('country' in s['last_name'])
        self.assertTrue('gender' in s['last_name'])
        self.assertTrue('rank' in s['last_name'])
        self.assertTrue(s['first_name']['gender']['Male'] > s['first_name']['gender']['Female'])
        self.assertTrue(len(s['last_name']['gender']) == 0)

        s2 = nd.search('unknown')
        self.assertIsNone(s2['first_name'])
        self.assertIsNone(s2['last_name'])

        self.assertEqual(nd.search('Mike'), nd.search('mike'))
        self.assertNotEqual(nd.search('Mickael'), nd.search('mike'))

    def test_exhaustive_search(self):
        all_names = list(nd.first_names.keys())
        for name in all_names:
            nd.search(name)

    def test_load(self):
        fn_nd = NameDataset(load_last_names=False)
        self.assertIsNone(fn_nd.search('Mike')['last_name'])
        self.assertIsNotNone(fn_nd.search('Mike')['first_name'])

        fn_nd = NameDataset(load_first_names=False)
        self.assertIsNone(fn_nd.search('Mike')['first_name'])
        self.assertIsNotNone(fn_nd.search('Mike')['last_name'])

    def test_forbes_users(self):
        pct_is_none = []
        with open(Path(__file__).parent / 'names-from-forbes-wp_users.txt') as r:
            for name_to_query in r.read().strip().splitlines():
                pct_is_none.append(nd.search(name_to_query)['first_name'])
        pct_is_none = 100 * sum([a is None for a in pct_is_none]) / len(pct_is_none)
        self.assertLess(pct_is_none, 0.4)

    def test_10000_english(self):
        pct_is_none = []
        with open(Path(__file__).parent / 'google-10000-english-no-names.txt') as r:
            for name_to_query in r.read().strip().splitlines():
                pct_is_none.append(nd.search(name_to_query)['first_name'])
        pct_is_none = 100 * sum([a is None for a in pct_is_none]) / len(pct_is_none)
        self.assertGreater(pct_is_none, 60)

    def test_no_na_in_gender(self):
        result = nd.get_top_names(n=10, country_alpha2='JP', use_first_names=True)
        self.assertNotIn('N/A', result['JP'])
        self.assertIn('M', result['JP'])
        self.assertTrue('F', result['JP'])

    def test_name_wrapper(self):
        z = NameWrapper(nd.search('Sarah'))
        p = NameWrapper(nd.search('Philippe'))
        self.assertEqual(z.gender, 'Female')
        self.assertEqual(p.gender, 'Male')
        self.assertEqual(z.country, 'United Kingdom')
        self.assertEqual(p.country, 'France')
        self.assertEqual(z.describe, 'Female, United Kingdom')
        self.assertEqual(p.describe, 'Male, France')
