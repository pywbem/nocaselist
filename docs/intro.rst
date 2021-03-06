
.. _`Introduction`:

Introduction
============


.. _`Functionality`:

Functionality
^^^^^^^^^^^^^

Class :class:`nocaselist.NocaseList` is a case-insensitive list that preserves
the lexical case of its items.

Example:

.. code-block:: bash

    $ python
    >>> from nocaselist import NocaseList
    >>> list1 = NocaseList(['Alpha', 'Beta'])

    >>> print(list1)  # Any access is case-preserving
    ['Alpha', 'Beta']

    >>> 'ALPHA' in list1  # Any lookup or comparison is case-insensitive
    True

The :class:`~nocaselist.NocaseList` class supports the functionality of the
built-in `list class of Python 3.8`_ on all Python versions it supports (except
for being case-insensitive, of course). This includes the ``clear()`` and
``copy()`` methods added in Python 3.3 to the built-in ``list`` class.

.. _list class of Python 3.8: https://docs.python.org/3.8/library/stdtypes.html#list


.. _`Supported environments`:

Supported environments
^^^^^^^^^^^^^^^^^^^^^^

The package does not have any dependencies on the type of operating system and
is regularly tested in CI systems on the following operating systems:

* Ubuntu, native Windows, CygWin, OS-X / macOS

The package is supported on the following Python versions:

* Python: 2.7, 3.4 and all higher 3.x versions


.. _`Installing`:

Installing
^^^^^^^^^^

* Prerequisites:

  - The Python environment into which you want to install must be the current
    Python environment, and must have at least the following Python packages
    installed:

    - setuptools
    - wheel
    - pip

* Install the nocaselist package and its prerequisite
  Python packages into the active Python environment:

  .. code-block:: bash

      $ pip install nocaselist


.. _`Installing a different version`:

Installing a different version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The examples in the previous sections install the latest version of
nocaselist that is released on `PyPI`_.
This section describes how different versions of nocaselist
can be installed.

* To install an older released version of nocaselist,
  Pip supports specifying a version requirement. The following example installs
  nocaselist version 0.1.0
  from PyPI:

  .. code-block:: bash

      $ pip install nocaselist==0.1.0

* If you need to get a certain new functionality or a new fix that is
  not yet part of a version released to PyPI, Pip supports installation from a
  Git repository. The following example installs nocaselist
  from the current code level in the master branch of the
  `nocaselist repository`_:

  .. code-block:: bash

      $ pip install git+https://github.com/pywbem/nocaselist.git@master#egg=nocaselist

.. _nocaselist repository: https://github.com/pywbem/nocaselist

.. _PyPI: https://pypi.python.org/pypi


.. _`Verifying the installation`:

Verifying the installation
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can verify that nocaselist is installed correctly by
importing the package into Python (using the Python environment you installed
it to):

.. code-block:: bash

    $ python -c "import nocaselist; print('ok')"
    ok


.. _`Package version`:

Package version
---------------

The version of the nocaselist package can be accessed by
programs using the ``nocaselist.__version__`` variable:

.. autodata:: nocaselist._version.__version__

Note: For tooling reasons, the variable is shown as
``nocaselist._version.__version__``, but it should be used as
``nocaselist.__version__``.


.. _`Compatibility and deprecation policy`:

Compatibility and deprecation policy
------------------------------------

The nocaselist project uses the rules of
`Semantic Versioning 2.0.0`_ for compatibility between versions, and for
deprecations. The public interface that is subject to the semantic versioning
rules and specificically to its compatibility rules are the APIs and commands
described in this documentation.

.. _Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html

The semantic versioning rules require backwards compatibility for new minor
versions (the 'N' in version 'M.N.P') and for new patch versions (the 'P' in
version 'M.N.P').

Thus, a user of an API or command of the nocaselist project
can safely upgrade to a new minor or patch version of the
nocaselist package without encountering compatibility
issues for their code using the APIs or for their scripts using the commands.

In the rare case that exceptions from this rule are needed, they will be
documented in the :ref:`Change log`.

Occasionally functionality needs to be retired, because it is flawed and a
better but incompatible replacement has emerged. In the
nocaselist project, such changes are done by deprecating
existing functionality, without removing it immediately.

The deprecated functionality is still supported at least throughout new minor
or patch releases within the same major release. Eventually, a new major
release may break compatibility by removing deprecated functionality.

Any changes at the APIs or commands that do introduce
incompatibilities as defined above, are described in the :ref:`Change log`.

Deprecation of functionality at the APIs or commands is
communicated to the users in multiple ways:

* It is described in the documentation of the API or command

* It is mentioned in the change log.

* It is raised at runtime by issuing Python warnings of type
  ``DeprecationWarning`` (see the Python :mod:`py:warnings` module).

Since Python 2.7, ``DeprecationWarning`` messages are suppressed by default.
They can be shown for example in any of these ways:

* By specifying the Python command line option: ``-W default``
* By invoking Python with the environment variable: ``PYTHONWARNINGS=default``

It is recommended that users of the nocaselist project
run their test code with ``DeprecationWarning`` messages being shown, so they
become aware of any use of deprecated functionality.

Here is a summary of the deprecation and compatibility policy used by
the nocaselist project, by version type:

* New patch version (M.N.P -> M.N.P+1): No new deprecations; no new
  functionality; backwards compatible.
* New minor release (M.N.P -> M.N+1.0): New deprecations may be added;
  functionality may be extended; backwards compatible.
* New major release (M.N.P -> M+1.0.0): Deprecated functionality may get
  removed; functionality may be extended or changed; backwards compatibility
  may be broken.


.. _'Python namespaces`:

Python namespaces
-----------------

This documentation describes only the external APIs of the
nocaselist project, and omits any internal symbols and
any sub-modules.
