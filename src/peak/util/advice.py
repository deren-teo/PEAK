from new import instancemethod
from types import ClassType, FunctionType
import sys

__all__ = [
    'advice', 'addClassAdvisor', 'isClassAdvisor',
]


































class advice(object):

    """advice(func) -- "around advice" wrapper base class

        This wrapper is a base class for "around" advice on a method.  Just
        redefine the '__call__' method to have the desired semantics.  E.g.::

            class loggedMethod(advice):

                __slots__ = ()

                def __call__(self,*__args,**__kw):
                    print "Entering", self._func, __args, __kw
                    self._func(*__args,**__kw)
                    print "Leaving",self._func

            class someObject(object):

                def aMethod(self,foobly):
                    print foobly

                aMethod = loggedMethod(aMethod)

        If your advice needs parameters, you'll probably want to override
        '__init__()' as well, and add some slots as appropriate.  Note that
        the 'self' parameter to '__call__' is the *advice object*, not the
        'self' that will be passed through to the underlying function (which
        is the first item in '__args'.

        The 'advice' class tries to transparently emulate a normal Python
        method, and to be indistinguishable from such a method to inspectors
        like 'help()' and ZPublisher's 'mapply()'.  Because of this, if
        callers of a method need to know that it is being "advised", you
        should document this in your method's docstring.  There isn't any
        other way someone can tell, apart from reading your source or checking
        the 'type()' or '__class__' of the retrieved method's 'im_func'.

        Advice objects can be transparently stacked, so you can do things like
        'aMethod = loggedMethod( lockedMethod(aMethod) )' safely."""


    __slots__ = '_func'


    def __init__(self, func):
        self._func = func


    def __get__(self,ob,typ):
        if typ is None: typ = ob.__class__
        return instancemethod(self, ob, typ)


    def __call__(self,*__args,**__kw):
        self._func(*__args,**__kw)


    def __repr__(self):
        return `self._func`


    # Pass through any attribute requests to the wrapped object;
    # this will make us "smell right" to ZPublisher's 'mapply()' function.

    def __getattr__(self, attr):
        return getattr(self._func,attr)


    # __doc__ is a special case; our class wants to supply it, and so won't
    # let __getattr__ near it.
    
    __doc__ = property(lambda s: s._func.__doc__)
    









def addClassAdvisor(callback, depth=2):

    """Set up 'callback' to be passed the containing class upon creation

    This function is designed to be called by an "advising" function executed
    in a class suite.  The "advising" function supplies a callback that it
    wishes to have executed when the containing class is created.  The
    callback will be given one argument: the newly created containing class.
    The return value of the callback will be used in place of the class, so
    the callback should return the input if it does not wish to replace the
    class.

    The optional 'depth' argument to this function determines the number of
    frames between this function and the targeted class suite.  'depth'
    defaults to 2, since this skips this function's frame and one calling
    function frame.  If you use this function from a function called directly
    in the class suite, the default will be correct, otherwise you will need
    to determine the correct depth yourself.

    This function works by installing a special class factory function in
    place of the '__metaclass__' of the containing class.  Therefore, only
    callbacks *after* the last '__metaclass__' assignment in the containing
    class will be executed.  Be sure that classes using "advising" functions
    declare any '__metaclass__' *first*, to ensure all callbacks are run."""

    frame = sys._getframe(depth)
    caller_locals = frame.f_locals
    caller_globals = frame.f_globals  

    if (caller_locals is caller_globals
        or '__module__' not in caller_locals
        or '__name__' not in caller_globals
        or caller_locals['__module__']<>caller_globals['__name__']):
            raise SyntaxError(
                "Advice must be in the body of a class statement"
            )

    previousMetaclass = caller_locals.get('__metaclass__')    
    defaultMetaclass  = caller_globals.get('__metaclass__', ClassType)


    def advise(name,bases,cdict):

        if previousMetaclass is None:
             if bases:
                 # find best metaclass or use global __metaclass__ if no bases
                 meta = determineMetaclass(bases)
             else:
                 meta = defaultMetaclass

        elif isClassAdvisor(previousMetaclass):
            # special case: we can't compute the "true" metaclass here,
            # so we need to invoke the previous metaclass and let it
            # figure it out for us (and apply its own advice in the process)
            meta = previousMetaclass

        else:
            meta = determineMetaclass(bases, previousMetaclass)

        newClass = meta(name,bases,cdict)

        # this lets the callback replace the class completely, if it wants to
        return callback(newClass)

    # introspection data only, not used by inner function
    advise.previousMetaclass = previousMetaclass
    advise.callback = callback

    # install the advisor
    caller_locals['__metaclass__'] = advise


def isClassAdvisor(ob):
    """True if 'ob' is a class advisor function"""
    return isinstance(ob,FunctionType) and hasattr(ob,'previousMetaclass')
    






def determineMetaclass(bases, explicit_mc=None):

    """Determine metaclass from 1+ bases and optional explicit __metaclass__"""

    meta = [getattr(b,'__class__',type(b)) for b in bases]

    if tuple(meta)==bases:
        # This would happen if mixing 'type' and 'ExtensionClass'
        # (for example)
        raise TypeError("Incompatible root metatypes", bases)

    if explicit_mc is not None:
        # The explicit metaclass needs to be verified for compatibility
        # as well, and allowed to resolve the incompatible bases, if any
        meta.append(explicit_mc)

    if len(meta)==1:
        # easy case
        return meta[0]
       

    candidates = []

    for b in meta:
        if b is ClassType: continue
        candidates = [bc for bc in candidates if not issubclass(b,bc)]
        candidates.append(b)

    if not candidates:
        # they're all "classic" classes
        return ClassType
        
    elif len(candidates)>1:
        # We could auto-combine, but for now we won't...
        raise TypeError("Incompatible metatypes",bases)

    # Just one, return it
    return candidates[0]

