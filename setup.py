import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def version():
    try:
        return read('VERSION').strip().lstrip('v')
    except:
        return "0.0.0.dev0"

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
        'Programming Language :: Python :: 3.9'
    ],
    keywords=['klaytn', 'etl', 'batch'],
    python_requires='>=3.7.2,<4',
    install_requires=[
        'web3>=5.29,<6',
        # eth-rlp is explicitly written to prevent dependency related issue
        'eth-rlp<0.3',
        'eth-utils==1.10',
        'eth-abi==2.1.1',
        # TODO: This has to be removed when "ModuleNotFoundError: No module named 'eth_utils.toolz'" is fixed at eth-abi
        'python-dateutil>=2.8.0,<3',
        'click==8.0.4',
        'ethereum-dasm==0.1.4',
        'pytz==2022.1',
        'base58',
        'requests',
        'boto3',
        'google-cloud-storage'
    ],
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
