
# Introduction

DameFormats is a python package part of DameLibraries.

In this project, we are experimenting a way, to store the snippets
related to python formats (csv, json, xml, yaml, netcdf, ...) in files
ready to execute unit test.

# Ways executing tests:

    $ cd dameformats
    
    $ ./runtests.sh

    $ nosetests3 tests

    $ nosetests3 tests/test_joke.py:TestJoke.test_is_string

# Pypi

-   To install from local:

    $ pip install -e .

-   To install create tar.gz in dist directory:

    $ python3 setup.py register sdist

-   To upload to pypi:

    $ twine upload dist/dameformats-0.1.tar.gz

-   You can install from Internet in a python virtual environment to check:

    $ python3 -m venv /tmp/funny
    $ cd /tmp/funny
    $ source bin/activate
    $ pip3 install dameformats