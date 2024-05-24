from setuptools import setup, find_packages
from os.path import join, dirname
#import CAPythonsBook.src as f

setup(
    name='CAPythonsBook',
    version='0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts':
            ['CAPythonsBook = CAPythonsBook.src.presentation.cli:main']
        },
    include_package_data=True
)