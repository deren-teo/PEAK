"""Unit tests for model.Element/FeatureMC, etc."""

from unittest import TestCase, makeSuite, TestSuite
from peak.api import *

class featureBase(object):

    __metaclass__ = model.FeatureMC

    singular = 1

    newVerbs = Items(
        get     = 'get%(initCap)s',
        set     = 'set%(initCap)s',
        unset   = 'unset%(initCap)s',
        doubled = '%(name)sDoubled',
    )

    def get_single(feature, self):
        return self.__dict__[feature.attrName][0]

    get_single.verb = 'get'
    get_single.installIf = lambda feature,method: feature.singular


    def get_multi(feature, self):
        return self.__dict__[feature.attrName]

    get_multi.verb = 'get'
    get_multi.installIf = lambda feature,method: not feature.singular


    def set(feature,self,val):
        self.__dict__[feature.attrName]=[val]

    def unset(feature,self):
        del self.__dict__[feature.attrName]

    def doubled(feature,self):
        return feature.getMethod(self,'get')() * 2

class X(model.Element):

    class zebra(featureBase):
        singular = 0

    class Y(zebra):
        # test of subclassing from existing feature...
        singular = 1

    class Overwrite(featureBase):
        pass

    def OverwriteDoubled(self):
        return self.__class__.Overwrite.doubled(self) * 3

    class aCollection(featureBase):
        singular = 0
        singularForm = 'item'

        newVerbs = Items(
            add='add%(singularForm.initCap)s'
        )

        def add(feature,self,val):
            self.__dict__[feature.attrName].append(val)


class SubclassOfX(X):

    class Overwrite(featureBase):
        # Even though we redefine the feature here,
        # the old OverwriteDoubled method in the class
        # should apply...
        singular = 0







class checkExport(TestCase):

    def setUp(self):
        self.el = X()

    def checkMethods(self):
        self.el.setY(1)
        assert self.el.getY()==1
        assert self.el.__dict__['Y']==[1]
        assert self.el.YDoubled()==2
        self.el.unsetY()
        assert not self.el.__dict__.has_key('Y')

    def checkDescr(self):
        self.el.zebra = 2
        assert self.el.zebra==[2]
        assert self.el.__dict__['zebra']==[2]
        assert self.el.zebraDoubled()==[2,2]
        del self.el.zebra
        assert not self.el.__dict__.has_key('zebra')

    def checkOverwrite(self):

        self.el.Overwrite = 1
        assert self.el.OverwriteDoubled()==6

        e2 = SubclassOfX()
        e2.Overwrite = 1
        assert e2.OverwriteDoubled()==[1,1,1,1,1,1]

    def checkFancyNames(self):
        self.el.aCollection = 1
        self.el.addItem(9)
        assert self.el.aCollection==[1,9]







class aBase(model.Element):
    mdl_isAbstract = True
    class f1(model.Field): pass
    class f2(model.Field): pass

class aSub(aBase):
    class f3(model.Collection): isComposite=True
    class f1(model.Field): pass
    class a(model.Field): pass

class ordered(model.Element):
    class a(model.Field): sortPosn = 3
    class b(model.Field): sortPosn = 2
    class c(model.Field): sortPosn = 1

class checkMetaData(TestCase):

    def checkFeatures(self):
        assert aBase.mdl_featureNames   == ('f1','f2')
        assert aSub.mdl_featureNames    == ('f1','f2','a','f3')
        assert ordered.mdl_featureNames == ('c','b','a')
        assert aSub.mdl_compositeFeatures == (aSub.f3,)

    def checkIntroduced(self):
        assert aBase.mdl_featuresDefined == (aBase.f1, aBase.f2)
        assert aSub.mdl_featuresDefined  == (aSub.a, aSub.f1, aSub.f3)
        
    def checkChangeableBad(self):
        try:
            class anImmutable(model.Immutable):
                class aFeature(model.Field):
                    pass
        except TypeError:
            pass
        else:
            raise AssertionError,"Immutable allowed changeable features"

    def checkCreate(self):
        self.assertRaises(TypeError,aBase) # base is abstract...
        aSub()  # but subclass shouldn't be!

class anElement1(model.Element):

    class field1(model.Field):
        defaultValue = 1

    class simpleSeq(model.Sequence):
        pass

    class fwdRef(model.Reference):
        referencedEnd = 'backColl'

    class simpleRef(model.Reference):
        pass

    class fwdColl(model.Collection):
        referencedEnd = 'backRef'
        upperBound = 3


class anElement2(model.Element):

    class backColl(model.Collection):
        referencedEnd = 'fwdRef'

    class backRef(model.Reference):
        referencedEnd = 'fwdColl'















class exerciseFeatures(TestCase):

    def setUp(self):
        self.e = anElement1()


    def checkField(self):
        self.e.setField1(5)
        assert self.e.field1==5
        del self.e.field1
        assert self.e.field1==1


    def checkSimpleSeq(self):
        e = self.e

        map(e.addSimpleSeq, range(5))
        assert e.simpleSeq == [0,1,2,3,4]

        e.insertSimpleSeqBefore(1,-1)
        assert e.simpleSeq == [0,-1,1,2,3,4]

        e.removeSimpleSeq(-1)
        assert e.simpleSeq == [0,1,2,3,4]

        e.replaceSimpleSeq(0,-1)
        assert e.simpleSeq == [-1,1,2,3,4]


    def checkFwdRef(self):
        e1=self.e
        e2=anElement2()
        e1.fwdRef = e2
        assert e2.backColl[0] is e1
        assert len(e2.backColl)==1


    def checkSimpleRef(self):
        self.e.simpleRef = 99
        assert self.e.simpleRef == 99

    def checkFwdColl(self):
    
        e = self.e
        e1 = anElement2(); e.addFwdColl(e1)
        e2 = anElement2(); e.addFwdColl(e2)
        e3 = anElement2(); e.addFwdColl(e3)

        assert e.fwdColl == [e1,e2,e3]

        for x,y in zip(e.fwdColl, (e1,e2,e3)):
            assert x is y

        assert e1.backRef is e
        assert e2.backRef is e
        assert e3.backRef is e

        try:
            e.addFwdColl(anElement2())
        except ValueError:
            pass
        else:
            raise AssertionError,"Bounds check failed"


TestClasses = (
    checkExport, checkMetaData, exerciseFeatures, 
)


def test_suite():
    s = []
    for t in TestClasses:
        s.append(makeSuite(t,'check'))
    return TestSuite(s)

