from setuptools import setup, find_packages

import codecs

import os


here = os.path.abspath(os.path.dirname(__file__))


with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:

    long_description = "\n" + fh.read()


VERSION = '0.0.5'

DESCRIPTION = 'Tools to make it easier for Python beginners'

LONG_DESCRIPTION = 'Skull Cyber Security Labs adalah modul pembelajaran yang dapat menjalankan fungsi tertentu untuk mempermudahkan kinerja para pemula untuk membangun sebuah program berbahasa indonesia.'


# Setting up

setup(

    name="ScsLabs",

    version=VERSION,

    author="TomsDroid (Tomy Aliyansyah)",

    author_email="<tomsdroid@kingeagle.tech>",

    description=DESCRIPTION,

    long_description_content_type="text/markdown",

    long_description=long_description,

    packages=find_packages(),

    install_requires=['requests', 'bs4'],

    keywords=['scs python', 'pyhon', 'scs', 'skull cyber security', 'pyhon indoneisa', 'information gathering'],

    classifiers=[

        "Development Status :: 1 - Planning",

        "Intended Audience :: Developers",

        "Programming Language :: Python :: 3",

        "Operating System :: Unix",

        "Operating System :: MacOS :: MacOS X",

        "Operating System :: Microsoft :: Windows",

    ]

)
