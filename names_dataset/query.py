import os


def _query(search_set, key, use_upper_case):
    if use_upper_case and key.title() != key:
        return False
    return key.strip().lower() in search_set


class NameDataset:
    FIRST_NAME_SEARCH = 0
    LAST_NAME_SEARCH = 1

    def __init__(self):
        first_names_filename = os.path.join(os.path.dirname(__file__), 'first_names.all.txt')
        with open(first_names_filename, 'r', errors='ignore', encoding='utf8') as r:
            self.first_names = set(r.read().strip().split('\n'))
        last_names_filename = os.path.join(os.path.dirname(__file__), 'last_names.all.txt')
        with open(last_names_filename, 'r', errors='ignore', encoding='utf8') as r:
            self.last_names = set(r.read().strip().split('\n'))

    def search_first_name(self, first_name, use_upper_case=False):
        return _query(self.first_names, first_name, use_upper_case)

    def search_last_name(self, last_name, use_upper_case=False):
        return _query(self.last_names, last_name, use_upper_case)


if __name__ == '__main__':
    import sys

    if sys.version_info < (3, 0):
        print('Please use Python3+')
        exit(1)

    if len(sys.argv) < 2:
        print('Give names separated by a comma as input.')
        sys.exit(1)
    m = NameDataset()
    names_list = sys.argv[1].split(',')
    print('----- First names ----')
    print('Name'.ljust(30), 'Present?')
    for name in names_list:
        # ljust just for aesthetic reasons ;)
        print(str(name).ljust(30), m.search_first_name(name))

    print('----- Last names ----')
    print('Name'.ljust(30), 'Present?')
    for name in names_list:
        # ljust just for aesthetic reasons ;)
        print(str(name).ljust(30), m.search_last_name(name))
    sys.exit(0)
