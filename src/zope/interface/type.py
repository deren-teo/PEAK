##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Adapter-style interface registry

See Adapter class.

$Id: type.py,v 1.1 2003/01/31 16:22:01 pje Exp $
"""
__metaclass__ = type # All classes are new style when run with Python 2.2+

from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.interface._flatten import _flatten
from zope.interface.interfaces import ITypeRegistry

class TypeRegistry:

    __implements__ = ITypeRegistry

    # XXX This comment doesn't seem to be correct, because the mapping is
    # from interface -> object.  There are no tuples that I see.  Also,
    # I'm not sure what the last sentence is trying to say :-).

    # The implementation uses a mapping:
    #
    #  { (required_interface, provided_interface) ->
    #                             (registered_provides, component) }
    #
    # Where the registered provides is what was registered and
    # provided may be some base interface

    def __init__(self, data=None):
        if data is None:
            data = {}

        self._reg = data

    def register(self, interface, object):
        if interface is None or IInterface.isImplementedBy(interface):
            self._reg[interface] = object
        else:
            raise TypeError(
                "The interface argument must be an interface (or None)")

    def unregister(self, interface):
        if interface is None or IInterface.isImplementedBy(interface):
            if interface in self._reg:
                del self._reg[interface]
        else:
            raise TypeError(
                "The interface argument must be an interface (or None)")

    def get(self, interface, default=None):
        """
        Finds a registered component that provides the given interface.
        Returns None if not found.
        """
        return self._reg.get(interface, default)

    def setdefault(self, interface, default=None):
        return self._reg.setdefault(interface, default)

    def getAll(self, interface_spec):
        result = []
        for interface in _flatten(interface_spec):
            object = self._reg.get(interface)
            if object is not None:
                result.append(object)

        if interface_spec is not None:
            object = self._reg.get(None)
            if object is not None:
                result.append(object)

        return result

    def getAllForObject(self, object):
        # XXX This isn't quite right, since it doesn't take into
        # account implementation registries for objects that can't
        # have '__implements__' attributes.
        return self.getAll(getattr(object, '__implements__', None))

    def getTypesMatching(self, interface):
        if interface is None:
            return self._reg.keys()

        result = []
        for k in self._reg:
            if k is None or k.extends(interface, strict=False):
                result.append(k)
        return result

    def __len__(self):
        return len(self._reg)
