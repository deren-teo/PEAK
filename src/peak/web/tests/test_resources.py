from unittest import TestCase, makeSuite, TestSuite
from peak.api import *
from peak.tests import testRoot

from test_templates import TestApp, BasicTest

class ResourceApp1(TestApp):

    # This makes all 'peak.*' package resources available for testing;
    # Ordinarily, you'd do this via a config file, but this is quick and easy

    __makePkgAvailable = binding.Make(lambda: True,
        offerAs = ['peak.web.resource_packages.peak.*']
    )

    show = web.bindResource('template1')

class MethodTest1(BasicTest):

    appClass = ResourceApp1

    def setUp(self):
        r = testRoot()
        self.policy = web.TestPolicy(self.appClass(r))

















class ResourceApp2(ResourceApp1):

    show = web.bindResource('template2')

    xml = web.bindResource(
        '/peak.running/EventDriven', permissionNeeded=security.Anybody
    )

class MethodTest2(MethodTest1):
    appClass = ResourceApp2

    rendered = """<body>
<h1>The title (with &lt;xml/&gt; &amp; such in it)</h1>

<ul><li>1</li><li>2</li><li>3</li></ul>

<a href="http://127.0.0.1/++resources++/peak.running/EventDriven.xml">
The EventDriven.xml file, found at
http://127.0.0.1/++resources++/peak.running/EventDriven.xml
</a>

</body>
"""


















class ResourceTests(TestCase):

    def testSubObjectRejection(self):
        # Files and templates shouldn't allow subitems in PATH_INFO
        paths = 'peak.web/resource_defaults.ini', 'peak.web.tests/template1'
        policy = web.TestPolicy(ResourceApp1(testRoot()))
        for path in paths:
            try:
                policy.simpleTraverse('/++resources++/%s/subitem' % path, True)
            except web.NotFound,v:
                self.assertEqual(v.args[0], "subitem")
            else:
                raise AssertionError("Should have raised NotFound:", path)

    def testURLcalculations(self):

        # Simple paths: direct children of a non-IPlace parent
        r=web.Resource(testRoot())
        self.assertEqual(r.place_url,'')
        r=web.Resource(testRoot(),'foo')
        self.assertEqual(r.place_url,'foo')

        # Skin path is resource prefix
        policy = web.TestPolicy(ResourceApp1(testRoot()))
        ctx = policy.simpleTraverse('/++resources++', False)
        self.assertEqual(ctx.current.place_url, '++resources++')

        # Skin children should include resource prefix
        ctx2 = ctx.traverseName('peak.web')
        self.assertEqual(ctx2.current.place_url, '++resources++/peak.web')

        # check absolute ("mount point") URL
        r=web.Resource(testRoot(),'foo',place_url="http://example.com/foo")
        ctx = policy.newContext()
        ctx = ctx.childContext('foo',r)
        self.assertEqual(ctx.absoluteURL, ctx.current.place_url)





TestClasses = (
    MethodTest1, MethodTest2, ResourceTests,
)

def test_suite():
    return TestSuite([makeSuite(t,'test') for t in TestClasses])



































