# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="CPCC",
    version="0.1",
    packages=['reminder'],
    scripts=['cpccAndUnicom.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'reminder': ['*.msg'],
    },


    # metadata for upload to PyPI
    author="HK",
    author_email="me@example.com",
    description="This is an Example Package",
    license="PSF",
    keywords="cpcc shot message",
    url="http://www.baidu.com",  # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
