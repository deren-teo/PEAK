from peak.naming.api import *
from peak.naming.contexts import AbstractContext
from peak.binding.imports import importString

from types import StringTypes


class importURL(OpaqueURL):

    __implements__ = IAddress
    
    def retrieve(self, refInfo, name, context, environment, attrs=None):
        return importString(self.body)

    def fromURL(klass, name):
        return klass.fromArgs(name.scheme, name.body)

    fromURL = classmethod(fromURL)