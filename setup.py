"""Blaster setup.

The blaster setup module commonly containing Python packaging code.
"""
from os.path import dirname, join

from setuptools import setup, find_packages


def get_version():
    """Return the package version.

    :return: blaster package version
    :rtype: str
    """
    with open(join(dirname(__file__), 'blaster', '__init__.py')) as fp:
        for line in fp.readlines():
            if line.startswith("__version__"):
                return line.split('"' if '"' in line else "'")[1]


setup(
    name='blaster',
    version=get_version(),
    description='Blast off a list of tasks concurrently calling each tasks '
                'methods defined',
    url='https://github.com/ryankwilliams/blaster',
    author='Ryan Williams',
    author_email='rwilliams5262@gmail.com',
    license='GPLv3',
    package_dir={'': '.'},
    packages=find_packages('.'),
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ]
)
