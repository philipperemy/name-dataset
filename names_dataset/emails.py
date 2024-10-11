import re
from collections import Counter
from typing import Dict

import numpy as np

from names_dataset import NameDataset


def _compute_score(ranks: Dict):
    values = {a: b for a, b in ranks['rank'].items() if b is not None}.values()
    if len(values) == 0:
        return float('-inf')
    return -min(values)


def _score(nd: NameDataset, candidate: str):
    if len(candidate) == 0:
        return float('-inf')
    first_name = nd.search(candidate)['first_name']
    last_name = nd.search(candidate)['last_name']
    if first_name is None and last_name is None:
        return float('-inf')
    if first_name is not None and last_name is not None:
        s1 = _compute_score(first_name)
        s2 = _compute_score(last_name)
        return max(s1, s2)
    if first_name is not None:
        return _compute_score(first_name)
    if last_name is not None:
        return _compute_score(last_name)


# Function to infer the best split between first and last name
def _infer_best_split(nd: NameDataset, full_name: str):
    max_score = _score(nd, full_name)
    best_split = (full_name, None)

    # Try all possible ways to split the full_name
    for i in range(0, len(full_name)):  # Start at 1 to ensure both parts have characters
        first = full_name[:i]
        last = full_name[i:]

        # Calculate total score for the split
        total_score = _score(nd, first) + _score(nd, last)

        # If this split has a higher score, update the best split
        if total_score > max_score:
            max_score = total_score
            best_split = (first, last)

    return best_split, max_score


def _general_score(nd: NameDataset, candidate: str):
    c = nd.search(candidate)
    if c['first_name'] is not None and c['last_name'] is not None:
        s1 = _compute_score(c['first_name'])
        s2 = _compute_score(c['last_name'])
        return max(s1, s2)
    return float('-inf')


def try_to_split_with_two_last_names(nd: NameDataset, email: str):
    c = Counter()
    for i in range(1, len(email)):
        first_name, last_name = extract_names_from_email(nd, email[0:i])
        if first_name is not None:
            c[first_name] += 1
        if last_name is not None:
            c[last_name] += 1
    most_common = c.most_common(1)
    if len(most_common) > 0:
        candidate1 = most_common[0][0]
        candidate2, candidate3 = extract_names_from_email(nd, email.replace(candidate1, ''))

        if candidate2 is None or candidate3 is None:
            # if candidate2 is not None:
            #     return candidate1, None, None
            # if candidate3 is not None:
            #     return candidate1, candidate3, None
            return candidate1, None, None

        fn1, ln1 = _infer_first_and_last_names(candidate1, candidate2, nd)
        fn2, ln2 = _infer_first_and_last_names(candidate1, candidate3, nd)
        fn3, ln3 = _infer_first_and_last_names(candidate2, candidate3, nd)

        real_first_name = Counter([fn1, fn2, fn3]).most_common(1)[0][0]
        last_names = list({candidate1, candidate2, candidate3} - {real_first_name})
        last_name1 = last_names[0]
        last_name2 = last_names[1]
        if email.index(last_name1) < email.index(last_name2):
            last_name1, last_name2 = last_name1, last_name2
        else:
            last_name1, last_name2 = last_name2, last_name1
        return real_first_name, last_name1, last_name2
    return None, None, None


def extract_names_from_email(nd: NameDataset, email: str):
    email = email.strip()
    if '@' not in email:
        email += '@gmail.com'

    email = ''.join([e for e in list(email) if not e.isnumeric()])

    prefix, suffix = email.split('@')

    no_names = ['contact', 'sales', 'info', 'hello', 'reply', 'service', 'client']
    for no_name in no_names:
        if no_name in prefix:
            return None, None

    if 'contact' in prefix:
        return None, None

    for e in ['.', '_', '-']:
        if prefix.count(e) >= 2:
            c_list = prefix.split(e)
            scores = [_general_score(nd, c) for c in c_list]
            a, b = np.array(c_list)[np.argsort(scores)][-2:]
            email = f'{a}.{b}@{suffix}'

    patterns = [
        r"(?P<first>[a-zA-Z]+)\.(?P<last>[a-zA-Z]+)@",  # first.last@example.com
        r"(?P<first>[a-zA-Z]+)_(?P<last>[a-zA-Z]+)@",  # first_last@example.com
        r"(?P<last>[a-zA-Z]+)\.(?P<first>[a-zA-Z]+)@",  # last.first@example.com
        r"(?P<first>[a-zA-Z]+)-(?P<last>[a-zA-Z]+)@",  # first-last@example.com
        r"(?P<first>[a-zA-Z])[._](?P<last>[a-zA-Z]+)@",  # f.last@example.com or f_last@example.com
        r"(?P<first>[a-zA-Z]+)[._](?P<last>[a-zA-Z])[._]@",  # first.l@example.com or first_l@example.com
    ]

    # Try matching each pattern with the email
    first_name, last_name = None, None
    had_matched = False
    for pattern in patterns:
        match = re.match(pattern, email)
        if match:
            first_name = match.group('first').capitalize()
            last_name = match.group('last').capitalize()
            had_matched = True
            break

    if not had_matched:
        prefix = email.split('@')[0]
        (first_name, last_name), max_score = _infer_best_split(nd, prefix)

    if first_name is not None and len(first_name) == 1:
        first_name = None
    if last_name is not None and len(last_name) == 1:
        last_name = None

    if first_name is not None and last_name is not None:
        first_name, last_name = _infer_first_and_last_names(first_name, last_name, nd)

    if first_name is not None:
        first_name = first_name.lower()

    if last_name is not None:
        last_name = last_name.lower()

    return first_name, last_name


def _infer_first_and_last_names(first_name, last_name, nd):
    fn_1 = nd.search(first_name)['first_name']
    ln_1 = nd.search(last_name)['last_name']
    fn_2 = nd.search(first_name)['last_name']
    ln_2 = nd.search(last_name)['first_name']
    if fn_1 is not None and ln_1 is not None and fn_2 is not None and ln_2 is not None:
        score_1 = _compute_score(fn_1) + _compute_score(ln_1)
        score_2 = _compute_score(fn_2) + _compute_score(ln_2)
        if score_2 > score_1:
            first_name, last_name = last_name, first_name
    return first_name, last_name
