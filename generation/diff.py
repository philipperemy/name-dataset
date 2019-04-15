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
    a = read_dict_file(sys.argv[1])
    b = read_dict_file(sys.argv[2])
    if sys.argv[4] == '-':
        c = sorted(set(a) - set(b))
    else:
        c = sorted(set(a).union(set(b)))
    write_dict_file(sys.argv[3], c)


if __name__ == '__main__':
    main()
