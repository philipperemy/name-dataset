import subprocess

from evaluate import read_dict_file
from names_dataset import NameDataset


def main():
    m = NameDataset()
    words = read_dict_file('generation/example_text.txt')
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
    subprocess.check_output(f'echo -e "{output}"', shell=True)


if __name__ == '__main__':
    main()
