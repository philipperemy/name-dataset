import os
import zipfile
from pathlib import Path


def _query(search_set, key, use_upper_case):
    title_key = key.title()
    if use_upper_case and title_key != key:
        return 0.0
    lower_key = key.strip().lower()
    if lower_key in search_set:
        return search_set[lower_key]
    return 0.0


class NameDataset:

    def __init__(self):
        first_names_filename = Path(os.path.dirname(__file__)) / 'v2/first_names.zip'
        last_names_filename = Path(os.path.dirname(__file__)) / 'v2/last_names.zip'
        self.first_names = self._read_names_from_zip(first_names_filename)
        self.last_names = self._read_names_from_zip(last_names_filename)

    @staticmethod
    def _read_names_from_zip(zip_file):
        with zipfile.ZipFile(zip_file) as z:
            with z.open(z.filelist[0]) as f:
                names = f.read().decode('utf8').strip().split('\n')
                # noinspection PyTypeChecker
                names = dict([n.split(',') for n in names])
                names = {k.lower(): float(v) for k, v in names.items()}
                return names

    def search_first_name(self, first_name, use_upper_case=False):
        return _query(self.first_names, first_name, use_upper_case)

    def search_last_name(self, last_name, use_upper_case=False):
        return _query(self.last_names, last_name, use_upper_case)
