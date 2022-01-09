# python artifacts.py /home/philippe/tmp/curate/ /home/philippe/tmp/ok
import json
import operator
from argparse import ArgumentParser
from pathlib import Path

from generation.generate_stats import norm_dict


def get_script_arguments():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', type=Path, required=True)
    parser.add_argument('--output_dir', type=Path, required=True)
    parser.add_argument('--trunc_first_names_count', type=int, default=100_000)
    parser.add_argument('--trunc_last_names_count', type=int, default=100_000)
    parser.add_argument('--max_countries_per_name', type=int, default=5)
    return parser.parse_args()


def generate(by_country, gender_by, country_by, trunc_values, max_countries_per_name, output_filename):
    print(f'filter_records: {output_filename}.')
    names_all = {}
    for country_code, names in by_country.items():
        desc_tuples = sorted(names.items(), key=operator.itemgetter(1), reverse=True)
        desc_tuples = desc_tuples[0:trunc_values]
        names_by_country = {
            a: {**{'gender': gender_by[a] if a in gender_by else {}},
                **{'country': country_by[a] if a in country_by else {}},
                **{'popularity': {country_code: b}}}
            for a, b in dict(desc_tuples).items()
        }
        for k in names_by_country.keys():
            if k not in names_all:
                names_all[k] = {'popularity': {}}
            merged_scores = {**names_all[k]['popularity'], **names_by_country[k]['popularity']}
            names_all[k] = names_by_country[k]
            names_all[k]['popularity'] = merged_scores
    del names_all['']

    normalizers = {
        'gender': lambda x: round(x, 3),
        'country': lambda x: round(x, 3),
        'popularity': lambda x: round(x, 6)
    }
    for name, name_info in names_all.items():
        # truncate to maximum 5 countries. It will later be normalized.
        name_info['country'] = dict(sorted(
            name_info['country'].items(),
            key=operator.itemgetter(1),
            reverse=True)[0:max_countries_per_name])
        countries = name_info['country'].keys()
        # to make sure the country support is the same.
        name_info['popularity'] = {
            c: name_info['popularity'][c]
            if c in name_info['popularity'] else 0.0 for c in countries
        }
        if '' in name_info['gender']:
            del name_info['gender']['']  # only M and F. Discard N/A.
        norm_dict(name_info, apply=normalizers)

    with open(output_filename, 'w', encoding='utf8', errors='ignore') as w:
        json.dump(names_all, w, indent=2, ensure_ascii=False, sort_keys=True)


def main():
    args = get_script_arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    first_by_country_file = Path(args.input_dir) / 'first_by_country.json'
    last_by_country_file = Path(args.input_dir) / 'last_by_country.json'
    gender_by_first_file = Path(args.input_dir) / 'gender_by_first.json'
    country_by_first_file = Path(args.input_dir) / 'country_by_first.json'
    country_by_last_file = Path(args.input_dir) / 'country_by_last.json'
    with open(gender_by_first_file) as r:
        gender_by_first = json.load(r)
    print('1', gender_by_first_file)
    with open(country_by_first_file) as r:
        country_by_first = json.load(r)
    print('2', country_by_first_file)
    with open(first_by_country_file) as r:
        first_by_country = json.load(r)
    print('3', first_by_country_file)
    with open(last_by_country_file) as r:
        last_by_country = json.load(r)
    print('4', last_by_country_file)
    with open(country_by_last_file) as r:
        country_by_last = json.load(r)
    print('5', country_by_last_file)

    # FIRST NAMES.
    generate(
        first_by_country, gender_by_first, country_by_first,
        args.trunc_first_names_count, args.max_countries_per_name,
        args.output_dir / 'first_names.json'
    )

    # LAST NAMES.
    generate(
        last_by_country, {}, country_by_last,
        args.trunc_last_names_count, args.max_countries_per_name,
        args.output_dir / 'last_names.json'
    )


if __name__ == '__main__':
    main()
