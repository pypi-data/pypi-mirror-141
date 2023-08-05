import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py sdist', 'setup.py check -r -s']):
    raise ImportError('This package is parked by RedTachyon. See https://github.com/RedTachyon/putout for more information.')

setup(
    name="putout",
    author='RedTachyon',
    url='https://github.com/RedTachyon/putout',
    description='This package is parked by mattsb42. See https://github.com/RedTachyon/putout for more information.',
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
