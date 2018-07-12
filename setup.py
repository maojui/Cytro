import sys
from setuptools import setup, find_packages
# import cryptools

__name__ = 'cryptools'
__version__ = '0.0.2'
__author__ = 'Neptune (maojui0427@gmail.com)'
__license__ = 'MIT'


setup(name=__name__,
    version=__version__,
    author=__author__,
    author_email='maojui0427@gmail.com',
    license=__license__,
    url='https://github.com/maojui/cryptools',
    description='Some cryptography tools for CTF',
    keywords=['CTF','cryptools','cyrpto'],
    packages=['cryptools','cryptools.RSA','cryptools.DSA','cryptools.CBC','cryptools.Classical'],
    provides=['cryptools'],
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
