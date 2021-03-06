"""Binding tests"""

from unittest import TestCase, makeSuite, TestSuite
from peak.api import *
from peak.tests import testRoot
from sets import Set
import dispatch.predicates, peak.binding.components

class baseWithClassAttr(binding.Component):

    myName = binding.classAttr( binding.Make( lambda self: self.__name__ ) )

class subclassWithClassAttr(baseWithClassAttr):
    pass


class anotherSubclass(baseWithClassAttr):
    pass


class ClassAttrTest(TestCase):

    def testActivationOrder(self):
        # Note: order is to confirm that the using a once binding on a
        # base class doesn't prevent the subclass' copy of the binding
        # from activating.
        assert subclassWithClassAttr.myName == 'subclassWithClassAttr'
        assert baseWithClassAttr.myName == 'baseWithClassAttr'
        assert anotherSubclass.myName == 'anotherSubclass'

    def testMetaTypes(self):
        assert anotherSubclass.__class__ is baseWithClassAttr.__class__
        assert anotherSubclass.__class__.__name__ == 'baseWithClassAttrClass'








class assemblyTracer(binding.Component):
    """Tracing for assembly events"""

    log = binding.Require("logging function")
    activated = binding.Require("list to append ids to")
    id = binding.Require("identity of this object")

    def uponAssembly(self):
        if self.__objectsToBeAssembled__ is not None:
            self.activated.append(self.id)
        self.log(('entering',self.id,self.__objectsToBeAssembled__))
        super(assemblyTracer,self).uponAssembly()
        self.log(('exiting',self.id))

    # The following operation doesn't work because self.log may not be
    # initialized yet.  If you want to log 'notifyUponAssembly' events, it has
    # to be done some other way.
    #def notifyUponAssembly(self,child):
    #    self.log(('requesting notify for',child,'by',self))
    #    super(assemblyTracer,self).notifyUponAssembly(child)

class counter(object):
    v = 0
    def next(self):
        self.v += 1
        return self.v

class Outermost(assemblyTracer):
    foo = binding.Require("A component goes here")

class InnerMost(assemblyTracer):
    thingy = binding.Make(lambda: None, uponAssembly=True)

class Middle(assemblyTracer):

    def child(self):
        return InnerMost(self,
            id=self.id+1, log=self.log, activated=self.activated
        )
    child = binding.Make(child, uponAssembly=True)

class AssemblyTests(TestCase):

    verbose = False

    def setUp(self):
        self.log = []
        self.activated = []
        self.append = self.log.append

    def assertCompleteness(self,obCount):
        a = self.activated[:]
        a.sort()
        assert a == range(1,obCount+1), a

    def tearDown(self):
        if self.verbose:
            print "Event log for %s:" % (self,)
            print
            from pprint import pprint
            pprint(self.log)
            print

    def testConnectBefore(self):
        # Create parent, then child, then activate parent
        log = self.append
        root = Outermost(log=log, activated=self.activated, id = 1)
        root.foo = InnerMost(root, id=2, log=log, activated=self.activated)
        root.getParentComponent()   # whitebox hack for testing; don't do this
        self.assertCompleteness(2)

    def testInit(self):
        # Create parent, activate, then attach child
        log = self.append
        root = Outermost(None, log=log, activated=self.activated, id=1)
        root.foo = InnerMost(root, id=2, log=log, activated=self.activated)
        self.assertCompleteness(2)





    def testKW(self):
        # create child, then parent, then activate
        log = self.append
        root = Outermost(None,
            log=log, activated=self.activated, id=1,
            foo = InnerMost(id=2, log=log, activated=self.activated)
        )
        self.assertCompleteness(2)


    def testBindingSubscribes(self):
        # create parent w/child that creates a child
        log = self.append
        root = Outermost(None,
            log=log, activated=self.activated, id=1,
            foo = Middle(id=2, log=log, activated=self.activated)
        )
        self.assertCompleteness(3)



    def testDelayedSubscribe(self):
        # create parent w/child, assembled, then create child
        log = self.append
        root = Outermost(None, log=log, activated=self.activated, id=1,
            foo = Outermost(id=3, log=log, activated=self.activated)
        )
        new = InnerMost(root.foo, log=log,activated=self.activated, id=2)
        self.assertCompleteness(3)












testList = [1,2,'buckle your shoe']

class DescriptorData(binding.Component):

    thing1 = binding.Make(lambda: "this is my thing")
    thing2 = binding.Obtain('thing1')
    thing3 = binding.Require('This is required')
    thing4 = binding.Obtain(['thing1','thing2'])
    thing7 = 'aService/nestedService/namedThing'
    thing8 = binding.Obtain(naming.Indirect('thing7'))
    underflow = binding.Obtain('/'.join(['..']*50)) # 50 parents up

    class aService(binding.Component):

        thing5 = binding.Obtain('..')

        class nestedService(binding.Component):

            thing6 = binding.Obtain('../..')

            deep = binding.Obtain('deep')

            namedThing = binding.Make(binding.Component)

            acquired = binding.Obtain('thing1')

            getRoot = binding.Obtain('/')

            getUp = binding.Obtain('..')

        nestedService = binding.Make(nestedService)

    aService = binding.Make(aService)
    newDict  = binding.Make(dict)

    listCopy = binding.Make(lambda: testList[:])    # XXX
    deep = binding.Obtain('aService/nestedService/thing6/thing1')
    testImport = binding.Obtain('import:unittest:TestCase')



class DescriptorTest(TestCase):

    def setUp(self):
        self.data = DescriptorData(testRoot(), 'data')


    def testNaming(self):
        svc = self.data.aService
        gcn = binding.getComponentName
        assert gcn(svc)=='aService'
        assert gcn(svc.nestedService)=='nestedService'
        assert gcn(svc.nestedService.namedThing)=='namedThing'
        assert gcn(self.data)=='data'


    def testBinding(self):
        thing2 = self.data.thing2
        assert (thing2 is self.data.thing1), thing2
        assert self.data.__dict__['thing2'] is thing2


    def testMulti(self):
        thing4 = self.data.thing4
        assert len(thing4)==2
        assert type(thing4) is tuple
        assert thing4[0] is self.data.thing1
        assert thing4[1] is self.data.thing2


    def testConstructors(self):
        self.assertRaises(TypeError, DescriptorData, nonExistentKeyword=1)

        td = {}
        assert DescriptorData(newDict = td).newDict is td

    def testIndirect(self):
        assert self.data.thing8 is self.data.aService.nestedService.namedThing




    def testHasParentCriterion(self):
        from dispatch import strategy, predicates, functions
        from peak.binding.components import HasParentCriterion as HPC
        from peak.binding.components import dispatch_by_hierarchy

        data = HPC(self.data)
        svc  = HPC(self.data.aService)
        table = {data.ptr:"pass", None:"fail"}
        strategy.validateCriterion(data,
            strategy.make_node_type(dispatch_by_hierarchy), # XXX
            parents=[HPC(p) for p in binding.iterParents(self.data)]
        )
        self.failUnless(svc.implies(data))

        for item in self.data, self.data.aService.thing5, self.data.thing8:
            self.failUnless(strategy.Pointer(item) in data)
            self.assertEqual(dispatch_by_hierarchy(table, item),"pass")
        for item in self.data.getParentComponent(), self.data.thing1, None:
            self.failIf(strategy.Pointer(item) in data)
            self.assertEqual(dispatch_by_hierarchy(table, item),"fail")
        table[svc.ptr] = "pass"
        self.assertEqual(Set(data.matches(table)), Set([svc.ptr,data.ptr]))

        gf = functions.GenericFunction(lambda x:None)
        d = locals()
        parse = gf.parse
        pe = lambda e: parse(e,d,globals())
        self.assertEqual(pe('binding.hasParent(x,self.data)'),
            strategy.Signature(x=data))

        [gf.when("binding.hasParent(x,self.data)")]
        def gf(x): return "in data"
        [gf.when("binding.hasParent(x,self.data.aService)")]
        def gf(x): return "in service"

        self.assertEqual(gf(self.data),"in data")
        self.assertEqual(gf(self.data.thing8),"in service")
        self.assertEqual(gf(self.data.aService.thing5),"in data")
        self.assertEqual(gf(self.data.aService.nestedService),"in service")


    def testParents(self):

        p1 = self.data.aService.thing5
        p2 = self.data.aService.nestedService.thing6
        p3 = self.data.underflow

        try:
            assert p1 is p2
            assert p1 is self.data
            assert p3 is None
        finally:
            del self.data.aService.thing5
            del self.data.aService.nestedService.thing6
            del self.data.underflow


    def testForError(self):
        try:
            self.data.thing3
        except NameError:
            pass
        else:
            raise AssertionError("Didn't get an error retrieving 'thing3'")


    def testNew(self):

        data = self.data
        d = data.newDict
        assert type(d) is dict      # should be dict
        assert data.newDict is d    # only compute once

        data = DescriptorData()
        assert d == data.newDict        # should be equal
        assert d is not data.newDict    # but separate!






    def testCopy(self):

        data = self.data
        l = data.listCopy

        assert type(l) is list      # should be a list
        assert l == testList        # should be equal
        assert l is not testList    # but separate!


    def testDeep(self):

        data = self.data
        thing = data.thing1
        assert data.deep is thing

        nested = data.aService.nestedService

        assert nested.deep is thing
        assert nested.acquired is thing
        assert nested.getRoot is binding.getParentComponent(data)
        assert nested.getUp is data.aService


    def testImport(self):
        assert self.data.testImport is TestCase


    def testPaths(self):
        svc = self.data.aService
        gcp = binding.getComponentPath

        assert str(gcp(svc,self.data))=='aService'
        assert str(gcp(svc.nestedService,self.data))=='aService/nestedService'
        assert str(
            gcp(svc.nestedService.namedThing,self.data)
        )=='aService/nestedService/namedThing'




    def testAbsPaths(self):
        svc = self.data.aService
        gcp = binding.getComponentPath

        assert str(gcp(svc))=='/data/aService'
        assert str(gcp(svc.nestedService))=='/data/aService/nestedService'
        assert str(
            gcp(svc.nestedService.namedThing)
        )=='/data/aService/nestedService/namedThing'


    def testSuggestions(self):
        data = DescriptorData(None, 'data',
            thing1 = binding.Component(),
            thing2 = DescriptorData(
                thing4 = [binding.Component(), binding.Component()]
            ),
            thing3 = "foo",
            thing4 = binding.Component(1)
        )
        assert binding.getParentComponent(data.thing1) is data
        assert binding.getParentComponent(data.thing2) is data
        assert binding.getParentComponent(data.thing3) is None
        assert binding.getParentComponent(data.thing4) == 1

        assert binding.getComponentName(data.thing1)=='thing1'
        assert binding.getComponentName(data.thing2)=='thing2'
        assert data.thing3 == "foo"
        assert binding.getComponentName(data.thing4) is None

        assert isinstance(data.thing2.thing4, list)
        assert len(data.thing2.thing4) == 2

        for ob in data.thing2.thing4:
            assert ob.__class__ is binding.Component
            assert binding.getParentComponent(ob) is data.thing2
            assert binding.getComponentName(ob) == 'thing4'
            assert ob is not data.thing2.thing1
            assert ob is not data.thing2.thing2


TestClasses = (
    AssemblyTests, ClassAttrTest, DescriptorTest,
)

def test_attributes():
    from peak.util import doctest
    return doctest.DocFileSuite(
        'attributes.txt', optionflags=doctest.ELLIPSIS, package='peak.binding',
    )

def test_components():
    from peak.util import doctest
    return doctest.DocFileSuite(
        'components.txt', optionflags=doctest.ELLIPSIS, package='peak.binding',
    )

def test_suite():
    return TestSuite(
        [makeSuite(t,'test') for t in TestClasses] +
        [test_attributes(), test_components()]
    )




















