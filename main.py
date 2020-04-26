import os
import sys

from evaluate import read_dict_file
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
    for word in words:
        if m.search_first_name(word, use_upper_case=True):
            output += '\e[44m'
            output += word
            output += '\e[0m'
        elif m.search_last_name(word, use_upper_case=True):
            output += '\e[46m'
            output += word
            output += '\e[0m'

        else:
            output += word
        output += ' '
    print(output)


if __name__ == '__main__':
    main()
