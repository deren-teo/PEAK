"""Running system tests"""

from unittest import TestCase, makeSuite, TestSuite
from peak.api import *
from peak.tests import testRoot
from peak.running.clusters import loadCluster
from peak.running.daemons import AdaptiveTask, TaskQueue
from peak.running.scheduler import UntwistedReactor, MainLoop

test = binding.Component()

loadCluster(test.__instance_offers__,
    config.fileNearModule(__name__,'test_cluster.txt')
)

pm = running.CLUSTER.of(test)


groupToHosts = Items(

    __all__= (
            'foo.baz.com', 'bar.baz.com', 'one.baz.com', 'three.baz.com',
            'five.baz.com', 'two.baz.com','four.baz.com','six.baz.com',
            'frob.baz.com'
    ),

    __orphans__ = ('foo.baz.com', 'bar.baz.com'),

    odd     = ('one.baz.com','three.baz.com','five.baz.com'),
    even    = ('two.baz.com','four.baz.com','six.baz.com'),
    prime   = ('one.baz.com','three.baz.com','five.baz.com','two.baz.com'),
    qux     = ('one.baz.com','frob.baz.com'),

    weird   = (
        'one.baz.com','three.baz.com','five.baz.com','two.baz.com',
        'frob.baz.com'
    ),
)



class ClusterTests(TestCase):

    def checkHosts(self):
        assert pm.hosts()==pm.groups['__all__']

    def checkGroups(self):
        assert pm.groups()==('odd','even','prime','qux','weird')

    def checkMembers(self):
        for group, members in groupToHosts:
            assert pm.groups[group] == members, (group,members,pm.groups[group])

    # XXX need host->group tests, plus ???




























class TestClock(binding.Component):

    now = 0
    log = binding.requireBinding("function to call with event data")

    def time(self):
        return self.now

    def sleep(self,secs):
        self.log(("Sleeping for",secs))
        self.now += secs

    def select(self,i,o,e,timeout):
        self.log(("Select:",i,o,e,timeout))
        self.sleep(timeout)


class ScheduleTestTask(AdaptiveTask):

    job = binding.requireBinding("Simulated job, if any")
    log = binding.requireBinding("function to call with event data")

    def getWork(self):
        self.log(("getting work", self.job))
        return self.job

    def doWork(self,job):
        self.log(("doing work", job))
        return job

class QuietTask(ScheduleTestTask):
    def getWork(self):
        return self.job








class TestApp(binding.Component):

    def reactor(self,d,a):
        return UntwistedReactor( self,
            time = self.clock.time,
            sleep = self.clock.sleep,
            select=self.clock.select
        )

    reactor = binding.Once(reactor, offerAs=[running.IBasicReactor])

    def mainLoop(self,d,a):
        return MainLoop(self, time = self.clock.time)

    mainLoop = binding.Once(mainLoop, offerAs=[running.IMainLoop])

    tq = binding.New(TaskQueue, offerAs=[running.ITaskQueue])

    log = binding.New(list)

    append = binding.bindTo('log/append')

    def clock(self,d,a):
        return TestClock(log=self.append)

    clock = binding.Once(clock)


ping = ('doing work','ping')
pong = ('doing work','pong')
spam = ('doing work','spam')
foo = ('doing work','foo')
bar = ('doing work','bar')
sleep = lambda n: ('Sleeping for',n)

notWork = ('getting work',False)
gotWork = ('getting work',True)
didWork = ('doing work',True)



class ReactiveTests(TestCase):

    verbose = False

    def setUp(self):
        self.app = TestApp(testRoot())
        self.log = self.app.log
        self.append = self.app.append


    def tearDown(self):
        if self.verbose:
            print "Event log for %s:" % (self,)
            print
            from pprint import pprint
            pprint(self.log)
            print


    def checkActivationAndPriorityQueueing(self):

        app = self.app
        tq = app.lookupComponent(running.ITaskQueue)

        tasks = [
            ScheduleTestTask(app, runEvery = 5, priority = 5-priority)
                for priority in range(5)
        ]

        assert len(tq.activeTasks)==5, (tq.activeTasks, tasks)

        for priority in range(5):
            assert tq.activeTasks[priority] is tasks[4-priority]








    def checkPrioritized1(self):

        log = self.append
        app = self.app

        t1 = QuietTask(app, runEvery = 1, job = "ping", log = log, priority=1)
        t2 = QuietTask(app, runEvery = 2, job = "pong", log = log, priority=2)

        app.mainLoop.run(4)

        assert self.log == [
            pong, ping, sleep(1), ping, sleep(1), pong, ping, sleep(1), ping,
            sleep(1), pong, ping
        ]


    def checkPrioritized2(self):

        log = self.append
        app = self.app

        t1 = QuietTask(app, runEvery = 1, job = "ping", log = log, priority=2)
        t2 = QuietTask(app, runEvery = 2, job = "pong", log = log, priority=1)

        app.mainLoop.run(4)

        assert self.log == [
            ping, pong, sleep(1), ping, sleep(1), ping, pong, sleep(1), ping,
            sleep(1), ping, pong
        ]











    def checkIntervalsAndMainLoop(self):

        log = self.append
        app = self.app

        t5 = QuietTask(app, runEvery = 5, job = "ping", log = log)
        t7 = QuietTask(app, runEvery = 7, job = "pong", log = log)

        app.mainLoop.run(60, 5, 20.5)

        # Note: this does not match exactly what would happen with a "real"
        # clock; execution times will make a difference, and the finish-out
        # that happens here, wouldn't take place because the events at the 35
        # second mark wouldn't be scheduled.  It's only this way because the
        # clock doesn't move between 'sleeps'.  But *because* this isn't
        # real, the test is therefore stable (i.e. deterministic), as well
        # as a faster-than-real-time.

        assert self.log == [
            ping, pong, sleep(5), ping, sleep(2), pong, sleep(3), # 10 seconds
            ping, sleep(4), pong, sleep(1), ping, sleep(5), ping, # 20 seconds
            sleep(.5), # at 20.5 seconds idle checking begins
            sleep(.5), # but not idle enough yet, so next is pong at 21 seconds
            pong, sleep(4.0), ping, # 25 seconds
            sleep(1.0), # wake up and make sure we haven't been idle for 5 secs
            sleep(2.0), # but it was a false alarm, so finish waiting to 28 secs
            pong, sleep(2.0), ping,    # 30 seconds now
            sleep(3.0), # idle checker looking for timeout, false alarm again
            sleep(2.0), # idle timeout! but reactor will process pending items;
            pong, ping  # finit at 35 seconds
        ]










    def checkAdaptativeScheduling(self):

        log = self.append

        task = ScheduleTestTask(
            runEvery = 5,
            minimumIdle = 1,
            maximumIdle = 150,
            multiplyIdleBy = 2,
            increaseIdleBy = 7,
            job = False,
            log = log,
        )


        for i in range(10):
            if i==6: task.job = True
            if i==8: task.job = False
            log((i,task(),task.pollInterval))

        assert self.log == [
            notWork, (0,False,5),
            notWork, (1,False,17),
            notWork, (2,False,41),
            notWork, (3,False,89),
            notWork, (4,False,150),
            notWork, (5,False,150),
            gotWork, didWork, (6,True,1),
            gotWork, didWork, (7,True,1),
            notWork, (8,False,5),
            notWork, (9,False,17),
        ]









    def checkRoundRobin(self):

        log = self.append
        app = self.app

        t1 = QuietTask(app, runEvery = 1, job = "ping", log = log, priority=1)
        t2 = QuietTask(app, runEvery = 1, job = "pong", log = log, priority=1)
        t3 = QuietTask(app, runEvery = 1, job = "spam", log = log, priority=1)
        t4 = QuietTask(app, runEvery = 1, job = "foo", log = log, priority=1)
        t5 = QuietTask(app, runEvery = 1, job = "bar", log = log, priority=1)

        app.mainLoop.run(5)

        all = [ping,pong,spam,foo,bar]

        assert self.log == (all+[sleep(1)]) * 5 + all





TestClasses = (
    ClusterTests, ReactiveTests
)

def test_suite():
    s = []
    for t in TestClasses:
        s.append(makeSuite(t,'check'))

    return TestSuite(s)










