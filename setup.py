from distutils.core import setup

setup(
    name='Biodiscovery',
    version='0.1.0',
    author='Gregory Znoyko',
    #author_email='jrh@example.com',
    packages=['auto_microarray', 'auto_ngs'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    #license='LICENSE.txt',
    #description='Useful towel-related stuff.',
    #long_description=open('README.txt').read(),
    install_requires=[
        "pylint==1.9.1",
        "pandas==0.23.0",
        "xlrd==1.1.0",
    ],
)