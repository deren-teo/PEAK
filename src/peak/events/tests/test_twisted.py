"""Test event sources and threads with Twisted"""

from __future__ import generators
from unittest import TestCase, makeSuite, TestSuite
from peak.api import *
from peak.tests import testRoot
from test_events import ScheduledThreadsTest, SchedulerTests, ValueTests
from twisted.internet import defer
from twisted.python import failure
import sys

SA = config.ServiceArea(testRoot())
SA.lookupComponent(running.ITwistedReactor)     # force twisted usage


class TestDeferredAsEvent(ValueTests):

    sourceType = defer.Deferred

    def reenter(self,source,event):
        # XXX ugh this is the only way to force this not to fire
        # XXX I'm not sure this is really a valid test
        self.source.subject.called = False
        source.addCallback(self.sink)


class TwistedThreadsTest(ScheduledThreadsTest):

    def setUp(self):
        self.scheduler = SA.lookupComponent(events.IScheduler)

    def testUncaughtError(self):
        pass    # XXX Twisted forces trapping of all errors     :(








class TestDeferreds(TestCase):

    def setUp(self):
        self.d = defer.Deferred()
        self.log = []

    def wait(self):
        try:
            yield self.d; self.log.append(events.resume())
        except:
            self.log.append(sys.exc_info()[1])

    wait = events.threaded(wait)

    def testCallbackWhileWaiting(self):
        self.wait()
        self.assertEqual(self.log, [])
        self.d.callback(42)
        self.assertEqual(self.log, [42])

    def testCallbackBeforeWaiting(self):
        self.assertEqual(self.log, [])
        self.d.callback(42)
        self.wait()
        self.assertEqual(self.log, [42])

    def testErrbackWhileWaiting(self):
        self.wait()
        self.assertEqual(self.log, [])
        self.d.errback(ValueError())
        self.failUnless(self.log[0].type is ValueError, self.log)

    def testErrbackBeforeWaiting(self):
        self.assertEqual(self.log, [])
        self.d.errback(ValueError())
        self.wait()
        self.failUnless(self.log[0].type is ValueError, self.log)




TestClasses = (
    TwistedThreadsTest, TestDeferreds, TestDeferredAsEvent
)

def test_suite():
    s = []
    for t in TestClasses:
        s.append(makeSuite(t,'test'))

    return TestSuite(s)






























