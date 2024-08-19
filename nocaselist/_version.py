# Copyright (C) 2020 Andreas Maier
"""
Version of the nocaselist package.
"""

try:
    from ._version_scm import version, version_tuple
except ImportError:
    from importlib.metadata import version as get_version
    version = get_version("nocaselist")
    v_list = []
    for item in version.split('.'):
        try:
            v_item = int(item)
        except ValueError:
            v_item = item
            v_list.append(v_item)
    version_tuple = tuple(v_list)

__all__ = ['__version__', '__version_tuple__']

#: The full version of this package including any development levels, as a
#: :term:`string`.
#:
#: Possible formats for this version string are:
#:
#: * "M.N.Pa1.dev7+g1234567": A not yet released version M.N.P
#: * "M.N.P": A released version M.N.P
__version__ = version

#: The full version of this package including any development levels, as a
#: tuple of version items, converted to integer where possible.
#:
#: Possible formats for this version string are:
#:
#: * (M, N, P, 'a1', 'dev7', 'g1234567'): A not yet released version M.N.P
#: * (M, N, P): A released version M.N.P
__version_tuple__ = version_tuple
