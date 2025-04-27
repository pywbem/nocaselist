
.. _`Change log`:

Change log
==========


nocaselist 2.1.0
----------------

Released: 2024-04-27

**Incompatible changes:**

* Dropped support for Python 3.6 and 3.7 because they are out of service and
  to simplify development dependencies. (issue #178)

* Dev: Changed 'make install' to no longer perform an editable install, but
  a standalone install, since pip will remove support for editable installs.
  (related to issue #152)

* Dev: Removed support for the env.var TEST_INSTALLED that used the installed
  package for testing, for simplicity. Now, the local package in the repository
  main directory is always used for testing.

**Bug fixes:**

* Addressed safety issues up to 2025-04-27.

* Dev: Added missing dependencies for development.

* Test: Fixed the issue that coveralls was not found in the test workflow on MacOS
  with Python 3.9-3.11, by running it without login shell. Added Python 3.11 on
  MacOS to the normal tests.

* Fixed new issues of Pylint 3.3.

**Enhancements:**

* Added support for Python 3.13. This required increasing the minimum version
  of several packages needed for development. (issue #203)

* Added '__version_tuple__' with the integer versions. (related to issue #152)

* Dev: Changed from setup.py to using pyproject.toml. (issue #152)

**Cleanup:**

* Dev: Split safety policy files into one for installation dependencies and one
  for development dependencies. (issue #170, related to issue #152)

* Dev: Split minimum-constraints.txt file into one for installation dependencies
  and one for development dependencies. (related to issue #152)

* Dev: Cleanup in the Makefile. (related to issue #152)

* Docs: Changed versions shown for the documentation to be master and the
  latest fix version of each minor version. Changed documentation links in
  README file to reference the master version.


nocaselist 2.0.3
----------------

Released: 2024-08-18

**Bug fixes:**

* Dev: Fixed safety issues up to 2024-08-18.

* Test: Fixed new issues from pylint 3.2.

* Docs: Fixed missing Python 3.12 in Trove classifiers.

**Cleanup:**

* Test: Increased vrsions of GitHub Actions plugins used, to eliminate warnings
  about node v16.


nocaselist 2.0.2
----------------

Released: 2024-05-08

**Bug fixes:**

* Fixed incorrect formatting of package description on Pypi by setting the
  correct content type in setup.py. (issue #157)

**Enhancements:**

* Test: Added support for testing on Python 3.12. (issue #159)

* Test: Added a step to the test workflow for displaying the tree of all
  package dependencies using pipdeptree. (issue #153)

* Test: Added a new make target 'check_reqs' that checks missing package
  dependencies, and added a step to the test workflow that runs it.
  (issue #155)

**Cleanup:**

* Converted any use of percent-style formatting strings and most use of
  'format()' to f-strings. (issue #154)


nocaselist 2.0.1
----------------

Released: 2024-05-04

**Incompatible changes:**

* Installation of this package using "setup.py" is no longer supported.
  Use "pip" instead.

**Bug fixes:**

* Fixed safety issues up to 2024-05-04.

* Test: Removed setup.py based installs from "make installtest", since one
  of them started installing a pre-release of a package on an unsupported Python
  version. The recommendation has been for a while now to no longer use

* Docs: Added RTD config file .readthedocs.yaml

* In the Github Actions test workflow for Python 3.6 and 3.7, changed
  macos-latest back to macos-12 because macos-latest got upgraded from macOS 12
  to macOS 14 which no longer supports these Python versions.

* Test: Fixed issues resulting from removal of support for pytest.warns(None)
  in pytest version 8.

**Enhancements:**

* Improvements for safety check tool: Made passing the safety check mandatory;
  Fixed safety issues; Separated the safety check into a separate make target;
  Added a safety policy file.

* Test: Moved the Safety run to the end of the test workflow because it regularly
  fails due to new issues introduced by other packages, in order to surface
  our own issues in the test runs in any case.

* Added support for a new make target 'authors' that generates an AUTHORS.md
  file from the git commit history. Added the invocation of 'make authors' to
  the description of how to release a version in the development
  documentation.


nocaselist 2.0.0
----------------

Released: 2023-06-01

**Incompatible changes:**

* Removed support for Python 2.7, 3.4, 3.5. The minimum required Python version
  is now 3.6. This was needed in order to add Python type hints.

**Bug fixes:**

* Fixed coveralls issues with KeyError and HTTP 422 Unprocessable Entity.

* Added support for passing slices to '__setitem__()' and '__delitem__()'.
  Expanded the testcases accordingly.

* Fixed incorrect error handling when passing objects of unsupported types to
  the right hand operand of the rich comparison methods of NocaseList. This
  previously caused AttributeError "'list' object has no attribute 'lower'"
  and TypeError "'int' object is not iterable" to be raised which was confusing.
  This is now handled by returning 'NotImplemented' from these methods as
  recommended by Python, causing TypeError with a proper message to be raised
  by Python.

**Enhancements:**

* Resurrected support for byte strings as list values in the default
  implementation of the casefold method. The list can now contains unicode
  strings and byte strings.

* Added type hints and type checking with MyPy (issue #96).



nocaselist 1.1.0
----------------

Released: 2023-01-21

**Incompatible changes:**

* The default casefolding method on Python 3 was changed from `str.lower()`
  to `str.casefold()`. This changes the matching of the case-insensitive values.
  This shold normally be an improvement, but in case you find that you are
  negatively affected by this change, you can go back to the `str.lower()`
  method by overriding the `NocaseDict.__casefold__()` method with a method
  that calls `str.lower()`. (issue #95)

**Enhancements:**

* Added support for Python 3.11.

* Changed the default casefolding method on Python 3 to be `str.casefold()` in
  order to improve Unicode support. On Python 2, it remains `str.lower()`.
  Added support for user-defined casefolding. (issue #95)

* Added support for storing `None` as a value in a NocaseList. Previously, that
  was rejected with `AttributeError` since the casefold method was attempted to
  be called on the `None` value. (part of issue #95)


nocaselist 1.0.6
----------------

Released: 2022-08-04

**Bug fixes:**

* Various fixes in dependencies and test environment.


nocaselist 1.0.5
----------------

Released: 2022-03-27

**Bug fixes:**

* Mitigated the coveralls HTTP status 422 by pinning coveralls-python to
  <3.0.0 (issue #55).

* Fixed a dependency error that caused importlib-metadata to be installed on
  Python 3.8, while it is included in the Python base.

* Fixed new issues raised by Pylint 2.10.

* Disabled new Pylint issue 'consider-using-f-string', since f-strings were
  introduced only in Python 3.6.

* Fixed install error of wrapt 1.13.0 on Python 2.7 on Windows due to lack of
  MS Visual C++ 9.0 on GitHub Actions, by pinning it to <1.13.

* Fixed TypeError when running Sphinx due to using docutils 0.18 on Python 2.7.

* Fixed error when installing virtualenv in install test on Python 2.7.

* Fixed that the added setup.py commands (test, leaktest, installtest) were not
  displayed. They are now displayed at verbosity level 1 (using '-v').

**Enhancements:**

* Enhanced test matrix on GitHub Actions to always include Python 2.7 and
  Python 3.4 on Ubuntu and Windows, and Python 2.7 and Python 3.5 on macOS.

* Support for Python 3.10: Added Python 3.10 in GitHub Actions tests, and in
  package metadata.

**Cleanup:**

* Removed old tools that were needed on Travis and Appveyor but no longer on
  GitHub Actions: remove_duplicate_setuptools.py, retry.bat


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
