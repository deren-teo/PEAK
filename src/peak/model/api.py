"""Basic, in-memory implementation of the Service-Element-Feature pattern"""

from TW.API import *
from TW.SEF.Interfaces import *
from TW.SEF.Interfaces import __all__ as allInterfaces

from types import FunctionType



__all__ = [
    'Base','App','Service','Specialist','DynamicBinding','StaticBinding',
    'StructuralFeature', 'Field', 'Collection', 'Reference', 'Sequence',
    'Classifier','PrimitiveType','Enumeration','DataType','Element',
    'bindTo', 'requireBinding', 'bindToNames', 'bindToParent', 'Specialist'
]


# We export the interfaces too, so people don't have to dig for them...

__all__ += allInterfaces



class DynamicBindingMC(Meta.AssertInterfaces):

    def __get__(self, obj, typ=None):
        if obj is None: return self        
        newOb = self()
        newOb._setSEFparent(obj)
        obj.__dict__[newOb._componentName] = newOb
        return newOb


class DynamicBinding(object):

    __metaclass__ = DynamicBindingMC




class bindTo(Once):

    """Automatically look up and cache a relevant service

        Usage::

            class someClass(SEF.Service):

                thingINeed = SEF.bindTo("path.to.service")

        'someClass' can then refer to 'self.thingINeed' instead of
        calling 'self.getService("path.to.service")' repeatedly.
    """

    singleValue = 1

    def __init__(self,targetName):
        self.targetNames = (targetName,)

    def computeValue(self, obj, instanceDict, attrName):

        instanceDict[attrName] = None   # recursion guard

        parent = obj.getSEFparent()
        if parent is None: parent = obj

        obs = map(parent.getService, self.targetNames)

        for newOb in obs:
            if newOb is None:
                del instanceDict[attrName]
                raise NameError(
                    "%s not found binding %s" % (self.targetName, attrName)
                )
            elif self.singleValue:
                return newOb

        return tuple(obs)



class bindToNames(bindTo):

    """Automatically look up and cache a sequence of services by name

        Usage::

            class someClass(SEF.Service):

                thingINeed = SEF.bindToNames(
                    "path.to.service1", "another.path", ...
                )

        'someClass' can then refer to 'self.thingINeed' to get a tuple of
        services instead of calling 'self.getService()' on a series of names.
    """

    singleValue = 0

    def __init__(self,*targetNames):
        self.targetNames = targetNames





















class bindToParent(Once):

    """Look up and cache a reference to the nth-level parent service

        Usage::

            class someClass(SEF.Service):

                grandPa = SEF.bindToParent(2)

       'someClass' can then refer to 'self.grandPa' instead of calling
       'self.getSEFparent().getSEFparent()'.

       Note that this binding creates a circular reference as soon as it
       is retrieved from an instance.  The circular reference can be
       broken by deleting the attribute (e.g. 'del self.grandPa'), but of
       course it will come back the next time you use the attribute.
    """

    def __init__(self,level=1):
        self.level = level

    def computeValue(self, obj, instDict, attrName):

        for step in range(self.level):
            newObj = obj.getSEFparent()
            if newObj is None: break
            obj = newObj

        return obj











class requireBinding(Once):

    """Placeholder for a binding that should be (re)defined by a subclass"""

    def __init__(self,description=""):
        self.description = description
    
    def computeValue(self, obj, instanceDict, attrName):
    
        raise NameError("Class %s must define %s; %s"
            % (obj.__class__.__name__, attrName, self.description)
        )





























class Base(object):

    """Base for all S-E-F classes"""

    __metaclasses__  = (
        Meta.AssertInterfaces, Meta.ClassInit, Meta.ActiveDescriptors
    )
    
    __implements__ = ISEF
    _sefParent     = None

    def getService(self,name=None):

        if name:
            if not isinstance(name,tuple):
                name = tuple(name.split('.'))
                
            if hasattr(self,name[0]):
                o = getattr(self,name[0])
                if len(name)==1:
                    return o
                else:
                    return o.getService(name[1:])
            else:    
                parent = self.getSEFparent()
                if parent is not None:
                    return parent.getService(name)
        else:                
            return self.getSEFparent()


    def _setSEFparent(self,parent):
        from weakref import ref
        self.getSEFparent = ref(parent)

    def getSEFparent(self): return None

    def _componentName(self): return self.__class__.__name__

    _componentName = property(_componentName)

class Service(DynamicBinding, Base):

    """Instance (as opposed to class)"""

    __implements__ = IService
    

class App(Service):

    """Application class"""

    def newElement(self,elementType,*args,**kw):
        element = apply(getattr(self,elementType),args,kw)  # XXX won't do dotted names
        element._fData = {}
        element._setSEFparent(self)
        return element


class StaticBinding(object):
    pass





















class Specialist(Service):

    """Service for finding/creating objects of a specific type family

        Specialists are the high-level building blocks of TransWarp
        applications, providing "well-known" locations for retrieving or
        creating objects that play a given role in an application.  They also
        serve as a focal point for operations that deal with objects of a
        particular type, but which deal with zero or more than one instance
        of that type (and thus can't be instance methods).

        Why not just use a class?  Because a Specialist serves as a "placeful"
        implementation of storage and lifecycle management for its objects,
        while classes in the general sense are neither placeful nor provide
        storage/lifecycle management.

        This basic Specialist implementation supplies retrieval, creation, and
        caching support for Elements based on Records (see the
        TW.Database.DataModel package).  It should be straightforward to create
        mixin classes, however, that implement other storage methodologies such
        as ZODB-backed BTrees, etc.

        Also, most application Specialists will probably add in a few
        application-specific methods, and Zope 3 applications will probably
        also want to define more specific interfaces than 'ISpecialist' so
        they can use views to create user interfaces for their Specialists.

        Configuring a Specialist

            Specialists are specified as subclasses of 'SEF.Specialist'.  Here
            are a few of the attributes you can specify in subclasses:

             * 'isAbstract' -- if true, the Specialist will not create new
                items.  The default is false.

             * 'elementClass' -- the class used for retrieved or created
                elements.  Can be specified using 'SEF.bindTo' functions.

             * 'keyGenerator' -- an object with a 'next()' method, which will
                be called to generate the "next" key value for a newly created
                item, if a key is not supplied by the caller.

             * 'cache' -- A 'OnceClass' that implements the 'TW.Caching.ICache'
               interface, such as any of the 'TW.Caching' cache classes, or
               the 'TW.Database.Transactions.TransactionalCache' class.
               The default is 'TW.Caching.WeakCache'.

            Note that not all subclasses of Specialist may use or honor these
            attributes, since it is always possible to override the methods
            in this base class that use them.

        Record Management Support

            To support retrieving DataModel Records from RecordManagers, there
            are some additional attributes which you must specify:

             * 'recordManager' -- the RecordManager which records will be
                retrieved from; can be specified using a 'SEF.bindTo' function.

             * 'requiredType' -- The name of the RecordType which records
                retrieved from 'recordManager' must have, to be considered
                valid for retrieval.

             * 'keyField' -- name of the record field which corresponds to the
                application key.

             * 'keyConstants' -- An optional sequence of '(key,value)' pairs
                which will be passed to 'recordManager.getItem()' along with
                the key field.  This helps support multi-field keys, which is
                especially useful with CORE and WarpCORE "object names".

            Of course, if you are using a Specialist subclass/variant which
            doesn't use RecordManagers, then you needn't supply these
            class attributes.

        Polymorphism (Sub-Specialist) Support

            In many applications, there will be Specialists whose scope
            includes more-specialized variants of themselves.  For example, a
            task management application might have two specialists, 'Tasks'
            and 'ToDos', where the to-do item is a more specialized kind of
            task.  Semantically, the 'Tasks' specialist must also be able to
            retrieve items that are actually managed by the 'ToDos' specialist.

            The base 'Specialist' class includes support for this circumstance,
            so long as the record management support is being used, the 
            specialists are using the same RecordManager, and the RecordTypes
            are subclasses of each other.  To activate this support, supply
            a 'subtypeSpecialists' class attribute which is a sequence of the
            specialists which specialize in direct subtypes.
            'SEF.bindToNames()' is an easy way to provide such a sequence,
            e.g.::

                class Task(SEF.Element):
                    ...

                class ToDo(Task):
                    ...

                class Project(Task):
                    ...

                class Tasks(SEF.Specialist):

                    elementClass = Task
                    subtypeSpecialists = SEF.bindToNames('ToDos', 'Projects')

                    ...


                class ToDos(SEF.Specialist):

                    elementClass = ToDo

                    ...


                class Projects(SEF.Specialist):

                    elementClass = Project

                    ...

            The subtype specialists will be asked to retrieve an object
            whenever the more-general specialist does not have a suitable
            item available in its cache.  The first non-None item returned
            from one of the subtype specialists will be used.  If no subtype
            specialist claims the item, the more-general specialist will
            use its own element class to wrap the retrieved record.
    """

    __implements__ = ISpecialist

    isAbstract     = 0

    elementClass   = requireBinding(
        "Class for elements managed by this specialist"
    )

    keyGenerator   = requireBinding("Object with a 'next()' method")

    recordManager  = requireBinding("RecordManager to get records from")
    requiredType   = requireBinding("RecordType name that records must have")
    keyField       = requireBinding("Name of record key field")
    keyConstants   = ()         # key/value pairs to be passed to recordType

    subtypeSpecialists = ()     # specialists to check for subtypes

    from TW.Caching import WeakCache as cache















    def __getitem__(self, key, default=NOT_GIVEN):

        """Retrieve element designated by 'key'; raise KeyError if not found"""

        item = self.cache.get(key, NOT_GIVEN)

        if item is NOT_GIVEN:
            item = self._retrieveItem(key)
            self.cache[key] = item

        if item is NOT_FOUND:

            if default is NOT_GIVEN:
                raise KeyError,key

            item = default

        return item


    def getItem(self, key, default=None):

        """Retrieve element designated by 'key', or 'default' if not found"""

        return self.__getitem__(key,default)


    def newItem(self, key=None):

        """Create element with key 'key' (or a new key if 'key' is None)"""

        if self.isAbstract:
            raise TypeError("Abstract specialists can't create new items")

        if key is None:
            key = self.keyGenerator.next()

        item = self.cache[key] = self._newItem(key)
        return item


    def _retrieveItem(self,key):

        """The heavy lifting for retrieval; redefine for non-RM subclasses"""

        record = self.recordManager.getItem(
            self.keyConstants + ((self.keyField,key),)
        )

        # record doesn't exist or is wrong type, ditch it...

        if not record.hasType(self.requiredType):

            if not record.exists():
                record.invalidate()

            return None


        # Check sub-specialists so that we get most-specific type

        for sub in self.subtypeSpecialists:

            item = sub.getItem(record[sub.keyField])

            if item is not None:
                return item


        return self._wrapElement(record)


    def _wrapElement(self,record):

        """Wrap 'record' in an Element"""

        element = self.elementClass()
        element._fData = record
        element._setSEFparent(self)

        return element

    def _newItem(self,key):

        """The heavy lifting for creation; redefine for non-RM subclasses"""

        record = self.recordManager.getItem(
            self.keyConstants + ((self.keyField,key),)
        )

        if record.exists():
            raise KeyError(key, "key already exists")

        record.addType(self.requiredType)

        item = self._wrapElement(record)
        self.cache[key] = item

        return item
























class FeatureMC(Meta.MethodExporter):

    """Method-exporting Property
    
        This metaclass adds property support to Meta.MethodExporter by adding
        '__get__', '__set__', and '__delete__' methods, which are delegated
        to the method templates for the 'get', 'set' and 'delattr' verbs.

        In other words, if you define a feature 'foo', following standard
        'namingConvention' settings for its 'set', 'get' and 'delattr' verbs,
         and 'bar' is an Element whose class includes the 'foo' feature, then
        'bar.foo = 1' is equivalent to 'bar.setFoo(1)'.  Similarly,
        referencing 'bar.foo' by itself is equivalent to 'bar.getFoo()',
        and 'del bar.foo' is equivalent to 'bar.delattrFoo()'.

        (Note: this is true even if the Element class supplies its own 'setFoo'
        or 'getFoo' implementations, since the 'getMethod()' API is used.)

        Please see the 'TW.API.Meta.MethodExporter' class documentation for
        more detail on how method templates are defined, the use of naming
        conventions, verbs, template variants, etc."""

    def __get__(self, ob, typ=None):

        """Get the feature's value by delegating to 'ob.getX()'"""

        if ob is None: return self
        return self.getMethod(ob,'get')()

    def __set__(self, ob, val):

        """Set the feature's value by delegating to 'ob.setX()'"""

        return self.getMethod(ob,'set')(val)

    def __delete__(self, ob):

        """Delete the feature's value by delegating to 'ob.delattrX()'"""

        return self.getMethod(ob,'delattr')()

class StructuralFeature(object):

    __metaclasses__ = FeatureMC,

    isRequired    = 0
    lowerBound    = 0
    upperBound    = None    # None means unbounded upper end

    isOrdered     = 0
    isChangeable  = 1       # default is to be changeable

    referencedEnd = None    # and without an 'other end'
    referencedType = None
    defaultValue   = None

    def get(self):
        feature = self.__class__.__feature__
        return self.__dict__.get(feature.__name__, feature.defaultValue)

    get.namingConvention = 'get%(initCap)s'


    def set(self,val):
        feature = self.__class__.__feature__
        self.__dict__[feature.__name__]=val
        feature._changed(self)

    set.namingConvention = 'set%(initCap)s'


    def delete(self):
        feature = self.__class__.__feature__
        del self.__dict__[feature.__name__]
        feature._changed(self)

    delete.namingConvention = 'delete%(initCap)s'
    delete.verb = 'delattr'    

    def _changed(feature, element):
        pass

class Field(StructuralFeature):

    __class_implements__ = IValue    
    upperBound = 1

class Collection(StructuralFeature):

    __class_implements__ = ICollection

    def _getList(feature, element):
        return element.__dict__.setdefault(feature.__name__, [])
        
    def get(self):
        feature = self.__class__.__feature__
        return feature._getList(self)

    get.namingConvention = 'get%(initCap)s'

    def set(self,val):
        feature = self.__class__.__feature__
        feature.__delete__(self)
        self.__dict__[feature.__name__]=val
        feature._changed(self)

    set.namingConvention = 'set%(initCap)s'

    def add(self,item):
        """Add the item to the collection/relationship"""      
        feature = self.__class__.__feature__
        ub = feature.upperBound
        value = feature._getList(self)

        if not ub or len(value)<ub:
            feature._notifyLink(self,item)
            feature._link(self,item)
            feature._changed(self)
        else:
            raise ValueError("Too many items")

    add.namingConvention = 'add%(initCap)s'

    def remove(self,item):
        """Remove the item from the collection/relationship, if present"""
        feature = self.__class__.__feature__
        feature._unlink(self,item)
        feature._notifyUnlink(self,item)
        feature._changed(self)

    remove.namingConvention = 'remove%(initCap)s'


    def replace(self,oldItem,newItem):

        feature = self.__class__.__feature__

        d = feature._getList(self)
        p = d.index(oldItem)

        if p!=-1:
            d[p]=newItem
            feature._notifyUnlink(self,oldItem)
            feature._notifyLink(self,newItem)
            feature._changed(self)
        else:
            raise ValueError(oldItem,"not found")

    replace.namingConvention = 'replace%(initCap)s'















    def delete(self):
        """Unset the value of the feature (like __delattr__)"""

        feature = self.__class__.__feature__
        referencedEnd = feature.referencedEnd

        d = feature._getList(self)

        if referencedEnd:
            
            for item in d:
                otherEnd = getattr(item.__class__,referencedEnd)
                otherEnd._unlink(item,self)

        del self.__dict__[feature.__name__]
        feature._changed(self)

    delete.namingConvention = 'delete%(initCap)s'
    delete.verb = 'delattr'    


    def _notifyLink(feature, element, item):

        referencedEnd = feature.referencedEnd

        if referencedEnd:
            otherEnd = getattr(item.__class__,referencedEnd)
            otherEnd._link(item,element)


    def _notifyUnlink(feature, element, item):

        referencedEnd = feature.referencedEnd

        if referencedEnd:
            otherEnd = getattr(item.__class__,referencedEnd)
            otherEnd._unlink(item,element)




    def _link(feature,element,item):
        d=feature._getList(element)
        d.append(item)
        feature._changed(element)

    def _unlink(feature,element,item):
        d=feature._getList(element)
        d.remove(item)
        feature._changed(element)


class Reference(Collection):

    __class_implements__ = IReference

    upperBound = 1

    def get(self):
        feature = self.__class__.__feature__
        vals = feature._getList(self)
        if vals: return vals[0]

    get.namingConvention = 'get%(initCap)s'


    def set(self,val):
        feature = self.__class__.__feature__
        feature.__delete__(self)
        feature.getMethod(self,'add')(val)

    set.namingConvention = 'set%(initCap)s'










class Sequence(Collection):

    __class_implements__ = ISequence

    isOrdered = 1

    def insertBefore(self,oldItem,newItem):

        feature = self.__class__.__feature__
        d = feature._getList(self)
        
        ub = feature.upperBound
        if ub and len(d)>=ub:
            raise ValueError("Too many items")

        i = -1
        if d: i = d.index(oldItem)

        if i!=-1:
            d.insert(i,newItem)
            feature._changed(self)
            feature._notifyLink(self,newItem)
        else:
            raise ValueError(oldItem,"not found")
    
    insertBefore.namingConvention = 'insert%(initCap)sBefore'















class Classifier(StaticBinding, Base):
    """Basis for all flavors"""
            
class PrimitiveType(Classifier):
    """A primitive type (e.g. Boolean, String, etc.)"""

class Enumeration(DynamicBinding, Classifier):
    """An enumerated type"""

class DataType(Classifier):
    """A complex datatype"""

class Element(DataType):
    """An element in its own right"""
    __implements__ = IElement


setupModule()























