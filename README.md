# nocaselist - A case-insensitive list for Python

[![Version on Pypi](https://img.shields.io/pypi/v/nocaselist.svg)](https://pypi.python.org/pypi/nocaselist/)
[![Test status (master)](https://github.com/pywbem/nocaselist/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/pywbem/nocaselist/actions/workflows/test.yml?query=branch%3Amaster)
[![Docs status (master)](https://readthedocs.org/projects/nocaselist/badge/?version=latest)](https://readthedocs.org/projects/nocaselist/builds/)
[![Test coverage (master)](https://coveralls.io/repos/github/pywbem/nocaselist/badge.svg?branch=master)](https://coveralls.io/github/pywbem/nocaselist?branch=master)

# Overview

Class
[NocaseList](https://nocaselist.readthedocs.io/en/stable/reference.html#nocaselist.NocaseList)
is a case-insensitive list that preserves the lexical case of its items.

Example:

    $ python
    >>> from nocaselist import NocaseList

    >>> list1 = NocaseList(['Alpha', 'Beta'])

    >>> print(list1)  # Any access is case-preserving
    ['Alpha', 'Beta']

    >>> 'ALPHA' in list1  # Any lookup or comparison is case-insensitive
    True

The
[NocaseList](https://nocaselist.readthedocs.io/en/stable/reference.html#nocaselist.NocaseList)
class supports the functionality of the built-in
[list class of Python 3.8](https://docs.python.org/3.8/library/stdtypes.html#list)
on all Python versions it supports (except for being case-insensitive, of
course).

The case-insensitivity is achieved by matching any key values as their
casefolded values. By default, the casefolding is performed with
[str.casefold()](https://docs.python.org/3/library/stdtypes.html#str.casefold)
for unicode string keys and with
[bytes.lower()](https://docs.python.org/3/library/stdtypes.html#bytes.lower)
for byte string keys. The default casefolding can be overridden with a
user-defined casefold method.

# Installation

To install the latest released version of the nocaselist package into
your active Python environment:

    $ pip install nocaselist

The nocaselist package has no prerequisite Python packages.

For more details and alternative ways to install, see
[Installation](https://nocaselist.readthedocs.io/en/stable/intro.html#installation).

# Documentation

- [Documentation](https://nocaselist.readthedocs.io/en/stable/)

# Change History

- [Change history](https://nocaselist.readthedocs.io/en/stable/changes.html)

# Contributing

For information on how to contribute to the nocaselist project, see
[Contributing](https://nocaselist.readthedocs.io/en/stable/development.html#contributing).

# License

The nocaselist project is provided under the [Apache Software License
2.0](https://raw.githubusercontent.com/pywbem/nocaselist/master/LICENSE).
