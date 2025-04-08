from setuptools import setup, find_packages

VERSION = '3.3.1'

packages = find_packages()
package_name = packages[0]

setup(
    name='names-dataset',
    version=VERSION,
    description='The python library to handle names',
    author='Philippe Remy',
    license='MIT',
    install_requires=['pycountry', 'numpy'],
    packages=[package_name],
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    include_package_data=True,
    package_data={
        package_name: ['**/*.txt', '**/*.pkl.gz']
    }
)
