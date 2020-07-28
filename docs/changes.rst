
.. _`Change log`:

Change log
==========


nocaselist 1.0.1.dev1
---------------------

Released: not yet

**Incompatible changes:**

**Deprecations:**

**Bug fixes:**

**Enhancements:**

* Test: Coveralls now runs on all python versions, merging the result.
  (See issue #17)

* Test: Added support for testing against standard list, by adding a new
  make target 'testlist', and running that test on the Travis and Appveyor CIs.
  (See issue #16)

* Removed enforcement of Python version at run time. (See issue #18)

* Docs: Switched Sphinx theme to sphinx_rtd_theme (See issue #19)

* Docs: Documented exceptions that can be raised, in all methods.

* Docs: Switched links to items in the Python documentation to go to Python 3
  instead of Python 2.

* Added support for the clear() method on Python 2.7 (where the built-in list
  class does not support it yet). (See issue #30)

* Docs: Clarified that NocaseList supports the functionality of the built-in
  list class as of Python 3.8, including all methods that have been added since
  Python 2.7, on all Python versions.

**Cleanup:**

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/pywbem/nocaselist/issues


nocaselist 1.0.0
----------------

Released: 2020-07-21

Initial release.
