"""Object Naming subsystem, analagous to Java's JNDI (javax.naming)

    This package is intended to be a rough equivalent to the 'javax.naming'
    package for implementing JNDI in Java.  The idea is to be a conceptual
    match, rather than a 100% compatible API.  Pythonic naming conventions
    and operating idioms are preferred over their Java equivalents.

    To Do (no particular ordering)


        * AbstractContext needs:

            - __init__ signature add kwargs

            - makeName handling distinctions for URLs vs. ???

            - document need for __iter__ to return keys usable by _get

        * ParsedURL needs to be able to parse bodies alone, and a way to init
          from kwargs instead of a string.  Also need a metaclass to re.compile
          the 'pattern' attrib so subclassers don't need to import re.

        * 'factories' package needs double registry for Reference.type vs.
          RefAddr.type info, and registration methods so that one needn't
          write directly into the alias registries.  A direct lookup mechanism
          (non-alias based) for URL schemes might be a good idea too.

        * create FederationContext, set up to handle '+:' URL scheme, whose
          operations simply do a series of lookup/lookup_nns operations on the
          composite name path in order to implement all the "standard" operations

        * 'MappingContext', 'ConfigContext', 'FSContext', etc.

        * Unit tests!!!!

        * Directory attribute support, and other remaining interface methods

        * Detailed interface and subclassing docs
"""


from interfaces import *
from names      import *
from references import *
from api        import *
import spi

