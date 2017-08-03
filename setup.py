from os.path import dirname, join
from re import compile

from setuptools import setup


def version():
    """Return the package version."""
    init = open(join(dirname(__file__), 'blaster', '__init__.py')).read()
    return compile(r'''__version__ = ['"]([0-9.]+)['"]'''). \
        search(init).group(1)


setup(
    name='blaster',
    version=version(),
    description='Blast off a list of tasks concurrently calling each tasks '
                'methods defined',
    url='https://github.com/rywillia/blaster',
    author='Ryan Williams',
    author_email='rwilliams5262@gmail.com',
    license='GPLv3',
    packages=['blaster'],
    zip_safe=False
)
