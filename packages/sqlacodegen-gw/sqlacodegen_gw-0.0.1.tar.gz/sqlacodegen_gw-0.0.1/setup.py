import codecs
import os
import sys
try:
    from setuptools import setup,find_packages
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "sqlacodegen_gw"
PACKAGES = ["sqlacodegen_gw"]
DESCRIPTION = "change columns name fake camel style"
LONG_DESCRIPTION = "change columns name fake camel style for gw"
KEYWORDS = "sqlacodegen_gw"
AUTHOR = "derek"
AUTHOR_EMAIL = "chongchongzl@163.com"
URL = "https://github.com/derek-zl"
VERSION = "0.0.1"
LICENSE = "MIT"
setup(
    name =NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description =LONG_DESCRIPTION,
    classifiers =[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords =KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL, 
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
    entry_points={
      "console_scripts": [
                          "sqlacodegen_gw = sqlacodegen_gw.main:main",
                          ]
      },

)