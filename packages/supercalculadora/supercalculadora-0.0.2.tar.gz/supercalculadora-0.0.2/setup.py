from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.2'
DESCRIPTION = 'supercalc'
LONG_DESCRIPTION = 'supercalc'

# Setting up
setup( 
    name="supercalculadora",
    version=VERSION,
    author="Gustavo",
    author_email="<gustavodanieldetoledo@gmail.com.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)