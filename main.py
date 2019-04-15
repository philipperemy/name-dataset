from evaluate import read_dict_file
from names_dataset import NameDataset
import os
import sys

def main():
    m = NameDataset()
    if os.path.isfile(sys.argv[1]):
        words = read_dict_file('generation/example_text.txt')
    else:
        words = [sys.argv[1]]
    words = ' '.join(words).replace('.', ' ').replace('?', ' ').split(' ')  # cheap word tokenizer.
    output = ''
    for word in words:
        if m.search_first_name(word):
            output += '\e[44m'
            output += word
            output += '\e[0m'
        else:
            output += word
        output += ' '
    print(output)


if __name__ == '__main__':
    main()
