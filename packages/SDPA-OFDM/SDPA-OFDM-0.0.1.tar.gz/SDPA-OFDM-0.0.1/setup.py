from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Software OFDM Modulator'
LONG_DESCRIPTION = 'This package provides capability modulate a user-defined message into I and Q for usage in a SDR'

# Setting up
setup(
    name="SDPA-OFDM",
    version=VERSION,
    author="Sebastien Deriaz",
    author_email="sebastien.deriaz1@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'ofdm', 'modulation', 'modulator', 'sdr'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)