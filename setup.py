import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def version():
    try:
        return read('VERSION').strip().lstrip('v')
    except:
        return "0.0.0.dev0"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='klaytn-etl-cli',
    version=version(),
    author='Yongchan Hong',
    author_email='chan.hong@krustuniverse.com',
    description='Tools for exporting Klaytn blockchain data to JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/klaytn/klaytn-etl',
    packages=find_packages(exclude=['schemas', 'tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['klaytn', 'etl', 'batch'],
    python_requires='>=3.7.2,<4',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest~=4.3.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'klaytnetl=klaytnetl.cli:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/klaytn/klaytn-etl/issues',
        'Source': 'https://github.com/klaytn/klaytn-etl/tree/klaytn-etl',
    },
)
