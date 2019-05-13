import sys
from setuptools import setup, find_packages

__name__ = 'cytro'
__version__ = '0.1.2'
__author__ = 'Neptune (maojui0427@gmail.com)'
__license__ = 'MIT'

setup(name=__name__,
    version=__version__,
    author=__author__,
    author_email='maojui0427@gmail.com',
    license=__license__,
    url='https://github.com/maojui/cytro',
    description='cryptography tools for CTF crypto challennge',
    keywords=['CTF','cryptools','crypto','cytro'],
    packages=find_packages(),
    provides=['cytro'],
    install_requires=[
        'pycrypto==2.6.1',
        'pillow==4.3.0',
        'sympy==1.0.0',
    ],
    classifiers=['Natural Language :: Chinese',
        'License :: OSI Approved :: MIT License',
        'Topic :: Competition :: Capture the Flag',
        'Topic :: Security :: Cryptography',
    ],
)
