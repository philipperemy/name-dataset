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

    def __init__(self, threshold=0.0):
        first_names_filename = Path(os.path.dirname(__file__)) / 'v2/first_names.zip'
        last_names_filename = Path(os.path.dirname(__file__)) / 'v2/last_names.zip'
        self.first_names = self._read_names_from_zip(first_names_filename, threshold)
        self.last_names = self._read_names_from_zip(last_names_filename, threshold)

    @staticmethod
    def _read_names_from_zip(zip_file, threshold):
        with zipfile.ZipFile(zip_file) as z:
            with z.open(z.filelist[0]) as f:
                lines = f.read().decode('utf8').strip().splitlines()

                names = {}
                for line in lines:
                    parts = line.split(',')
                    frequency = float(parts[1])
                    if frequency < threshold:
                        break
                    names[parts[0].lower()] = frequency

                return names

    def search_first_name(self, first_name, use_upper_case=False):
        return _query(self.first_names, first_name, use_upper_case)

    def search_last_name(self, last_name, use_upper_case=False):
        return _query(self.last_names, last_name, use_upper_case)
