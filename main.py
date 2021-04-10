import os
import sys

from generation.diff import read_dict_file
from names_dataset import NameDataset


def main():
    m = NameDataset()
    if os.path.isfile(sys.argv[1]):
        words = read_dict_file(sys.argv[1])
    else:
        words = [sys.argv[1]]

    # cheap word tokenizer.
    words = ' '.join(words).replace('.', ' ').replace('?', ' ').replace('\'', ' ').split(' ')
    output = ''

    threshold = 5
    for word in words:
        if m.search_first_name(word, use_upper_case=False) > threshold:
            output += '**'
            output += word.upper()
            output += '**'
        else:
            output += word
        output += ' '
    print(output)


if __name__ == '__main__':
    main()
