"""Extend a PEAK model with the ability to read XML Metadata Interchange files

    Usage::

        import peak.metamodels.xmi.reading as model

        class MyMetaModel(model.App):

            class anElementOfMyMetaModel(model.Element):

                ...

    In other words, create a metamodel as you normally would with 'peak.model'
    classes, but using the 'peak.metamodels.xmi.reading' module instead of
    'peak.model.api'.  Of course, you can also create your own variant
    modules that combine other aspects with this one over the base
    'peak.model.api' module.  Also, you may choose to define your metamodel
    in a module that does not import a specific variant of the 'peak.model'
    module, but instead uses the default unless overridden in an inheriting
    module.  (See, for example, 'peak.metamodels.uml.MetaModel', which uses
    the default model implementation, and 'peak.metamodels.UML.Model', which
    adds domain logic to the raw UML metamodel, and elects to use
    'peak.metamodels.SimpleModel' in place of the default 'peak.model' module.
"""        

from peak.api import *
from peak.util.SOX import Node, Document, load
from kjbuckets import kjGraph
import peak.model.api

__bases__ = peak.model.api,










class XMINode(Node):

    _acquiredAttrs = 'factory','target'

    def _finish(self):
        idref=getattr(self,'xmi.idref',None)
        if idref: return self.factory.get(idref)
    

class XMIJunk(XMINode):

    def _newNode(self,name,atts):
        if name=='XMI.content':
            return XMIElement(name,atts)
        else:
            return XMIJunk(name,atts)
            
    def _finish(self):
        return self


class XMIDocument(Document):

    def _newNode(self,name,atts):
        return XMIJunk(name,atts)

    def _finish(self):
        return self._findFirst('XMI.content')[0]._subNodes













class XMIElement(XMINode):

    def _newNode(self,name,atts):

        if atts.has_key('xmi.id'):

            key = atts['xmi.id']
            element = self.factory.newItem(name,key)         # creating new Element
            
            if element is None:
                return XMINode(name,atts)    # ignore unknown types
                
            return XMIElement(name,atts,target=element)

        elif atts.has_key('xmi.idref'):
        
            key = atts['xmi.idref']
            
            if not self.factory.has_key(key):
                self.factory.addForwardReference(key,self.target)
                
            return XMINode(name,atts)


        # Otherwise, it's a feature
        
        newTarget = self.factory.getSubtarget(self.target,name)
        
        if newTarget is not None:
            return XMIElement(name,atts,target=newTarget)
        else:
            return XMINode(name,atts)    # ignore unknown features


    def _finish(self):
        return self.target._fromXMI(self)





class FeatureTarget:

    def __init__(self, element, featureName):
        self.element = element
        self.feature = getattr(self.element.__class__,featureName)
        #self._XMIMap = self.feature._XMIMap

    def addItem(self, obj):
        self.feature.add(self.element,obj)

    def _fromXMI(self, node):
        return self.feature._fromXMI(self.element, node)





























class XMIFactory:

    def __init__(self,rootService):
        self.rootService = rootService
        self.contents = {}
        self.forwards = kjGraph()
        
    def __getitem__(self,key):      return self.contents[key]
    def get(self,key,default=None): return self.contents.get(key,default)
    def has_key(self,key):          return self.contents.has_key(key)

    def addForwardReference(self,key,target):
        self.forwards.add(key,target)

    def newItem(self,typeName,key):

        typeName = getattr(self.rootService,'_XMIMap',{}).get(typeName)
        if not typeName: return None
        
        element = self.rootService.newElement(typeName)
        self.contents[key]=element
        
        # Fix up any outstanding forward references
        forwards = self.forwards
        if forwards.has_key(key):
            for obj in forwards.neighbors(key):
                obj.addItem(element)
            del forwards[key]

        return element

    def getSubtarget(self,target,name):
        featureName = getattr(target,'_XMIMap',{}).get(name)  
        if not featureName: return None

        if isinstance(target,FeatureTarget):
            return getattr(target,featureName)
        else:
            return FeatureTarget(target,featureName)


class XMIMapMaker_Meta(type):

    def __init__(klass, name, bases, dict):

        super(XMIMapMaker_Meta,klass).__init__(name, bases, dict)

        xm = {}

        for attName in dir(klass):
            # work around Python 2.2 bug #575229 by skipping __weakref__
            if attName!='__weakref__':
                for k in getattr(getattr(klass,attName),'_XMINames',()):
                    xm[k] = attName

        klass._XMIMap = xm


class XMIMapMaker:

    __metaclass__ = XMIMapMaker_Meta





















class StructuralFeature:

    def _fromXMI(feature,element,node):
    
        v = getattr(node,'xmi.value',None)
        if v is not None:
            feature.set(element, v)
        elif node._subNodes:
            feature.set(element, node._subNodes[0])
        elif node._allNodes:
            feature.set(element, ''.join(node._allNodes))
        else:
            return node


class Classifier(XMIMapMaker):

    def _fromXMI(self,node):
        return self



class Reference:
    def _fromXMI(feature,element,node):
        for n in node._subNodes:
            feature.set(element,n)


class Collection:
    def _fromXMI(feature,element,node):
        add = feature.add
        val = feature.get(element)
        for node in node._subNodes:
            if node not in val: add(element,node)







class App(XMIMapMaker):

    def _fromXMI(self,node):
        return node


    def _XMIroot(self,*args,**kw):
        document = apply(XMIDocument,args,kw)
        document.factory = XMIFactory(self)
        document.target = self
        return document


    def importFromXMI(self,filename_or_stream):
        return load(filename_or_stream, self._XMIroot())


config.setupModule()
