import sys


def read_dict_file(filename):
    with open(filename, 'r', encoding='utf8', errors='ignore') as r:
        lines = r.read().strip().lower().split('\n')
    return lines


def write_dict_file(filename, dicts):
    with open(filename, 'w', encoding='utf8') as w:
        for line in dicts:
            w.write(line)
            w.write('\n')


def main():
    names_file = read_dict_file(sys.argv[1])
    eng_dict_file = read_dict_file(sys.argv[2])
    ss = set(eng_dict_file)
    output = []
    for name in names_file:
        if name.split(',')[0] not in ss:
            output.append(name.title())
        else:
            print(f'FILTER: {name}.')
    write_dict_file(sys.argv[3], output)


if __name__ == '__main__':
    main()
