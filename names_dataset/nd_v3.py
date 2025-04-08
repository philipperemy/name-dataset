import copy
import gzip
import operator
import os
import pickle
from collections import defaultdict
from pathlib import Path
from typing import Optional, Dict, List

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


def _autocomplete_search(
        prefix: str,
        names_dict: Dict[str, Dict],
        n: int = 5,
        gender: Optional[str] = None,
        country_alpha2: Optional[str] = None,
        max_rank: int = 5000
) -> List[Dict]:
    matching_names = []
    for name, info in names_dict.items():
        if name.startswith(prefix) and not name.startswith(prefix + ' '):
            if gender is None or (len(info['gender']) > 0 and gender == max(info['gender'], key=info['gender'].get)):
                matching_names.append(name)
    result = []
    for name in matching_names:
        attrs = names_dict[name]
        ranks = attrs['rank']
        if len(ranks) <= 1:
            continue
        if country_alpha2 is not None:
            if country_alpha2 not in ranks:
                continue
            rank = ranks[country_alpha2]
        else:
            rank = int(sum(ranks.values()) / len(ranks))
        result.append({'name': name, 'rank': rank})
    result = sorted(result, key=lambda x: x['rank'])
    result = [r for r in result if r['rank'] < max_rank][:n]
    return result


def _fuzzy_search(
        fuzzy_name: str,
        names_dict: Dict[str, Dict],
        n: int = 5,
        gender: Optional[str] = None,
        country_alpha2: Optional[str] = None,
) -> List[Dict]:
    from fuzzywuzzy import fuzz
    closest_names = []
    for name, info in names_dict.items():
        similarity = fuzz.ratio(fuzzy_name, name)
        if gender is None or (len(info['gender']) > 0 and gender == max(info['gender'], key=info['gender'].get)):
            closest_names.append((name, similarity))
    closest_names.sort(key=lambda x: x[1], reverse=True)
    result = []
    for name in closest_names[0:n * 5]:
        attrs = names_dict[name[0]]
        ranks = attrs['rank']
        if len(ranks) == 0:
            continue
        if country_alpha2 is not None:
            if country_alpha2 not in ranks:
                continue
            rank = ranks[country_alpha2]
        else:
            rank = int(sum(ranks.values()) / len(ranks))
        result.append({'name': name[0], 'rank': rank})
    result = sorted(result, key=lambda x: x['rank'])[0:n]
    return result


class NameDataset:

    def __init__(self, load_first_names=True, load_last_names=True):
        if not load_first_names and not load_last_names:
            raise ValueError('Select either [load_first_names=True] and/or [load_last_names=True].')
        first_names_filename = Path(os.path.dirname(__file__)) / 'v3/first_names.pkl.gz'
        last_names_filename = Path(os.path.dirname(__file__)) / 'v3/last_names.pkl.gz'
        self.first_names = self._read_pickle_from_gzip(first_names_filename) if load_first_names else None
        self.last_names = self._read_pickle_from_gzip(last_names_filename) if load_last_names else None
        self.country_codes = self.get_country_codes(alpha_2=True)

    def auto_complete(
            self,
            name: str,
            n: int = 5,
            use_first_names: bool = True,
            country_alpha2: Optional[str] = None,
            gender: Optional[str] = None,
            *args, **kwargs
    ) -> List[Dict]:
        name, gender = self._process_inputs(name, use_first_names, gender, country_alpha2)
        names_dict = self.first_names if use_first_names else self.last_names
        return _autocomplete_search(
            n=n, prefix=name, names_dict=names_dict, gender=gender, country_alpha2=country_alpha2, *args, **kwargs
        )

    def fuzzy_search(
            self,
            name: str,
            n: int = 5,
            use_first_names: bool = True,
            country_alpha2: Optional[str] = None,
            gender: Optional[str] = None,
    ) -> List[Dict]:
        name, gender = self._process_inputs(name, use_first_names, gender, country_alpha2)
        names_dict = self.first_names if use_first_names else self.last_names
        return _fuzzy_search(
            n=n, fuzzy_name=name, names_dict=names_dict, gender=gender, country_alpha2=country_alpha2
        )

    @staticmethod
    def _read_pickle_from_gzip(gzip_path):
        with gzip.open(gzip_path, 'rb') as f:
            return pickle.load(f)

    def _process_inputs(
            self,
            name: str,
            use_first_names: bool,
            gender: Optional[str] = None,
            country_alpha2: Optional[str] = None
    ):
        q_name = name.strip().title()
        if use_first_names and self.first_names is None:
            raise ValueError('Select [load_first_names=True] at init.')
        if not use_first_names and self.last_names is None:
            raise ValueError('Select [load_last_names=True] at init.')
        if gender is not None:
            if gender.title() in {'M', 'Male'}:
                gender = 'M'
            elif gender.title() in {'F', 'Female'}:
                gender = 'F'
            else:
                raise ValueError('Invalid gender value.')
        if country_alpha2 is not None and country_alpha2 not in self.country_codes:
            raise ValueError(f'Invalid Country alpha-2 code. Valid are: {",".join(self.country_codes)}.')
        return q_name, gender

    def search(self, name: str):
        key = name.strip().title()
        fn = self._post_process(self.first_names.get(key)) if self.first_names is not None else None
        ln = self._post_process(self.last_names.get(key)) if self.last_names is not None else None
        return {'first_name': fn, 'last_name': ln}

    def get_country_codes(self, alpha_2=False, cache: bool = False):
        if cache and alpha_2:
            return self.country_codes
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
