"""API functions and classes for the peak.naming package"""

from interfaces import *
from names      import *

import spi


def InitialContext(parent=None, ctxName=None, **options):

    """Get an initial naming context, based on 'parent' and keyword options

    'parent' is the component which will be used as the naming context's
    parent component, to obtain any required configuration data.  The
    'options' keyword arguments are used to set up the context attributes,
    just as with a normal PEAK component constructor.

    This function implements the 'binding.IBindingFactory' interface, and
    thus can be used as a factory for a 'binding.New()' attribute.  That
    is, you can do this::

        myInitCtx = binding.New(naming.InitialContext)

    in a class to create a 'myInitCtx' attribute.  This can be useful if
    you will be using naming functions a lot and would like to hang onto
    an initial context.
    """

    return spi.getInitialContext(parent, ctxName, **options)


from peak.binding.interfaces import IBindingFactory
InitialContext.__implements__ = IBindingFactory

del IBindingFactory






def lookup(name, parent=None, **options):

    """Look up 'name' in the default initial context for 'parent', w/'options'

    This is just a shortcut for calling::
    
        naming.InitialContext(parent,**options)[name]
    """

    return InitialContext(parent, **options)[name]




def parseURL(name, parent=None):

    """Return a parsed URL for 'name', based on schemes available to 'parent'

    If a parser for the URL scheme isn't available, or 'name' is not a
    valid URL, 'exceptions.InvalidName' will be raised.  Note that 'name'
    must include a URL scheme, (e.g. '"ldap:"'), or it will be considered
    invalid.
    """

    url = toName(name)

    if url.nameKind != URL_KIND:
        raise exceptions.InvalidName("Not a URL", name)

    scheme, body = url.scheme, url.body

    ctx = spi.getURLContext(scheme, IResolver, parent)

    if ctx is None:
        from peak.exceptions import InvalidName
        raise InvalidName("Unknown scheme", scheme)

    return ctx.schemeParser(scheme, body)

