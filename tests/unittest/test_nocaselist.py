# Copyright (C) 2020 Andreas Maier
"""
Test the NocaseList class.
"""


import sys
import os
import re
import unicodedata
import pickle
import pytest

from ..utils.simplified_test_function import simplified_test_function

# pylint: disable=wrong-import-position, wrong-import-order, invalid-name
from ..utils.import_installed import import_installed
nocaselist = import_installed('nocaselist')
from nocaselist import NocaseList as _NocaseList  # noqa: E402
# pylint: enable=wrong-import-position, wrong-import-order, invalid-name

# pylint: disable=use-dict-literal

# Controls whether the tests are run against a standard dict instead.
TEST_AGAINST_LIST = bool(os.getenv('TEST_AGAINST_LIST'))

if TEST_AGAINST_LIST:
    print("\nInfo: test_nocaselist.py tests run against standard list")

# The list class being tested
# pylint: disable=invalid-name
NocaseList = list if TEST_AGAINST_LIST else _NocaseList

# Flag indicating that standard dict is guaranteed to preserve order
DICT_PRESERVES_ORDER = sys.version_info[0:2] >= (3, 7)


def ensure_unicode(value):
    """
    Return the value as a unicode string.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return value.decode('utf-8')


def assert_equal(list1, list2, verify_order=True):
    """
    Assert that list1 is equal to list2.
    Check consistency of list1.

    list1: Must be a NocaseList or list object.
    list2: Must be a NocaseList or list or iterable object.
    """

    list1_lst = list(list1)  # Uses NocaseList.__iter__()
    list2_lst = list(list2)  # Uses NocaseList.__iter__()

    if verify_order:
        assert list1_lst == list2_lst
    else:
        assert sorted(list1_lst, key=ensure_unicode) == \
            sorted(list2_lst, key=ensure_unicode)

    # Check consistency of list1 between its internal casefolded list and
    # its external list
    if isinstance(list1, _NocaseList):
        list1_cf = list1._casefolded_list  # pylint: disable=protected-access
        assert len(list1_lst) == len(list1_cf)
        for i, value in enumerate(list1):  # Uses NocaseList.__iter__()
            value_cf = list1_cf[i]
            assert list1.__casefold__(value) == value_cf


TESTCASES_NOCASELIST_INIT = [

    # Testcases for NocaseList.__init__() / ncl=NocaseList()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to NocaseList().
    #   * init_kwargs: Dict of keyword arguments to NocaseList().
    #   * exp_list: Expected resulting list.
    #   * verify_order: Flag to verify the expected order.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list from no args",
        dict(
            init_args=(),
            init_kwargs={},
            exp_list=[],
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "Empty list from empty list as positional arg",
        dict(
            init_args=([],),
            init_kwargs={},
            exp_list=[],
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "Empty list from empty tuple as positional arg",
        dict(
            init_args=(tuple(),),
            init_kwargs={},
            exp_list=[],
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "Empty list from empty dict as positional arg",
        dict(
            init_args=({},),
            init_kwargs={},
            exp_list=[],
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "Empty list from empty NocaseList as positional arg",
        dict(
            init_args=(NocaseList(),),
            init_kwargs={},
            exp_list=[],
            verify_order=True,
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List from list as positional arg",
        dict(
            init_args=(['Dog', b'Cat'],),
            init_kwargs={},
            exp_list=['Dog', b'Cat'],
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "List from tuple as positional arg",
        dict(
            init_args=(('Dog', b'Cat'),),
            init_kwargs={},
            exp_list=['Dog', b'Cat'],
            verify_order=True,
        ),
        None, None, True
    ),
    (
        "List from dict as positional arg (uses only the keys)",
        dict(
            init_args=({'Dog': 'Kitten', b'Cat': 'Budgie'},),
            init_kwargs={},
            exp_list=['Dog', b'Cat'],
            verify_order=DICT_PRESERVES_ORDER,
        ),
        None, None, True
    ),
    (
        "List from string as positional arg (string chars become list items)",
        dict(
            init_args=('Dog',),
            init_kwargs={},
            exp_list=['D', 'o', 'g'],
            verify_order=True,
        ),
        None, None, True
    ),

    # Error cases
    (
        "'iterable' keyword arg (no kwargs)",
        dict(
            init_args=(),
            init_kwargs=dict(iterable=[1, 2]),
            exp_list=None,
            verify_order=None,
        ),
        TypeError if TEST_AGAINST_LIST else AttributeError, None, True
        # TODO(issue #25): Make behavior consistent to standard list
    ),
    (
        "None as positional arg (is not iterable)",
        dict(
            init_args=(None,),
            init_kwargs={},
            exp_list=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "Integer type as positional arg",
        dict(
            init_args=(42,),
            init_kwargs={},
            exp_list=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
    (
        "Two positional args",
        dict(
            init_args=([], []),
            init_kwargs={},
            exp_list=None,
            verify_order=None,
        ),
        TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_INIT)
@simplified_test_function
def test_NocaseList_init(testcase, init_args, init_kwargs, exp_list,
                         verify_order):
    """
    Test function for NocaseList.__init__() / ncl=NocaseList()
    """

    # The code to be tested
    act_list = NocaseList(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify that NocaseList inherits from list
    assert isinstance(act_list, list)

    assert_equal(act_list, exp_list, verify_order)  # Uses NocaseList.__iter__()


TESTCASES_NOCASELIST_REPR = [

    # Testcases for NocaseList.__repr__() / repr(ncl)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_REPR)
@simplified_test_function
def test_NocaseList_repr(testcase, nclist):
    """
    Test function for NocaseList.__repr__() / repr(ncl)
    """

    # The code to be tested
    result = repr(nclist)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert re.match(r'^\[.*\]$', result)

    # Note: This only tests for existence of each item, not for excess items
    # or representing the correct order.
    for item in nclist:
        exp_item_result = repr(item)
        assert exp_item_result in result


TESTCASES_NOCASELIST_GETITEM = [

    # Testcases for NocaseList.__getitem__() / val = ncl[idx]

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * index: Index to be used for the test.
    #   * exp_value: Expected value for the index.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with None as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index=None,
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with unicode string as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index='',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with byte string as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index=b'',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with non-existing index 0 (out of range)",
        dict(
            nclist=NocaseList(),
            index=0,
            exp_value=None,
        ),
        IndexError, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with None as index (invalid type)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index=None,
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "List with two items, with string as index (invalid type)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index='',
            exp_value=None,
        ),
        TypeError, None, True
    ),
    (
        "List with two items, with non-existing index 2 (out of range)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index=2,
            exp_value=None,
        ),
        IndexError, None, True
    ),
    (
        "List with two items, with index 0",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index=0,
            exp_value='Dog',
        ),
        None, None, True
    ),
    (
        "List with two items, with index 1",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index=1,
            exp_value=b'Cat',
        ),
        None, None, True
    ),
    (
        "List with two items, with index -1",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index=-1,
            exp_value=b'Cat',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_GETITEM)
@simplified_test_function
def test_NocaseList_getitem(testcase, nclist, index, exp_value):
    """
    Test function for NocaseList.__getitem__() / val = ncl[idx]
    """

    # The code to be tested
    act_value = nclist[index]

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_value == exp_value, f"Unexpected value at index {index}"


TESTCASES_NOCASELIST_SETITEM = [

    # Testcases for NocaseList.__setitem__() / ncl[idx] = value

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * index: Index to be used for the test.
    #   * value: Value to be used for the test.
    #   * exp_nclist: Expected NocaseList object after test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with None as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index=None,
            value=None,
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with unicode string as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index='',
            value=None,
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with byte string as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index=b'',
            value=None,
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with non-existing index 0 (out of range)",
        dict(
            nclist=NocaseList(),
            index=0,
            value='Newbie',
            exp_nclist=None,
        ),
        IndexError, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with None as index (invalid type)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            index=None,
            value='Kitten',
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "List with two items, setting unicode string at index 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=0,
            value='Newbie',
            exp_nclist=NocaseList(['Newbie', 'Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, setting byte string at index 1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=1,
            value=b'Newbie',
            exp_nclist=NocaseList(['Dog', b'Newbie']),
        ),
        None, None, True
    ),
    (
        "List with two items, setting string at index -1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=-1,
            value='Newbie',
            exp_nclist=NocaseList(['Dog', 'Newbie']),
        ),
        None, None, True
    ),
    (
        "List with two items, setting string at index 2 (out of range)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=2,
            value='Newbie',
            exp_nclist=None,
        ),
        IndexError, None, True
    ),
    (
        "Updating string list at slice 0:2",
        dict(
            nclist=NocaseList(['A1', 'B2', 'C3', 'D4']),
            index=slice(0, 2),
            value=['XX', 'YY'],
            exp_nclist=NocaseList(['XX', 'YY', 'C3', 'D4']),
        ),
        None, None, True
    ),
    (
        "Updating string list at slice 0:2:2",
        dict(
            nclist=NocaseList(['A1', 'B2', 'C3', 'D4']),
            index=slice(0, 4, 2),
            value=['XX', 'YY'],
            exp_nclist=NocaseList(['XX', 'B2', 'YY', 'D4']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_SETITEM)
@simplified_test_function
def test_NocaseList_setitem(testcase, nclist, index, value, exp_nclist):
    """
    Test function for NocaseList.__setitem__() / ncl[idx]=value
    """

    # The code to be tested
    nclist[index] = value

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # The verification below also uses some NocaseList features, but that is
    # unavoidable if we want to work through the public interface:

    act_value = nclist[index]  # Uses NocaseList.__getitem__()

    assert act_value == value, f"Unexpected value at index {index}"

    assert_equal(nclist, exp_nclist)  # Uses NocaseList.__iter__()


TESTCASES_NOCASELIST_DELITEM = [

    # Testcases for NocaseList.__delitem__() / del ncl[idx]

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * index: Index to be used for the test.
    #   * exp_nclist: Expected NocaseList object after deletion, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with None as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index=None,
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with string as index (invalid type)",
        dict(
            nclist=NocaseList(),
            index='',
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "Empty list, with non-existing index 0 (out of range)",
        dict(
            nclist=NocaseList(),
            index=0,
            exp_nclist=None,
        ),
        IndexError, None, True
    ),
    (
        "Empty list, with non-existing index -1 (out of range)",
        dict(
            nclist=NocaseList(),
            index=-1,
            exp_nclist=None,
        ),
        IndexError, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with None as index (invalid type)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=None,
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "List with two items, with string as index (invalid type)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index='',
            exp_nclist=None,
        ),
        TypeError, None, True
    ),
    (
        "List with two items, with existing index 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=0,
            exp_nclist=NocaseList(['Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, with existing index -1 (last from end)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=-1,
            exp_nclist=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "List with two items, with non-existing index 2 (out of range)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            index=2,
            exp_nclist=None,
        ),
        IndexError, None, True
    ),
    (
        "Deleting string list at slice 0:2",
        dict(
            nclist=NocaseList(['A1', 'B2', 'C3', 'D4']),
            index=slice(0, 2),
            exp_nclist=NocaseList(['C3', 'D4']),
        ),
        None, None, True
    ),
    (
        "Deleting string list at slice 0:2:2",
        dict(
            nclist=NocaseList(['A1', 'B2', 'C3', 'D4']),
            index=slice(0, 4, 2),
            exp_nclist=NocaseList(['B2', 'D4']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_DELITEM)
@simplified_test_function
def test_NocaseList_delitem(testcase, nclist, index, exp_nclist):
    """
    Test function for NocaseList.__delitem__() / del ncl[idx]
    """

    # The code to be tested
    del nclist[index]

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(nclist, exp_nclist)  # Uses NocaseList.__iter__()


TESTCASES_NOCASELIST_ITER = [

    # Testcases for NocaseList.__iter__() / for item in ncl

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * exp_items: List with expected items in expected order.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
            exp_items=[],
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            exp_items=['Dog', 'Cat'],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_ITER)
@simplified_test_function
def test_NocaseList_iter(testcase, nclist, exp_items):
    """
    Test function for NocaseList.__iter__() / for item in ncl
    """

    # The code to be tested
    act_items = []
    for item in nclist:
        act_items.append(item)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_items == exp_items


TESTCASES_NOCASELIST_CONTAINS = [

    # Testcases for NocaseList.__contains__() / value in ncl

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * value: Value to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with None as value (no casefold method)",
        dict(
            nclist=NocaseList(),
            value=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with integer value 0 (no casefold method)",
        dict(
            nclist=NocaseList(),
            value=0,
            exp_result=False if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Empty list, with non-existing empty unicode string value (not found)",
        dict(
            nclist=NocaseList(),
            value='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with non-existing empty byte string value (not found)",
        dict(
            nclist=NocaseList(),
            value=b'',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with non-existing non-empty unicode string value "
        "(not found)",
        dict(
            nclist=NocaseList(),
            value='Dog',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "Empty list, with non-existing non-empty byte string value "
        "(not found)",
        dict(
            nclist=NocaseList(),
            value=b'Dog',
            exp_result=False,
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with None as value (no casefold method)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value=None,
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with integer value 0 (no casefold method)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value=0,
            exp_result=False if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "List with two items, with non-existing empty unicode string value "
        "(not found)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value='',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-existing empty byte string value "
        "(not found)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value=b'',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-existing non-empty unicode string value "
        "(not found)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value='invalid',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-existing non-empty byte string value "
        "(not found)",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value=b'invalid',
            exp_result=False,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing unicode string value in original "
        "case",
        dict(
            nclist=NocaseList(['Dog', b'Cat']),
            value='Dog',
            exp_result=True,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing byte string value in original "
        "case",
        dict(
            nclist=NocaseList([b'Dog', 'Cat']),
            value=b'Dog',
            exp_result=True,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing unicode string value in "
        "non-original upper case",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='DOG',
            exp_result=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing byte string value in "
        "non-original upper case",
        dict(
            nclist=NocaseList([b'Dog', 'Cat']),
            value=b'DOG',
            exp_result=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing unicode string value in "
        "non-original lower case",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='dog',
            exp_result=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing byte string value in "
        "non-original lower case",
        dict(
            nclist=NocaseList([b'Dog', 'Cat']),
            value=b'dog',
            exp_result=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing unicode string value in "
        "non-original mixed case",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='doG',
            exp_result=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with two items, with existing byte string value in "
        "non-original mixed case",
        dict(
            nclist=NocaseList([b'Dog', 'Cat']),
            value=b'doG',
            exp_result=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_CONTAINS)
@simplified_test_function
def test_NocaseList_contains(testcase, nclist, value, exp_result):
    """
    Test function for NocaseList.__contains__() / value in ncl
    """

    # The code to be tested
    act_result = value in nclist

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result, f"Unexpected result for value {value!r}"


TESTCASES_NOCASELIST_SIZEOF = [

    # Testcases for NocaseList.__sizeof__() / len(ncl)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            exp_result=2,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_SIZEOF)
@simplified_test_function
def test_NocaseList_sizeof(testcase, nclist, exp_result):
    """
    Test function for NocaseList.__sizeof__() / len(ncl)
    """

    # The code to be tested
    result = len(nclist)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_NOCASELIST_ADD = [

    # Testcases for NocaseList.__add__() / ncl + val

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList (LHO) object to be used for the test.
    #   * other: Other iterable (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Add an empty NocaseList and a string (must be list/tuple)",
        dict(
            nclist=NocaseList(),
            other='Dog',
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Add an empty NocaseList and an integer (must be list/tuple)",
        dict(
            nclist=NocaseList(),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Add an empty NocaseList and a tuple (list: must be list, "
        "NocaseList: success)",
        dict(
            nclist=NocaseList(),
            other=('Dog',),
            exp_result=None if TEST_AGAINST_LIST
            else NocaseList(['Dog']),
        ),
        TypeError if TEST_AGAINST_LIST else None, None, True
        # This is an extension of NocaseList over list
    ),
    (
        "Add an empty NocaseList and a list with one string item",
        dict(
            nclist=NocaseList(),
            other=['Dog'],
            exp_result=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "Add an empty NocaseList and a NocaseList with one string item",
        dict(
            nclist=NocaseList(),
            other=NocaseList(['Dog']),
            exp_result=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "Add an empty NocaseList and a list with one integer item "
        "(list: success, NocaseList: no casefold)",
        dict(
            nclist=NocaseList(),
            other=[42],
            exp_result=NocaseList([42]) if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Add a NocaseList with two items and a list with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            other=['Budgie', 'Fish'],
            exp_result=NocaseList(['Dog', 'Cat', 'Budgie', 'Fish']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_ADD)
@simplified_test_function
def test_NocaseList_add(testcase, nclist, other, exp_result):
    """
    Test function for NocaseList.__add__() / ncl + val
    """

    org_nclist = NocaseList(nclist)

    # The code to be tested
    result = nclist + other

    # Verify the input NocaseList object has not changed
    assert_equal(nclist, org_nclist)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


TESTCASES_NOCASELIST_IADD = [

    # Testcases for NocaseList.__iadd__() / ncl += val

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList (LHO) object to be used for the test.
    #   * other: Other iterable (RHO) to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Extend an empty NocaseList by a string (string chars become items)",
        dict(
            nclist=NocaseList(),
            other='Dog',
            exp_result=NocaseList(['D', 'o', 'g']),
        ),
        None, None, True
    ),
    (
        "Extend an empty NocaseList by an integer (no iterable)",
        dict(
            nclist=NocaseList(),
            other=42,
            exp_result=None,
        ),
        TypeError, None, True
    ),
    (
        "Extend an empty NocaseList by a tuple",
        dict(
            nclist=NocaseList(),
            other=('Dog',),
            exp_result=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "Extend an empty NocaseList by a list with one string item",
        dict(
            nclist=NocaseList(),
            other=['Dog'],
            exp_result=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "Extend an empty NocaseList by a NocaseList with one string item",
        dict(
            nclist=NocaseList(),
            other=NocaseList(['Dog']),
            exp_result=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "Extend an empty NocaseList by a list with one integer item "
        "(list: success, NocaseList: no casefold)",
        dict(
            nclist=NocaseList(),
            other=[42],
            exp_result=NocaseList([42]) if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Extend a NocaseList with two items by a list with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            other=['Budgie', 'Fish'],
            exp_result=NocaseList(['Dog', 'Cat', 'Budgie', 'Fish']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_IADD)
@simplified_test_function
def test_NocaseList_iadd(testcase, nclist, other, exp_result):
    """
    Test function for NocaseList.__iadd__() / ncl += val
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)
    nclist_copy_id = id(nclist_copy)

    # The code to be tested
    nclist_copy += other

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the object has been changed in place
    assert id(nclist_copy) == nclist_copy_id

    assert_equal(nclist_copy, exp_result)


TESTCASES_NOCASELIST_MUL = [

    # Testcases for NocaseList.__mul__() / ncl * num
    # Testcases for NocaseList.__rmul__() / num * ncl
    # Testcases for NocaseList.__imul__() / ncl *= num

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * number: Number parameter for the test function.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list times -1",
        dict(
            nclist=NocaseList(),
            number=-1,
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "Empty list times 0",
        dict(
            nclist=NocaseList(),
            number=0,
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "Empty list times 1",
        dict(
            nclist=NocaseList(),
            number=1,
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "Empty list times 2",
        dict(
            nclist=NocaseList(),
            number=2,
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "Empty list times -0.5 (must be integer)",
        dict(
            nclist=NocaseList(),
            number=-0.5,
            exp_result=NocaseList(),
        ),
        TypeError, None, True
    ),
    (
        "Empty list times +0.5 (must be integer)",
        dict(
            nclist=NocaseList(),
            number=+0.5,
            exp_result=NocaseList(),
        ),
        TypeError, None, True
    ),
    (
        "List with two items times -1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            number=-1,
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items times 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            number=0,
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items times 1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            number=1,
            exp_result=NocaseList(['Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items times 2",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            number=2,
            exp_result=NocaseList(['Dog', 'Cat', 'Dog', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_MUL)
@simplified_test_function
def test_NocaseList_mul(testcase, nclist, number, exp_result):
    """
    Test function for NocaseList.__mul__() / ncl * num
    """

    org_nclist = NocaseList(nclist)

    # The code to be tested
    result = nclist * number

    # Verify the input NocaseList object has not changed
    assert_equal(nclist, org_nclist)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_MUL)
@simplified_test_function
def test_NocaseList_rmul(testcase, nclist, number, exp_result):
    """
    Test function for NocaseList.__rmul__() / num * ncl
    """

    org_nclist = NocaseList(nclist)

    # The code to be tested
    result = number * nclist

    # Verify the input NocaseList object has not changed
    assert_equal(nclist, org_nclist)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_MUL)
@simplified_test_function
def test_NocaseList_imul(testcase, nclist, number, exp_result):
    """
    Test function for NocaseList.__imul__() / ncl *= num
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)
    nclist_copy_id = id(nclist_copy)

    # The code to be tested
    nclist_copy *= number

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the object has been changed in place
    assert id(nclist_copy) == nclist_copy_id

    assert_equal(nclist_copy, exp_result)


TESTCASES_NOCASELIST_REVERSE = [

    # Testcases for NocaseList.reverse()
    # Testcases for NocaseList.__reversed__() / reversed(ncl)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * exp_result: Expected result of the test function, or None.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
            exp_result=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            exp_result=NocaseList(['Cat', 'Dog']),
        ),
        None, None, True
    ),
    (
        "List with three items",
        dict(
            nclist=NocaseList(['Dog', 'Cat', 'Kitten']),
            exp_result=NocaseList(['Kitten', 'Cat', 'Dog']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_REVERSE)
@simplified_test_function
def test_NocaseList_reversed(testcase, nclist, exp_result):
    """
    Test function for NocaseList.__reversed__() / reversed(ncl)
    """

    org_nclist = NocaseList(nclist)

    # The code to be tested
    result = reversed(nclist)

    # Verify the input NocaseList object has not changed
    assert_equal(nclist, org_nclist)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(result, exp_result)


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_REVERSE)
@simplified_test_function
def test_NocaseList_reverse(testcase, nclist, exp_result):
    """
    Test function for NocaseList.reverse()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.reverse()

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result is None
    assert_equal(nclist_copy, exp_result)


TESTCASES_NOCASELIST_COMPARE = [

    # Testcases for NocaseList.__eq__(), __ne__()
    # Testcases for NocaseList.__gt__(), __le__()
    # Testcases for NocaseList.__lt__(), __ge__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj1: NocaseList object #1 to use.
    #   * obj2: NocaseList object #2 to use.
    #   * exp_eq: Expected result of __eq__() and !__ne__()
    #   * exp_gt: Expected result of __gt__() and !__le__()
    #   * exp_lt: Expected result of __lt__() and !__ge__()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty lists",
        dict(
            obj1=NocaseList(),
            obj2=NocaseList(),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Empty lists (list)",
        dict(
            obj1=NocaseList(),
            obj2=[],
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Lists with one item, that are excase-sensitively equal",
        dict(
            obj1=NocaseList(['Cat']),
            obj2=NocaseList(['Cat']),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Lists with one item, that are excase-sensitively equal (list)",
        dict(
            obj1=NocaseList(['Cat']),
            obj2=list(['Cat']),
            exp_eq=True,
            exp_gt=False,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "Lists with one item, that are case-insensitively equal",
        dict(
            obj1=NocaseList(['Cat']),
            obj2=NocaseList(['caT']),
            exp_eq=not TEST_AGAINST_LIST,
            exp_gt=False,
            exp_lt=TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "Lists with one item, that are case-insensitively equal (list)",
        dict(
            obj1=NocaseList(['Cat']),
            obj2=list(['caT']),
            exp_eq=not TEST_AGAINST_LIST,
            exp_gt=False,
            exp_lt=TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "Lists with one item, that are case-insensitively lt but "
        "case-sensitively gt",
        dict(
            obj1=NocaseList(['cat']),
            obj2=NocaseList(['Dog']),
            exp_eq=False,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "Lists with one item, that are case-insensitively lt but "
        "case-sensitively gt (list)",
        dict(
            obj1=NocaseList(['cat']),
            obj2=list(['Dog']),
            exp_eq=False,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with one item vs list with two items, first item is "
        "case-insensitively equal",
        dict(
            obj1=NocaseList(['cat']),
            obj2=NocaseList(['Cat', 'Dog']),
            exp_eq=False,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with one item vs list with two items, first item is "
        "case-insensitively equal (list)",
        dict(
            obj1=NocaseList(['cat']),
            obj2=list(['Cat', 'Dog']),
            exp_eq=False,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with one item vs list with two items, first item is not equal",
        dict(
            obj1=NocaseList(['cat']),
            obj2=NocaseList(['Kitten', 'Dog']),
            exp_eq=False,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with one item vs list with two items, first item is not equal "
        "(list)",
        dict(
            obj1=NocaseList(['cat']),
            obj2=list(['Kitten', 'Dog']),
            exp_eq=False,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=not TEST_AGAINST_LIST,
        ),
        None, None, True
    ),
    (
        "List with two items, both case-insensitively equal and in same order",
        dict(
            obj1=NocaseList(['Cat', 'Dog']),
            obj2=NocaseList(['CAT', 'DOG']),
            exp_eq=not TEST_AGAINST_LIST,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "List with two items, both case-insensitively equal and in same order "
        "(list)",
        dict(
            obj1=NocaseList(['Cat', 'Dog']),
            obj2=list(['CAT', 'DOG']),
            exp_eq=not TEST_AGAINST_LIST,
            exp_gt=TEST_AGAINST_LIST,
            exp_lt=False,
        ),
        None, None, True
    ),
    (
        "List with two items, both case-insensitively equal but in different "
        "order",
        dict(
            obj1=NocaseList(['Cat', 'Dog']),
            obj2=NocaseList(['DOG', 'CAT']),
            exp_eq=False,
            exp_gt=False,
            exp_lt=True,
        ),
        None, None, True
    ),
    (
        "List with two items, both case-insensitively equal but in different "
        "order (list)",
        dict(
            obj1=NocaseList(['Cat', 'Dog']),
            obj2=list(['DOG', 'CAT']),
            exp_eq=False,
            exp_gt=False,
            exp_lt=True,
        ),
        None, None, True
    ),
]

TESTCASES_NOCASELIST_EQUAL = [

    # Testcases for NocaseList.__eq__(), __ne__()
    (
        "List compared with integer (valid and False)",
        dict(
            obj1=NocaseList(['Cat', 'Dog']),
            obj2=42,
            exp_eq=False,
            exp_gt=None,  # not used
            exp_lt=None,  # not used
        ),
        None, None, True
    ),
    (
        "Integer compared with list (valid and False)",
        dict(
            obj1=42,
            obj2=NocaseList(['Cat', 'Dog']),
            exp_eq=False,
            exp_gt=None,  # not used
            exp_lt=None,  # not used
        ),
        None, None, True
    ),
]

TESTCASES_NOCASELIST_ORDER = [

    # Testcases for NocaseList.__gt__(), __le__()
    # Testcases for NocaseList.__lt__(), __ge__()
    (
        "List compared with integer (invalid)",
        dict(
            obj1=NocaseList(['Cat', 'Dog']),
            obj2=42,
            exp_eq=None,  # not used
            exp_gt=None,
            exp_lt=None,
        ),
        TypeError, None, True
    ),
    (
        "Integer compared with list (invalid)",
        dict(
            obj1=42,
            obj2=NocaseList(['Cat', 'Dog']),
            exp_eq=None,  # not used
            exp_gt=None,
            exp_lt=None,
        ),
        TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COMPARE + TESTCASES_NOCASELIST_EQUAL)  # type: ignore
@simplified_test_function
def test_NocaseList_eq(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for NocaseList.__eq__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    eq1 = (obj1 == obj2)
    eq2 = (obj2 == obj1)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert eq1 == exp_eq
    assert eq2 == exp_eq


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COMPARE + TESTCASES_NOCASELIST_EQUAL)  # type: ignore
@simplified_test_function
def test_NocaseList_ne(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for NocaseList.__ne__()
    """

    exp_ne = not exp_eq

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    ne1 = (obj1 != obj2)
    ne2 = (obj2 != obj1)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert ne1 == exp_ne
    assert ne2 == exp_ne


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COMPARE + TESTCASES_NOCASELIST_ORDER)  # type: ignore
@simplified_test_function
def test_NocaseList_gt(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for NocaseList.__gt__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    gt = (obj1 > obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert gt == exp_gt


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COMPARE + TESTCASES_NOCASELIST_ORDER)  # type: ignore
@simplified_test_function
def test_NocaseList_lt(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for NocaseList.__lt__()
    """

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    lt = (obj1 < obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert lt == exp_lt


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COMPARE + TESTCASES_NOCASELIST_ORDER)  # type: ignore
@simplified_test_function
def test_NocaseList_ge(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for NocaseList.__ge__()
    """

    exp_ge = not exp_lt

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    ge = (obj1 >= obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert ge == exp_ge


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COMPARE + TESTCASES_NOCASELIST_ORDER)  # type: ignore
@simplified_test_function
def test_NocaseList_le(testcase, obj1, obj2, exp_eq, exp_gt, exp_lt):
    # pylint: disable=unused-argument
    """
    Test function for NocaseList.__le__()
    """

    exp_le = not exp_gt

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    le = (obj1 <= obj2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert le == exp_le


TESTCASES_NOCASELIST_COUNT = [

    # Testcases for NocaseList.count()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * value: Value parameter for the test function.
    #   * exp_result: Expected result of the test function.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with integer value (no casefold)",
        dict(
            nclist=NocaseList(),
            value=1234,
            exp_result=0 if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Empty list, with non-empty string value",
        dict(
            nclist=NocaseList(),
            value='Cat',
            exp_result=0,
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with integer value (no casefold)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value=1234,
            exp_result=0 if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "List with two items, with non-matching empty string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='',
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items, with non-matching string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='Kitten',
            exp_result=0,
        ),
        None, None, True
    ),
    (
        "List with two items, with value matching one list item "
        "(case-insensitively)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='caT',
            exp_result=0 if TEST_AGAINST_LIST else 1,
        ),
        None, None, True
    ),
    (
        "List with four items, with value matching three list items "
        "(case-insensitively)",
        dict(
            nclist=NocaseList(['Cat', 'Dog', 'Cat', 'cat']),
            value='caT',
            exp_result=0 if TEST_AGAINST_LIST else 3,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COUNT)
@simplified_test_function
def test_NocaseList_count(testcase, nclist, value, exp_result):
    """
    Test function for NocaseList.count()
    """

    # The code to be tested
    result = nclist.count(value)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_NOCASELIST_COPY = [

    # Testcases for NocaseList.copy()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_COPY)
@simplified_test_function
def test_NocaseList_copy(testcase, nclist):
    """
    Test function for NocaseList.copy()
    """

    # The code to be tested
    nclist_copy = nclist.copy()

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # Verify the result is a different object
    assert id(nclist_copy) != id(nclist)

    assert_equal(nclist_copy, nclist)  # Uses NocaseList equality


TESTCASES_NOCASELIST_CLEAR = [

    # Testcases for NocaseList.clear()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_CLEAR)
@simplified_test_function
def test_NocaseList_clear(testcase, nclist):
    """
    Test function for NocaseList.clear()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.clear()

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # The verification below also uses some NocaseList features, but that is
    # unavoidable if we want to work through the public interface:

    assert result is None

    # The following line uses NocaseList len
    assert len(nclist_copy) == 0  # pylint: disable=len-as-condition


TESTCASES_NOCASELIST_INDEX = [

    # Testcases for NocaseList.index()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * args: Positional arguments for the test function.
    #   * exp_result: Expected result of the test function.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with integer value (no casefold)",
        dict(
            nclist=NocaseList(),
            args=(1234,),
            exp_result=None,
        ),
        ValueError if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Empty list, with non-existing string value (not in list)",
        dict(
            nclist=NocaseList(),
            args=('Cat',),
            exp_result=None
        ),
        ValueError, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with integer value (no casefold)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(1234,),
            exp_result=None,
        ),
        ValueError if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "List with two items, with non-existing empty string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('',),
            exp_result=NocaseList(['Dog', 'Cat', '']),
        ),
        ValueError, None, True
    ),
    (
        "List with two items, with case-insensitively existing string value "
        "at index 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('doG',),
            exp_result=None if TEST_AGAINST_LIST else 0,
        ),
        ValueError if TEST_AGAINST_LIST else None, None, True
    ),
    (
        "List with two items, with case-insensitively existing string value "
        "at index 1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('cAt',),
            exp_result=None if TEST_AGAINST_LIST else 1,
        ),
        ValueError if TEST_AGAINST_LIST else None, None, True
    ),
    (
        "List with two items, with start at 1 and string value of index 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('doG', 1),
            exp_result=None,
        ),
        ValueError, None, True
    ),
    (
        "List with two items, with start at 1 and string value of index 1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('caT', 1),
            exp_result=None if TEST_AGAINST_LIST else 1,
        ),
        ValueError if TEST_AGAINST_LIST else None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_INDEX)
@simplified_test_function
def test_NocaseList_index(testcase, nclist, args, exp_result):
    """
    Test function for NocaseList.index()
    """

    # The code to be tested
    result = nclist.index(*args)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result


TESTCASES_NOCASELIST_APPEND = [

    # Testcases for NocaseList.append()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * value: Value parameter for the test function.
    #   * exp_nclist: Expected NocaseList after being updated.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with integer value (no casefold)",
        dict(
            nclist=NocaseList(),
            value=1234,
            exp_nclist=NocaseList([1234]) if TEST_AGAINST_LIST
            else NocaseList(),
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Empty list, with non-empty string value",
        dict(
            nclist=NocaseList(),
            value='Cat',
            exp_nclist=NocaseList(['Cat']),
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with integer value (no casefold)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value=1234,
            exp_nclist=NocaseList(['Dog', 'Cat', 1234]) if TEST_AGAINST_LIST
            else NocaseList(['Dog', 'Cat']),
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "List with two items, with empty string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='',
            exp_nclist=NocaseList(['Dog', 'Cat', '']),
        ),
        None, None, True
    ),
    (
        "List with two items, with non-empty string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            value='Newbie',
            exp_nclist=NocaseList(['Dog', 'Cat', 'Newbie']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_APPEND)
@simplified_test_function
def test_NocaseList_append(testcase, nclist, value, exp_nclist):
    """
    Test function for NocaseList.append()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.append(value)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result is None
    assert_equal(nclist_copy, exp_nclist)


TESTCASES_NOCASELIST_EXTEND = [

    # Testcases for NocaseList.extend()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * values: List of values for the test function.
    #   * exp_nclist: Expected NocaseList after being updated.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, with empty tuple",
        dict(
            nclist=NocaseList(),
            values=(),
            exp_nclist=NocaseList(),
        ),
        None, None, True
    ),
    (
        "Empty list, with integer value (no casefold)",
        dict(
            nclist=NocaseList(),
            values=[1234],
            exp_nclist=[1234] if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Empty list, with list containing empty string and non-empty string",
        dict(
            nclist=NocaseList(),
            values=['', 'Cat'],
            exp_nclist=NocaseList(['', 'Cat']),
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, with empty tuple",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            values=(),
            exp_nclist=NocaseList(['Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, with integer value (no casefold)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            values=[1234],
            exp_nclist=['Dog', 'Cat', 1234] if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "List with two items, with empty string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            values=[''],
            exp_nclist=NocaseList(['Dog', 'Cat', '']),
        ),
        None, None, True
    ),
    (
        "List with two items, with non-empty string value",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            values=['Newbie'],
            exp_nclist=NocaseList(['Dog', 'Cat', 'Newbie']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_EXTEND)
@simplified_test_function
def test_NocaseList_extend(testcase, nclist, values, exp_nclist):
    """
    Test function for NocaseList.extend()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.extend(values)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result is None
    assert_equal(nclist_copy, exp_nclist)


TESTCASES_NOCASELIST_INSERT = [

    # Testcases for NocaseList.insert()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * args: Positional arguments for the test function.
    #   * exp_nclist: Expected NocaseList after being updated.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, inserting integer value before index 0 (no casefold)",
        dict(
            nclist=NocaseList(),
            args=(0, 1234),
            exp_nclist=[1234] if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "Empty list, inserting string value before index 0",
        dict(
            nclist=NocaseList(),
            args=(0, 'Newbie'),
            exp_nclist=NocaseList(['Newbie']),
        ),
        None, None, True
    ),
    (
        "Empty list, inserting string value before index 1",
        dict(
            nclist=NocaseList(),
            args=(1, 'Newbie'),
            exp_nclist=NocaseList(['Newbie']),
        ),
        None, None, True
    ),
    (
        "Empty list, inserting string value before index -1",
        dict(
            nclist=NocaseList(),
            args=(-1, 'Newbie'),
            exp_nclist=NocaseList(['Newbie']),
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, inserting integer value before index 0 "
        "(no casefold)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(0, 1234),
            exp_nclist=[1234, 'Dog', 'Cat'] if TEST_AGAINST_LIST else None,
        ),
        None if TEST_AGAINST_LIST else AttributeError, None, True
    ),
    (
        "List with two items, inserting string value before index 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(0, 'Newbie'),
            exp_nclist=NocaseList(['Newbie', 'Dog', 'Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, inserting string value before index 1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(1, 'Newbie'),
            exp_nclist=NocaseList(['Dog', 'Newbie', 'Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, inserting string value before index 2",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(2, 'Newbie'),
            exp_nclist=NocaseList(['Dog', 'Cat', 'Newbie']),
        ),
        None, None, True
    ),
    (
        "List with two items, inserting string value before index 3",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(3, 'Newbie'),
            exp_nclist=NocaseList(['Dog', 'Cat', 'Newbie']),
        ),
        None, None, True
    ),
    (
        "List with two items, inserting string value before index -1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(-1, 'Newbie'),
            exp_nclist=NocaseList(['Dog', 'Newbie', 'Cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_INSERT)
@simplified_test_function
def test_NocaseList_insert(testcase, nclist, args, exp_nclist):
    """
    Test function for NocaseList.insert()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.insert(*args)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result is None
    assert_equal(nclist_copy, exp_nclist)


TESTCASES_NOCASELIST_POP = [

    # Testcases for NocaseList.pop()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * args: Positional arguments for the test function.
    #   * exp_result: Expected result from the test function.
    #   * exp_nclist: Expected NocaseList after being updated.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, pop index 0 (does not exist)",
        dict(
            nclist=NocaseList(),
            args=(0,),
            exp_result=None,
            exp_nclist=None,
        ),
        IndexError, None, True
    ),
    (
        "Empty list, pop default index -1 (does not exist)",
        dict(
            nclist=NocaseList(),
            args=(),
            exp_result=None,
            exp_nclist=None,
        ),
        IndexError, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, pop index 0",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(0,),
            exp_result='Dog',
            exp_nclist=NocaseList(['Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, pop index 1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(1,),
            exp_result='Cat',
            exp_nclist=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "List with two items, pop index -1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(-1,),
            exp_result='Cat',
            exp_nclist=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "List with two items, pop default index -1",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=(),
            exp_result='Cat',
            exp_nclist=NocaseList(['Dog']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_POP)
@simplified_test_function
def test_NocaseList_pop(testcase, nclist, args, exp_result, exp_nclist):
    """
    Test function for NocaseList.pop()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    result = nclist_copy.pop(*args)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result == exp_result
    assert_equal(nclist_copy, exp_nclist)


TESTCASES_NOCASELIST_REMOVE = [

    # Testcases for NocaseList.remove()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * args: Positional arguments for the test function.
    #   * exp_nclist: Expected NocaseList after being updated.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, remove some value (does not exist)",
        dict(
            nclist=NocaseList(),
            args=('Cat',),
            exp_nclist=None,
        ),
        ValueError, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, remove first",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('Dog',),
            exp_nclist=NocaseList(['Cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, remove second",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('Cat',),
            exp_nclist=NocaseList(['Dog']),
        ),
        None, None, True
    ),
    (
        "List with two items, remove non-existing (not found)",
        dict(
            nclist=NocaseList(['Dog', 'Cat']),
            args=('Kitten',),
            exp_nclist=None,
        ),
        ValueError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_REMOVE)
@simplified_test_function
def test_NocaseList_remove(testcase, nclist, args, exp_nclist):
    """
    Test function for NocaseList.remove()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.remove(*args)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result is None
    assert_equal(nclist_copy, exp_nclist)


TESTCASES_NOCASELIST_SORT = [

    # Testcases for NocaseList.sort()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    #   * kwargs: Keyword arguments for the test function.
    #   * exp_nclist: Expected NocaseList after being updated.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Empty NocaseList
    (
        "Empty list, default sort",
        dict(
            nclist=NocaseList(),
            kwargs={},
            exp_nclist=NocaseList(),
        ),
        None, None, True
    ),

    # Non-empty NocaseList
    (
        "List with two items, case-insensitively unsorted, default sort key",
        dict(
            nclist=NocaseList(['Dog', 'cat']),
            kwargs={},
            exp_nclist=['Dog', 'cat'] if TEST_AGAINST_LIST
            else NocaseList(['cat', 'Dog']),
        ),
        None, None, True
    ),
    (
        "List with two items, case-insensitively unsorted, default sort key, "
        "descending",
        dict(
            nclist=NocaseList(['cat', 'Dog']),
            kwargs=dict(
                reverse=True,
            ),
            exp_nclist=['cat', 'Dog'] if TEST_AGAINST_LIST
            else NocaseList(['Dog', 'cat']),
        ),
        None, None, True
    ),
    (
        "List with two items, case-insensitively unsorted, with sort key",
        dict(
            nclist=NocaseList(['BUdgie', 'cat']),
            kwargs=dict(
                key=lambda x: x[1],  # sort by second character
            ),
            exp_nclist=['BUdgie', 'cat'] if TEST_AGAINST_LIST
            else NocaseList(['cat', 'BUdgie']),
        ),
        None, None, True
    ),
    (
        "List with two items, case-insensitively unsorted, with sort key, "
        "descending",
        dict(
            nclist=NocaseList(['cat', 'BUdgie']),
            kwargs=dict(
                key=lambda x: x[1],  # sort by second character
                reverse=True,
            ),
            exp_nclist=['cat', 'BUdgie'] if TEST_AGAINST_LIST
            else NocaseList(['BUdgie', 'cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_SORT)
@simplified_test_function
def test_NocaseList_sort(testcase, nclist, kwargs, exp_nclist):
    """
    Test function for NocaseList.sort()
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # The code to be tested
    # pylint: disable=assignment-from-no-return
    result = nclist_copy.sort(**kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert result is None
    assert_equal(nclist_copy, exp_nclist)


TESTCASES_NOCASELIST_PICKLE = [

    # Testcases for pickling and unpickling NocaseList objects

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nclist: NocaseList object to be used for the test.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list",
        dict(
            nclist=NocaseList(),
        ),
        None, None, True
    ),
    (
        "List with two items",
        dict(
            nclist=NocaseList(['Dog', 'cat']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_NOCASELIST_PICKLE)
@simplified_test_function
def test_NocaseList_pickle(testcase, nclist):
    """
    Test function for pickling and unpickling NocaseList objects
    """

    # Don't change the testcase data, but a copy
    nclist_copy = NocaseList(nclist)

    # Pickle the object
    pkl = pickle.dumps(nclist_copy)

    del nclist_copy

    # Unpickle the object
    nclist2 = pickle.loads(pkl)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert_equal(nclist2, nclist)


def test_casefold_override():
    """
    Test function for overriding the casefold method.
    """

    if TEST_AGAINST_LIST:
        pytest.skip("The override test does not support testing with list")

    class MyNocaseList(NocaseList):
        "Test class that overrides the casefold method"

        @staticmethod
        def __casefold__(value):
            return unicodedata.normalize('NFKD', value).casefold()

    nclist = MyNocaseList()

    # Add item with combined Unicode character
    nclist.append("\u00C7")

    # Look up item with combination sequence
    assert "c\u0327" in nclist
