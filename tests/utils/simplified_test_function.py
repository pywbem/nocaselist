# Copyright (C) 2020 Andreas Maier
"""
simplified_test_function - Pytest extension for simplifying test functions.
"""


import functools
import warnings
from collections import namedtuple
from inspect import Signature, Parameter  # type: ignore
import pytest

__all__ = ['simplified_test_function']


# Pytest determines the signature of the test function by unpacking any
# wrapped functions (this is the default of the signature() function it
# uses. We correct this behavior by setting the __signature__ attribute of
# the wrapper function to its correct signature. To do that, we cannot use
# signature() because its follow_wrapped parameter was introduced only in
# Python 3.5. Instead, we build the signature manually.
TESTFUNC_SIGNATURE = Signature(
    parameters=[
        Parameter('desc', Parameter.POSITIONAL_OR_KEYWORD),
        Parameter('kwargs', Parameter.POSITIONAL_OR_KEYWORD),
        Parameter('exp_exc_types', Parameter.POSITIONAL_OR_KEYWORD),
        Parameter('exp_warn_types', Parameter.POSITIONAL_OR_KEYWORD),
        Parameter('condition', Parameter.POSITIONAL_OR_KEYWORD),
    ]
)


def simplified_test_function(test_func):
    """
    A decorator for test functions that simplifies the test function by
    handling a number of things:

    * Skipping the test if the `condition` item in the testcase is `False`,
    * Invoking the Python debugger if the `condition` item in the testcase is
      the string "pdb",
    * Capturing and validating any warnings issued by the test function,
      if the `exp_warn_types` item in the testcase is set,
    * Catching and validating any exceptions raised by the test function,
      if the `exp_exc_types` item in the testcase is set.

    This is a signature-changing decorator. This decorator must be inserted
    after the `pytest.mark.parametrize` decorator so that it is applied
    first (see the example).

    Parameters of the wrapper function returned by this decorator:

    * desc (string): Short testcase description.

    * kwargs (dict): Keyword arguments for the test function.

    * exp_exc_types (Exception or list of Exception): Expected exception types,
      or `None` if no exceptions are expected.

    * exp_warn_types (Warning or list of Warning): Expected warning types,
      or `None` if no warnings are expected.

    * condition (bool or 'pdb'): Boolean condition for running the testcase.
      If it evaluates to `bool(False)`, the testcase will be skipped.
      If it evaluates to `bool(True)`, the testcase will be run.
      The string value 'pdb' will cause the Python pdb debugger to be entered
      before calling the test function.

    Parameters of the test function that is decorated:

    * testcase (testcase_tuple): The testcase, as a named tuple.

    * **kwargs: Keyword arguments for the test function.

    Example::

        TESTCASES_FOO_EQUAL = [
            # desc, kwargs, exp_exc_types, exp_warn_types, condition
            (
                "Equality with different lexical case of name",
                dict(
                    obj1=Foo('Bar'),
                    obj2=Foo('bar'),
                    exp_equal=True,
                ),
                None, None, True
            ),
            # ... more testcases
        ]

        @pytest.mark.parametrize(
            "desc, kwargs, exp_exc_types, exp_warn_types, condition",
            TESTCASES_FOO_EQUAL)
        @pytest_extensions.simplified_test_function
        def test_Foo_equal(testcase, obj1, obj2, exp_equal):

            # The code to be tested
            equal = (obj1 == obj2)

            # Ensure that exceptions raised in the remainder of this function
            # are not mistaken as expected exceptions
            assert testcase.exp_exc_types is None

            # Verify the result
            assert equal == exp_equal
    """

    # A testcase tuple
    testcase_tuple = namedtuple(
        'testcase_tuple',
        ['desc', 'kwargs', 'exp_exc_types', 'exp_warn_types', 'condition']
    )

    def wrapper_func(desc, kwargs, exp_exc_types, exp_warn_types, condition):
        """
        Wrapper function that calls the test function that is decorated.
        """

        if not condition:
            pytest.skip("Condition for test case not met")

        if condition == 'pdb':
            # pylint: disable=import-outside-toplevel
            import pdb

        testcase = testcase_tuple(desc, kwargs, exp_exc_types, exp_warn_types,
                                  condition)

        if exp_warn_types:
            with pytest.warns(exp_warn_types) as rec_warnings:
                if exp_exc_types:
                    with pytest.raises(exp_exc_types):
                        if condition == 'pdb':
                            # pylint: disable=forgotten-debug-statement
                            pdb.set_trace()

                        test_func(testcase, **kwargs)  # expecting an exception

                    ret = None  # Debugging hint
                    # In combination with exceptions, we do not verify warnings
                    # (they could have been issued before or after the
                    # exception).
                else:
                    if condition == 'pdb':
                        # pylint: disable=forgotten-debug-statement
                        pdb.set_trace()

                    test_func(testcase, **kwargs)  # not expecting an exception

                    ret = None  # Debugging hint
                    assert len(rec_warnings) >= 1
        else:
            with warnings.catch_warnings(record=True) as rec_warnings:
                if exp_exc_types:
                    with pytest.raises(exp_exc_types):
                        if condition == 'pdb':
                            # pylint: disable=forgotten-debug-statement
                            pdb.set_trace()

                        test_func(testcase, **kwargs)  # expecting an exception

                    ret = None  # Debugging hint
                else:
                    if condition == 'pdb':
                        # pylint: disable=forgotten-debug-statement
                        pdb.set_trace()

                    test_func(testcase, **kwargs)  # not expecting an exception

                    ret = None  # Debugging hint

                    # Verify that no warnings have occurred
                    if exp_warn_types is None and rec_warnings:
                        lines = []
                        for w in rec_warnings:
                            tup = (w.filename, w.lineno, w.category.__name__,
                                   str(w.message))
                            line = f"{tup[0]}:{tup[1]}: {tup[2]}: {tup[3]}"
                            if line not in lines:
                                lines.append(line)
                        msg = "Unexpected warnings:\n{}".format(
                            '\n'.join(lines))
                        raise AssertionError(msg)
        return ret

    # Needed because the decorator is signature-changin
    wrapper_func.__signature__ = TESTFUNC_SIGNATURE

    return functools.update_wrapper(wrapper_func, test_func)
