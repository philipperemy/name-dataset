import os
from setuptools import setup, find_packages

VERSION = '1.4.0'

package_name = find_packages()[0]

setup(
    name='names-dataset',
    version=VERSION,
    description='Probably the biggest dataset of Names, worldwide',
    author='Philippe Remy',
    license='MIT',
    packages=[package_name],
    include_package_data=True,
    data_files=[(package_name, [os.path.join(package_name, 'first_names.all.txt'),
                                os.path.join(package_name, 'last_names.all.txt')])]
)
