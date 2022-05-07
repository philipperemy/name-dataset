from pathlib import Path

from setuptools import setup, find_packages

VERSION = '3.1.0'

packages = find_packages()
package_name = packages[0]
data_files = list(Path(package_name).glob('**/*.txt')) + list(Path(package_name).glob('**/*.zip'))
data_files = [str(d) for d in data_files]

setup(
    name='names-dataset',
    version=VERSION,
    description='The python library to handle names',
    author='Philippe Remy',
    license='MIT',
    install_requires=['pycountry'],
    packages=[package_name],
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    include_package_data=True,
    data_files=[(package_name, data_files)]
)
