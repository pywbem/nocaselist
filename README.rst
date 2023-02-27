nocaselist - A case-insensitive list for Python
===============================================

.. image:: https://badge.fury.io/py/nocaselist.svg
    :target: https://pypi.python.org/pypi/nocaselist/
    :alt: Version on Pypi

.. image:: https://github.com/pywbem/nocaselist/workflows/test/badge.svg?branch=master
    :target: https://github.com/pywbem/nocaselist/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/nocaselist/badge/?version=latest
    :target: https://readthedocs.org/projects/nocaselist/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/pywbem/nocaselist/badge.svg?branch=master
    :target: https://coveralls.io/github/pywbem/nocaselist?branch=master
    :alt: Test coverage (master)


Overview
--------

Class `NocaseList`_ is a case-insensitive list that preserves the lexical case
of its items.

Example:

.. code-block:: bash

    $ python
    >>> from nocaselist import NocaseList

    >>> list1 = NocaseList(['Alpha', 'Beta'])

    >>> print(list1)  # Any access is case-preserving
    ['Alpha', 'Beta']

    >>> 'ALPHA' in list1  # Any lookup or comparison is case-insensitive
    True

The `NocaseList`_ class supports the functionality of the built-in
`list class of Python 3.8`_ on all Python versions it supports (except for being
case-insensitive, of course).

.. _list class of Python 3.8: https://docs.python.org/3.8/library/stdtypes.html#list
.. _NocaseList: https://nocaselist.readthedocs.io/en/stable/reference.html#nocaselist.NocaseList

The case-insensitivity is achieved by matching any key values as their
casefolded values. By default, the casefolding is performed with
`str.casefold()`_ for unicode string keys and with `bytes.lower()`_ for byte
string keys.
The default casefolding can be overridden with a user-defined casefold method.

.. _str.casefold(): https://docs.python.org/3/library/stdtypes.html#str.casefold
.. _bytes.lower(): https://docs.python.org/3/library/stdtypes.html#bytes.lower


Installation
------------

To install the latest released version of the nocaselist package into your
active Python environment:

.. code-block:: bash

    $ pip install nocaselist

The nocaselist package has no prerequisite Python packages.

For more details and alternative ways to install, see `Installation`_.

.. _Installation: https://nocaselist.readthedocs.io/en/stable/intro.html#installation

Documentation
-------------

* `Documentation <https://nocaselist.readthedocs.io/en/stable/>`_

Change History
--------------

* `Change history <https://nocaselist.readthedocs.io/en/stable/changes.html>`_

Contributing
------------

For information on how to contribute to the nocaselist project, see
`Contributing <https://nocaselist.readthedocs.io/en/stable/development.html#contributing>`_.


License
-------

The nocaselist project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/pywbem/nocaselist/master/LICENSE>`_.
