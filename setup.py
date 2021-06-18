
from setuptools import setup, find_packages
from bergwerk.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='bergwerk',
    version=VERSION,
    description='Bergwerk berechnen',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Justus Freudenberg',
    author_email='justus@freudenberg.me',
    url='https://github.com/hpymountain/bergwerk',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'bergwerk': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        bergwerk = bergwerk.main:main
    """,
)
