"""Interfaces for TW.Naming package"""

import Interface


__all__ = [

    'IName', 'ISyntax', 'IOpaqueURL',

    'IResolver', 'IBasicContext', 'IReadContext', 'IWriteContext',

    'NamingException', 'InvalidNameException', 'NameNotFoundException',
    'CannotProceedException', 'NotContextException',

]


























class NamingException(Exception):

    """Base class for all TW.Naming exceptions

        Supports the following constructor keyword arguments, which then
        become attributes of the exception object:

            rootException -- Exception that caused this exception to be thrown.
        
            rootTraceback -- Traceback of the root exception.
        
            resolvedName -- The portion of the name that was successfully
                resolved.

            resolvedObj -- The object through which resolution was successful,
                i.e., the object to which 'resolvedName' is bound.
            
            remainingName -- The remaining portion of the name which could not
                be resolved.

        The constructor also accepts an arbitrary number of unnamed arguments,
        which are treated the way arguments to the standard Exception class
        are treated.  (That is, saved in the 'args' attribute and used in the
        '__str__' method for formatting.)
    """

    formattables = ('resolvedName', 'remainingName', 'rootException',)
    otherattrs   = ('resolvedObj', 'rootTraceback', 'args', )

    __slots__ = list( formattables + otherattrs )


    def __init__(self, *args, **kw):

        for k in self.extras:
            setattr(self,k,kw.get(k))

        self.args = args



    def __str__(self):

        """Format the exception"""

        txt = super(NamingException,self).__str__(self)
        
        extras = [
            '%s=%s' % (k,getattr(self,k))
            for k in self.formattables if getattr(self,k) is not None
        ]

        if extras:
            return "%s [%s]" % (txt, ','.join(extras))
            
        return txt


class InvalidNameException(NamingException):
    """Unparseable string or non-name object"""
   

class NameNotFoundException(NamingException, LookupError):
    """A name could not be found"""

class NotContextException(NamingException):
    """Continuation is not a context/does not support required interface"""















class CannotProceedException(NamingException):

    """Thrown when a name can't be processed any further

        Supports all 'NamingException' attributes/arguments, plus:

            environment -- The environment that was in effect for the context
                which resolved 'resolvedName'
                
            remainingNewName -- For 'rename' operations; holds the unresolved
                portion of the "new" (i.e. to-be-named) name

            altName -- Name of the resolved object relative to 'altNameCtx'.
                Passed to object factory to resolve NNS references.
            
            altNameCtx -- Context to which 'altName' is relative.
                Passed to object factory to resolve NNS references.

    """

    formattables = NamingException.formattables + (
        'altName', 'remainingNewName',
    )
    
    otherattrs   = NamingException.otherattrs + (
        'altNameCtx', 'environment', 'opInterface'
    )

    __slots__ = list( formattables + otherattrs )












class ISyntax(Interface.Base):
    """Syntax object"""

class IName(Interface.Base):
    """Abstract name object"""

class IOpaqueURL(IName):
    """Opaque URL (scheme+body only)"""


class IResolver(Interface.Base):

    """Bare minimum context support"""

    def resolveToInterface(compositeName, opInterface, newName=None):
        """Resolve compositeName to find a context supporting opInterface"""

























class IBasicContext(Interface.Base):

    """Basic naming context; supports only configuration and name handling"""
    
    def lookup(name, requiredInterface=None):
        """Lookup 'name' --> object that supports 'requiredInterface'"""
        
    def parseName(name):
        """Parse 'name' string and return a name object"""
        
    def getEnvironment():
        """Return a mapping representing the context's configuration"""

    def addToEnvironment(key, value):
        """Add or alter a configuration entry in the context's environment"""

    def removeFromEnvironment(key):
        """Remove a configuration entry from the context's environment"""

    def close():
        """Close the context"""


    # lookupLink, composeName, getNameParser, getNameInNamespace


class IReadContext(IBasicContext):

    """Context that supports iteration/inspection of contents"""

    # list, listBindings,


class IWriteContext(IBasicContext):

    """Context that supports adding/changing its contents"""

    # bind, rebind, unbind, rename,
    # createSubcontext, destroySubcontext, 
