from distutils.core import setup
from setuptools import find_packages
setup(
    name='tokenquery',
    packages=find_packages(),
    version='0.1.1',
    description='Tokenquery - query language for tokens ',
    author='Ramtin Seraj',
    author_email='mehdizadeh.ramtin@gmail.com',
    url='https://github.com/ramtinms/tokenquery',
    download_url='https://github.com/ramtinms/tokenquery/tarball/0.1',
    keywords=['natural language processing', 'nlp', 'regex', 'regular expressions', 'tokenizer', 'query'],
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
        "conllu",
        "google-api-python-client",
        "sklearn",
    ],

)
