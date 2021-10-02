from pathlib import Path

from setuptools import setup, find_packages

VERSION = '2.1.0'

packages = find_packages()
package_name = packages[0]
data_files = list(Path(package_name).glob('**/*.txt')) + list(Path(package_name).glob('**/*.zip'))
data_files = [str(d) for d in data_files]

setup(
    name='names-dataset',
    version=VERSION,
    description='Probably the biggest dataset of Names, worldwide',
    author='Philippe Remy',
    license='MIT',
    packages=[package_name],
    include_package_data=True,
    data_files=[(package_name, data_files)]
)
