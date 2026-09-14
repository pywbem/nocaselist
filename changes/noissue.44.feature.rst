Made the following :class:`nocaselist.NocaseList` methods subclass-safe,
that so far returned a NocaseList object. Now, they return an object of
NocaseList or a subclass, if NocaseList was subclassed:
``__add__()``, ``__mul__()``, ``__rmul__()``, ``__reversed__()``, ``copy()``.
