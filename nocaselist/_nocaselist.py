"""
The only class exposed by this package is :class:`nocaselist.NocaseList`.
"""

from __future__ import print_function, absolute_import

__all__ = ['NocaseList']


def _lc_list(lst):
    """
    Return a lower-cased list from the input list.
    """
    result = list()
    for value in lst:
        result.append(value.lower())
    return result


class NocaseList(list):
    # pylint: disable=line-too-long
    """
    A case-insensitive, case-preserving, list.

    The list is case-insensitive: Whenever items of the list are looked up by
    value or item values are compared, that is done case-insensitively. The
    case-insensitivity is defined by performing the lookup or comparison on
    the result of the ``lower()`` method on list items. Therefore, list items
    must support the ``lower()`` method. If a list item does not do that,
    :exc:`py:AttributeError` is raised.

    The list is case-preserving: Whenever the value of list items is returned,
    they have the lexical case that was originally specified when adding
    or updating the item.

    Except for the case-insensitivity of its items, it behaves like, and is
    in fact derived from, the built-in :class:`py:list` class in order to
    facilitate type checks.

    The implementation maintains a second list with the lower-cased items of
    the inherited list, and ensures that both lists are in sync.

    The ``NocaseList`` class supports all behaviors of the built-in
    :class:`py:list` class, so its documentation applies completely:

    * `built-in list class documentation <https://docs.python.org/3/library/stdtypes.html#list>`_

    The following documentation is provided only for explicit documentation of
    the case-insensitive behavior, and to indicate which methods have been
    implemented for maintaining the second lower-cased list.
    """  # noqa E401
    # pylint: enable=line-too-long

    def __init__(self, iterable=()):
        """
        Initialize the list with the items in the specified iterable.
        """
        super(NocaseList, self).__init__(iterable)

        # A list with the same items as the original list, except they are in
        # lower case.
        self._lc_list = _lc_list(self)

    # __repr__(): The inherited method is used.

    # __getattribute__(): The inherited method is used.

    # __getitem__(): The inherited method is used.

    def __setitem__(self, index, value):
        """
        Update the value of the item at an existing index in the list.

        Invoked using ``ncl[index] = value``.
        """
        super(NocaseList, self).__setitem__(index, value)
        self._lc_list[index] = value.lower()

    def __delitem__(self, index):
        """
        Delete an item at an existing index from the list.

        Invoked using ``del ncl[index]``.
        """
        super(NocaseList, self).__delitem__(index)
        del self._lc_list[index]

    # __iter__(): The inherited method is used.

    def __contains__(self, value):
        """
        Return a boolean indicating whether the list contains at least one
        item with the value, by looking it up case-insensitively.

        Invoked using ``value in ncl``.
        """
        return value.lower() in self._lc_list

    # __sizeof__(): The inherited method is used.

    def __add__(self, value):
        """
        Return a shallow copy of the list, that has a new item with the value
        appended at the end. The original list is not changed.

        Invoked using ``ncl + value``.
        """
        lst = self.copy()
        lst.append(value)
        return lst

    def __iadd__(self, value):
        """
        Append a new item with the specified value to the list.

        Invoked using ``ncl += value``.
        """
        # Note: It is unusual that the method has to return self, but it was
        # verified that this is necessary.
        self.append(value)
        return self

    def __mul__(self, number):
        """
        Return a shallow copy of the list, that has the items from the original
        list as many times as specified by number (including 0). The original
        list is not changed.

        Invoked using ``ncl * number``.
        """
        lst = NocaseList()
        for _ in range(0, number):
            lst.extend(self)
        return lst

    def __rmul__(self, number):
        """
        Return a shallow copy of the list, that has the items from the original
        list as many times as specified by number (including 0). The original
        list is not changed.

        Invoked using ``number * ncl``.
        """
        lst = self * number  # Delegates to __mul__()
        return lst

    def __imul__(self, number):
        """
        Replace the original list by a list that has the items from the original
        list as many times as specified by number (including 0).

        Invoked using ``ncl *= number``.
        """
        # Note: It is unusual that the method has to return self, but it was
        # verified that this is necessary.
        lst = self * number  # Delegates to __mul__()
        return lst

    def __reversed__(self):
        """
        Return a shallow copy of the list that has its items reversed in order.

        Invoked using ``reversed(ncl)``.
        """
        lst = self.copy()
        lst.reverse()
        return lst

    def __eq__(self, other):
        """
        Return a boolean indicating whether the list and the other list are
        equal, by comparing corresponding list items case-insensitively.

        The other list may be a :class:`NocaseList` object or any other
        iterable. In all cases, the comparison takes place case-insensitively.

        Invoked using e.g. ``ncl == other``.
        """
        if isinstance(other, NocaseList):
            other = other._lc_list  # pylint: disable=protected-access
        else:
            other = _lc_list(other)
        return self._lc_list == other

    def __ne__(self, other):
        """
        Return a boolean indicating whether the list and the other list are
        not equal, by comparing corresponding list items case-insensitively.

        The other list may be a :class:`NocaseList` object or any other
        iterable. In all cases, the comparison takes place case-insensitively.

        Invoked using e.g. ``ncl != other``.
        """
        if isinstance(other, NocaseList):
            other = other._lc_list  # pylint: disable=protected-access
        else:
            other = _lc_list(other)
        return self._lc_list != other

    def __gt__(self, other):
        """
        Return a boolean indicating whether the list is greater than the other
        list, by comparing corresponding list items case-insensitively.

        The other list may be a :class:`NocaseList` object or any other
        iterable. In all cases, the comparison takes place case-insensitively.

        Invoked using e.g. ``ncl > other``.
        """
        if isinstance(other, NocaseList):
            other = other._lc_list  # pylint: disable=protected-access
        else:
            other = _lc_list(other)
        return self._lc_list > other

    def __lt__(self, other):
        """
        Return a boolean indicating whether the list is less than the other
        list, by comparing corresponding list items case-insensitively.

        The other list may be a :class:`NocaseList` object or any other
        iterable. In all cases, the comparison takes place case-insensitively.

        Invoked using e.g. ``ncl < other``.
        """
        if isinstance(other, NocaseList):
            other = other._lc_list  # pylint: disable=protected-access
        else:
            other = _lc_list(other)
        return self._lc_list < other

    def __ge__(self, other):
        """
        Return a boolean indicating whether the list is greater than or
        equal to the other list, by comparing corresponding list items
        case-insensitively.

        The other list may be a :class:`NocaseList` object or any other
        iterable. In all cases, the comparison takes place case-insensitively.

        Invoked using e.g. ``ncl >= other``.
        """
        if isinstance(other, NocaseList):
            other = other._lc_list  # pylint: disable=protected-access
        else:
            other = _lc_list(other)
        return self._lc_list >= other

    def __le__(self, other):
        """
        Return a boolean indicating whether the list is less than or
        equal to the other list, by comparing corresponding list items
        case-insensitively.

        The other list may be a :class:`NocaseList` object or any other
        iterable. In all cases, the comparison takes place case-insensitively.

        Invoked using e.g. ``ncl <= other``.
        """
        if isinstance(other, NocaseList):
            other = other._lc_list  # pylint: disable=protected-access
        else:
            other = _lc_list(other)
        return self._lc_list <= other

    def count(self, value):
        """
        Return the number of times the specified value occurs in the list,
        comparing the value and the list items case-insensitively.
        """
        return self._lc_list.count(value.lower())

    def copy(self):
        """
        Return a shallow copy of the list.
        """
        return NocaseList(self)

    def clear(self):
        """
        Remove all items from the list (and return None).

        Note: This method was introduced in Python 3.
        """
        super(NocaseList, self).clear()
        self._lc_list.clear()

    def index(self, value, start=0, stop=9223372036854775807):
        """
        Return the index of the first item that is equal to the specified
        value, comparing the value and the list items case-insensitively.

        The search is limited to the index range defined by the specified
        ``start`` and ``stop`` parameters, whereby ``stop`` is the index
        of the first item after the search range.

        Raises:
          ValueError: No such item is found.
        """
        return self._lc_list.index(value.lower(), start, stop)

    def append(self, value):
        """
        Append the specified value as a new item to the end of the list
        (and return None).
        """
        super(NocaseList, self).append(value)
        self._lc_list.append(value.lower())

    def extend(self, iterable):
        """
        Extend the list by the items in the specified iterable
        (and return None).
        """
        super(NocaseList, self).extend(iterable)
        for value in iterable:
            self._lc_list.append(value.lower())

    def insert(self, index, value):
        """
        Insert a new item with specified value before the item at the specified
        index (and return None).
        """
        super(NocaseList, self).insert(index, value)
        self._lc_list.insert(index, value.lower())

    def pop(self, index=-1):
        """
        Return the value of the item at the specified index and also remove it
        from the list.
        """
        self._lc_list.pop(index)
        return super(NocaseList, self).pop(index)

    def remove(self, value):
        """
        Remove the first item from the list whose value is equal to the
        specified value (and return None), comparing the value and the list
        items case-insensitively.
        """
        self._lc_list.remove(value.lower())
        super(NocaseList, self).remove(value)

    def reverse(self):
        """
        Reverse the items in the list in place (and return None).
        """
        super(NocaseList, self).reverse()
        self._lc_list = _lc_list(self)

    def sort(self, key=None, reverse=False):
        """
        Sort the items in the list in place (and return None).

        The sort is stable, in that the order of two (case-insensitively) equal
        elements is maintained.

        By default, the list is sorted in ascending order of its (lower-cased)
        item values. If a key function is given, it is applied once to each
        (lower-cased) list item and the list is sorted in ascending or
        descending order of their key function values.

        The ``reverse`` flag can be set to sort in descending order.
        """

        def lower_key(value):
            """Key function used for sorting"""
            if key:
                return key(value.lower())
            return value.lower()

        super(NocaseList, self).sort(key=lower_key, reverse=reverse)
        self._lc_list = _lc_list(self)
