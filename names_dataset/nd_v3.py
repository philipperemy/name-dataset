import copy
import json
import operator
import os
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Optional

import pycountry


def _query(search_set, key):
    key = key.strip().title()
    if key in search_set:
        return search_set[key]
    return None


def _arg(d: dict, f=max) -> str:
    try:
        g_ = {a: b for a, b in d.items() if b is not None}
        return f(g_, key=g_.get)
    except ValueError:
        return ''


class NameWrapper:

    def __init__(self, d: dict):  # result of NameDataset.search()
        self.d = d

    def _attrib(self, attrib_name):
        key = 'first_name' if self.d.get('first_name') is not None else 'last_name'
        if self.d[key] is None:
            return ''
        return _arg(self.d[key][attrib_name], max)

    @property
    def country(self):
        return self._attrib('country')

    @property
    def gender(self):
        return self._attrib('gender')

    @property
    def describe(self):
        return f'{self.gender}, {self.country}'


class NameDataset:

    def __init__(self, load_first_names=True, load_last_names=True):
        if not load_first_names and not load_last_names:
            raise ValueError('Select either [load_first_names=True] and/or [load_last_names=True].')
        first_names_filename = Path(os.path.dirname(__file__)) / 'v3/first_names.zip'
        last_names_filename = Path(os.path.dirname(__file__)) / 'v3/last_names.zip'
        self.first_names = self._read_json_from_zip(first_names_filename) if load_first_names else None
        self.last_names = self._read_json_from_zip(last_names_filename) if load_last_names else None

    @staticmethod
    def _read_json_from_zip(zip_file):
        with zipfile.ZipFile(zip_file) as z:
            with z.open(z.filelist[0]) as f:
                return json.load(f)

    def search(self, name: str):
        key = name.strip().title()
        fn = self._post_process(self.first_names.get(key)) if self.first_names is not None else None
        ln = self._post_process(self.last_names.get(key)) if self.last_names is not None else None
        return {'first_name': fn, 'last_name': ln}

    def get_country_codes(self, alpha_2=False):
        lookup_table = self.first_names if self.first_names is not None else self.last_names
        countries_list = [list(a['country'].keys()) for a in lookup_table.values()]
        countries = set()
        for c in countries_list:
            for cc in c:
                countries.add(cc)
        if alpha_2:
            return sorted(countries)
        else:
            return [pycountry.countries.get(alpha_2=a) for a in countries]

    def get_top_names(
            self,
            n: int = 100,
            use_first_names: bool = True,
            country_alpha2: Optional[str] = None,
            gender: Optional[str] = None
    ):
        if n <= 0:
            raise ValueError('[n] has to be positive.')
        if use_first_names and self.first_names is None:
            raise ValueError('Select [load_first_names=True] at init.')
        if not use_first_names and self.last_names is None:
            raise ValueError('Select [load_last_names=True] at init.')
        if not use_first_names and gender is not None:
            raise ValueError('Selecting a gender for last names is invalid.')
        if gender is not None:
            if gender.title() in ['M', 'Male']:
                gender = 'M'
            elif gender.title() in ['F', 'Female']:
                gender = 'F'
            else:
                raise ValueError('Invalid gender value.')
        ranks_per_country = defaultdict(dict)
        lookup_table = self.first_names if use_first_names else self.last_names
        for name, name_info in lookup_table.items():
            if len(name_info['gender']) == 0:
                gender_ = 'N/A'  # default
            elif len(name_info['gender']) == 1:
                gender_ = list(name_info['gender'].keys())[0]
            else:
                gender_ = 'M' if name_info['gender']['M'] > name_info['gender']['F'] else 'F'
            if gender is None or gender == gender_:
                for country_, rank in name_info['rank'].items():
                    if country_alpha2 is None or country_ == country_alpha2:
                        if gender_ not in ranks_per_country[country_]:
                            ranks_per_country[country_][gender_] = []
                        ranks_per_country[country_][gender_].append((name, rank))
        for country_, ranks in ranks_per_country.items():
            for gender_id in ['F', 'M', 'N/A']:
                if gender_id in ranks:
                    ranks[gender_id] = [a[0] for a in sorted(
                        ranks[gender_id],
                        key=operator.itemgetter(1), reverse=False
                    )][0:n]
        if not use_first_names:
            ranks_per_country = {a: b['N/A'] for a, b in ranks_per_country.items()}
        else:
            for country_code, values in ranks_per_country.items():
                if 'N/A' in values:
                    del values['N/A']
        return dict(ranks_per_country)

    @staticmethod
    def _post_process(result):
        if result is None:
            return None
        result = copy.deepcopy(result)  # to avoid side effects.
        gender = {'M': 'Male', 'F': 'Female'}
        for country in result['country'].keys():
            if country not in result['rank']:
                result['rank'][country] = None
        return {
            'country': {pycountry.countries.get(alpha_2=a).name: b for a, b in result['country'].items()},
            # 'popularity_score': {pycountry.countries.get(alpha_2=a).name: b for a, b in result['popularity'].items()},
            'gender': {gender[a]: b for a, b in result['gender'].items()},
            'rank': {pycountry.countries.get(alpha_2=a).name: b for a, b in result['rank'].items()}
        }
