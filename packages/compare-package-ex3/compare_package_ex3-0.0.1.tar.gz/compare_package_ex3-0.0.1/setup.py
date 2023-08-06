from gettext import install
from struct import pack
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Compare number'
LONG_DESCRIPTION = 'Compare number package'

setup(
    name="compare_package_ex3",
    version=VERSION,
    author="TranNguyenHanh",
    author_email="tnh210302@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['sympy'],
    keywords=['python', 'compare'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)