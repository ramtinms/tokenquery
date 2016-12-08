from distutils.core import setup
from setuptools import find_packages
setup(
    name='tokenregex',
    packages=find_packages(),  #['tokenregex','tokenregex.models','tokenregex.nlp'], # this must be the same as the name above
    version='0.1.14',
    description='NLP at your fingertips',
    author='Ramtin Seraj',
    author_email='mehdizadeh.ramtin@gmail.com',
    url='https://github.com/ramtinms/tokenregex',
    download_url='https://github.com/ramtinms/tokenregex/tarball/0.1',
    keywords=['natural language processing', 'nlp', 'regex', 'tokenizer'], # arbitrary keywords
    classifiers=['Intended Audience :: Information Technology',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Human Machine Interfaces',
                 'Topic :: Scientific/Engineering :: Information Analysis',
                 'Topic :: Text Processing',
                 'Topic :: Text Processing :: Filters',
                 'Topic :: Text Processing :: General',
                 'Topic :: Text Processing :: Indexing',
                 'Topic :: Text Processing :: Linguistic',
                 ],

    install_requires=[
        "requests",
        "nltk",
    ],

)
