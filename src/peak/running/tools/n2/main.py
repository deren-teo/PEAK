"""N2 Main Program"""

from peak.api import *
from peak.running.commands import AbstractCommand

import sys, os, code
from getopt import getopt

try:
    import readline
except:
    readline = None

from interfaces import *
import ns


class N2(AbstractCommand):

    # We put this here so help(n2) will work in the interpreter shell

    """PEAK and pdb are already imported for you.
c is bound to the object you looked up, or the initial context.

cd(x)\t\tlike c = c[x]
cd()\t\tsets c back to the original value
pwd\t\tinfo about c
ls()\t\tshow contents of c
"""

    usage = """usage: peak n2 [-e] [-p] [name]

-e\tif name lookup fails, go into python interactor anyway
-p\tuse python interactor even if there is a more specific interactor
\t(implies -e)"""

    idict = binding.New(dict)       # interpreter dictionary
    width = binding.Constant(80)    # XXX screen width


    def run(self):
        try:
            opts, args = getopt(self.argv[1:], 'ep')
            self.opts = dict(opts)
        except:
            self.invocationError('illegal argument')
            return 1

        if len(args) > 1:
            self.invocationError('too many arguments')
            return 1

        cprt = 'Type "copyright", "credits" or "license" for more information.'
        help = 'Type "help" or "help(n2)" for help.'

        self.banner = 'PEAK N2 (Python %s on %s)\n%s\n%s' % (
            sys.version.split(None, 1)[0], sys.platform, cprt, help)

        self.idict['n2'] = self

        exec 'from peak.api import *' in self.idict
        exec 'import pdb' in self.idict

        for cmd in ('cd','ls'):
            self.idict[cmd] = getattr(self, 'py_' + cmd)

        if readline:
            history = os.path.join(self.environ.get('HOME', os.getcwd()),
                '.n2_history')
            try:
                readline.read_history_file(history)
            except:
                pass

        storage.begin(self)

        try:
            if args:
                c = naming.lookup(self, args[0])
            else:
                c = naming.InitialContext(self)
        except:
           if self.opts.has_key('-p') or self.opts.has_key('-e'):
                c = None
                sys.excepthook(*sys.exc_info()) # XXX
                print >>self.stderr
           else:
                raise

        self.idict['c'] = self.idict['__c__'] = c
        self.idict['pwd'] = `c`

        self.handle(c)

        try:
            storage.abort(self)
        except:
            pass

        if readline:
            readline.write_history_file(history)

        return 0


    def get_pwd(self):
        return self.idict['c']


    def get_home(self):
        return self.idict['__c__']


    def getvar(self, var, default=NOT_GIVEN):
        v = self.idict.get(var, default)
        if v is NOT_GIVEN:
            raise KeyError, var
        else:
            return v


    def setvar(self, var, val):
        if var == 'c':
            raise KeyError, "can't change protected variable"

        self.idict[var] = val


    def unsetvar(self, var):
        if var == 'c':
            raise KeyError, "can't change protected variable"

        try:
            del self.idict[var]
        except:
            pass

    def listvars(self):
        return self.idict.keys()


    def do_cd(self, c):
        self.idict['c'] = c
        self.idict['pwd'] = r = `c`


    def __repr__(self):
        return self.__doc__


    def interact(self, c=NOT_GIVEN, n2=NOT_GIVEN):
        if c is NOT_GIVEN:
            c = self.get_pwd()

        if n2 is NOT_GIVEN:
            n2 = self

        b = self.banner
        if c is not None:
            b += '\n\nc = %s\n' % `c`

        code.interact(banner=b, local=self.idict)


    def handle(self, c):
        if self.opts.has_key('-p'):
            interactor = self
        else:
            interactor = adapt(c, IN2Interactor, self)
            binding.suggestParentComponent(self, None, interactor)

        interactor.interact(c, self)


    # Extra builtins in the python shell

    def py_cd(self, arg=None):
        if arg is None:
            c = self.idict['__c__']
        else:
            c = self.idict['c']
            c = c[arg]

        self.do_cd(c)

        print >>self.stdout, 'c = %s' % self.idict['pwd']


    def py_ls(self):
        c = self.idict['c']
        c = adapt(c, naming.IReadContext, None)
        if c is None:
            print >>self.stderr, "c doesn't support the IReadContext interface."
        else:
            for k in c.keys():
                print >>self.stdout, str(k)


    def printColumns(self, stdout, l, sort=1, rev=0):
        """utility for things that want to print ls-like columnar output"""

        if not l: return
        if sort: l.sort()
        if rev: l.reverse()

        l = [
            len(x) >= self.width and x[:self.width-4]+'...' or x
            for x in l
        ]
        ml = max([len(x) for x in l])+1
        nc = self.width / ml
        # XXX readjust nc if we have space to spare to make more even
        cw = self.width / nc
        nr = (len(l) + nc - 1) / nc
        #print ml, nc, cw, nr
        l.extend(((nr*nc)-len(l)) * [''])
        #print len(l), l
        ll = []
        for i in range(nc):
            ll.append(l[i*nr:(i+1)*nr])
        #print len(ll), ll
        ll = zip(*ll)
        ##print len(ll), ll
        for l in ll:
            l = [x.ljust(cw) for x in l[:nc-1]] + [l[nc-1]]
            print >>stdout, ''.join(l)
