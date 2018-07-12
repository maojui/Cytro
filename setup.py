import sys
from setuptools import setup, find_packages
import cryptools


setup(name='cryptools',
    version=cryptools.__version__,
    author='Neptune',
    author_email='maojui0427@gmail.com',
    license='MIT',
    url='https://github.com/maojui/cryptools',
    description='Some cryptography tools for CTF',
    # keywords='CTF RSA ... ',
    packages=['cryptools','cryptools.RSA','cryptools.DSA','cryptools.CBC','cryptools.Classical'],
    provides=['cryptools'],
    install_requires=[
        'hashpumpy==1.2',
        'pycrypto==2.6.1',
        'pillow==4.3.0',
    ],
    # packages=find_packages(),
    classifiers=['Natural Language :: Chinese',
        'License :: OSI Approved :: MIT License',
        'Topic :: Competition :: Capture the Flag',
        'Topic :: Security :: Cryptography',
    ],
)
