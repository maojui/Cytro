import sys
from distutils.core import setup

import cryptools

setup(name='cryptools',
      version=cryptools.__version__,
      author='Neptune',
      author_email='maojui0427@gmail.com',
      license='MIT',
      url='https://github.com/maojui/cryptools',
      description='Some cryptography tools for CTF',
      keywords='CTF RSA ... ',
      packages=['cryptools','cryptools.RSA','cryptools.DSA','cryptools.CBC','cryptools.Classical'],
      provides=['cryptools'],
      classifiers=['Natural Language :: Chinese',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Competition :: Capture the Flag',
                   'Topic :: Security :: Cryptography',
                  ],
     )
