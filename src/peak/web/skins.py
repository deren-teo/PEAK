from peak.api import *
from interfaces import *
from places import Traversable, MultiTraverser
from publish import TraversalPath
from resources import Resource
from environ import traverseName, getCurrent, getSkin, getPolicy

__all__ = [
    'Skin', 'LayerService', 'SkinService',
]


class LayerService(binding.Component):

    """Service for accessing layers (w/caching and sharing between skins)"""

    protocols.advise(
        instancesProvide=[ILayerService]
    )

    layerMap = binding.Make( config.Namespace('peak.web.layers') )

    def getLayer(self,layerName):
        ob = getattr(self.layerMap,layerName)
        binding.suggestParentComponent(self,layerName,ob)
        return ob















class SkinService(binding.Component):

    protocols.advise(
        instancesProvide=[ISkinService]
    )

    app = root = binding.Delegate('policy')

    policy = binding.Obtain('..')

    skinMap = binding.Make( config.Namespace('peak.web.skins') )

    def getSkin(self, name):
        ob = getattr(self.skinMap,name)
        binding.suggestParentComponent(self.policy,name,ob)
        return ob

























class Skin(Traversable):

    """Skins provide a branch-point between the app root and resources"""

    protocols.advise(
        instancesProvide = [ISkin]
    )

    resources  = binding.Make(lambda self: MultiTraverser(items=self.layers))
    cache      = binding.Make(dict)
    policy     = binding.Obtain('..')
    root       = binding.Delegate("policy")

    layerNames = binding.Require("Sequence of layer names")
    layers     = binding.Make(
        lambda self: map(self.policy.getLayer, self.layerNames)
    )

    dummyInteraction = binding.Make(
        lambda self: self.policy.newInteraction(user=None)
    )

    def traverseTo(self, name, ctx):

        if name == getPolicy(ctx).resourcePrefix:
            return self.resources

        return self.root.traverseTo(name, ctx)

    resourcePath = ''  # skin is at root











    def getResource(self, path):

        path = adapt(path,TraversalPath)

        if path in self.cache:
            return self.cache[path]

        start = self.policy.newEnvironment(
            {   'peak.web.skin':self,
                'peak.web.interaction':self.dummyInteraction
            }
        )

        # start at ++resources++
        start = traverseName(start,self.policy.resourcePrefix)

        resourceCtx = path.traverse(start, getRoot = lambda ctx: start)
        self.cache[path] = subject = getCurrent(resourceCtx)
        return subject






















