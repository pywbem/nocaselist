
.. _`Change log`:

Change log
==========


nocaselist 1.0.4
----------------

Released: 2021-01-01

**Enhancements:**

* Migrated from Travis and Appveyor to GitHub Actions. This required changes
  in several areas including dependent packages used for testing and coverage.
  This did not cause any changes on dependent packages used for the installation
  of the package.


nocaselist 1.0.3
----------------

Released: 2020-10-04

**Bug fixes:**

* Test: Fixed issue with virtualenv raising AttributeError during installtest
  on Python 3.4. (see issue #43)

* Added checking for no expected warning. Adjusted a testcase to accomodate
  the new check. (see issue #45)


nocaselist 1.0.2
----------------

Released: 2020-09-11

**Bug fixes:**

* Fixed an AttributeError during unpickling. (See issue #37)

**Enhancements:**

* Optimized pickling a NocaseList object by serializing only the original
  list, but not the second lower-cased list. This optimization is only
  implemented for Python 3.

* Added tests for pickling and unpickling.

**Cleanup:**

* Suppressed new Pylint issue 'super-with-arguments', because this package
  still supports Python 2.7.


nocaselist 1.0.1
----------------

Released: 2020-07-28

**Bug fixes:**

* Fixed the incorrect behavior of the '+' and '+=' operators to now (correctly)
  treat the right hand operand as an iterable of items to be added, instead of
  (incorrectly) as a single item. For '+', the right hand operand now must
  be a list, consistent with the built-in list class. (See issue #25)

* Fixed the incorrect behavior of the `*` and `*=` operators to now validate
  that the number is an integer and raise TypeError otherwise, consistent with
  the built-in list class. (See issue #27)

**Enhancements:**

* Removed enforcement of Python version at run time. (See issue #18)

* Added support for the clear() method on Python 2.7 (where the built-in list
  class does not support it yet). (See issue #30)

* The `*=` operator now modifies the left hand operand list in place, instead of
  returning a new list. Note that both is correct behavior. (Part of issue #27)

* Improved the performance of initializing a NocaseList object by copying
  the internal lower-cased list when possible, instead of rebuilding it from
  the original list.

* Test: Coveralls now runs on all python versions, merging the result.
  (See issue #17)

* Test: Added support for testing against standard list, by adding a new
  make target 'testlist', and running that test on the Travis and Appveyor CIs.
  (See issue #16)

* Docs: Clarified that NocaseList supports the functionality of the built-in
  list class as of Python 3.8, including all methods that have been added since
  Python 2.7, on all Python versions.

* Docs: Documented exceptions that can be raised, in all methods.

* Docs: Switched Sphinx theme to sphinx_rtd_theme (See issue #19)

* Docs: Switched links to items in the Python documentation to go to Python 3
  instead of Python 2.


nocaselist 1.0.0
----------------

Released: 2020-07-21

Initial release.
