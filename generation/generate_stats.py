# python artifacts.py /home/philippe/tmp/curate/ /home/philippe/tmp/ok
import json
import sys
from argparse import ArgumentParser
from collections import defaultdict, Counter
from pathlib import Path

from tqdm import tqdm


def get_script_arguments():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', type=Path, required=True)
    parser.add_argument('--output_dir', type=Path, required=True)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--option', choices=
    ['gender_by_first', 'first_by_country',
     'last_by_country', 'country_by_first', 'country_by_last', 'all'],
                        required=True)
    return parser.parse_args()


def norm_dict(dic: dict, apply=None, keys_to_avoid_norm=None):
    if keys_to_avoid_norm is None:
        keys_to_avoid_norm = set()
    for k in dic.keys():
        v = dic[k]
        if k in keys_to_avoid_norm:
            scale = 1
        else:
            scale = sum(v.values())
        while True:
            try:
                if apply is not None:
                    dic[k] = {a: apply[k](b / scale) for a, b in v.items()}
                else:
                    dic[k] = {a: b / scale for a, b in v.items()}
                break
            except ZeroDivisionError:
                scale += 1e-6


def main():
    args = get_script_arguments()
    print(f'Option: {args.option}.')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    gender_by_first = first_by_country = last_by_country = country_by_first = country_by_last = None
    if args.option in ['gender_by_first', 'all']:
        gender_by_first = defaultdict(Counter)
    if args.option in ['first_by_country', 'all']:
        first_by_country = defaultdict(Counter)
    if args.option in ['last_by_country', 'all']:
        last_by_country = defaultdict(Counter)
    if args.option in ['country_by_first', 'all']:
        country_by_first = defaultdict(Counter)
    if args.option in ['country_by_last', 'all']:
        country_by_last = defaultdict(Counter)

    files = sorted(args.input_dir.glob('*.*'))  # sorted -> deterministic
    if args.debug:
        files = files[0:20]
    with tqdm(files, file=sys.stdout) as bar:
        for c in bar:
            bar.set_description(c.name)
            with open(c, encoding='utf8') as r:
                buffer = r.read().strip()
            buffer_lines = buffer.splitlines()
            for v in buffer_lines:
                first, last, gender, country = v.split(',')

                # country -> frequencies of first names
                if first_by_country is not None:
                    first_by_country[country].update([first])

                # country -> frequencies of last names
                if last_by_country is not None:
                    last_by_country[country].update([last])

                # first -> gender is male or female?
                if gender_by_first is not None:
                    gender_by_first[first].update([gender])

                # first -> which country?
                if country_by_first is not None:
                    country_by_first[first].update([country])

                # last -> which country?
                if country_by_last is not None:
                    country_by_last[last].update([country])

    if first_by_country is not None:
        norm_dict(first_by_country)
        with open(args.output_dir / 'first_by_country.json', 'w', encoding='utf8') as w:
            json.dump(first_by_country, fp=w, indent=2, ensure_ascii=False)

    if last_by_country is not None:
        norm_dict(last_by_country)
        with open(args.output_dir / 'last_by_country.json', 'w', encoding='utf8') as w:
            json.dump(last_by_country, fp=w, indent=2, ensure_ascii=False)

    if gender_by_first is not None:
        norm_dict(gender_by_first)
        with open(args.output_dir / 'gender_by_first.json', 'w', encoding='utf8') as w:
            json.dump(gender_by_first, fp=w, indent=2, ensure_ascii=False)

    if country_by_first is not None:
        norm_dict(country_by_first)
        with open(args.output_dir / 'country_by_first.json', 'w', encoding='utf8') as w:
            json.dump(country_by_first, fp=w, indent=2, ensure_ascii=False)

    if country_by_last is not None:
        norm_dict(country_by_last)
        with open(args.output_dir / 'country_by_last.json', 'w', encoding='utf8') as w:
            json.dump(country_by_last, fp=w, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
