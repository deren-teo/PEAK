"""
SQL Interactor
"""

from peak.api import *
from commands import *
from interfaces import *
from peak.util.readline_stack import *

from tempfile import mktemp
import sys, os, time, re


varpat = re.compile('\\$\\{((?:[a-zA-Z0-9_]+)|(?:=[^}]+))\\}')


def bufname(s):
    """comvert buffer name to canonical form
    ignoring leading ! on user-defined buffers"""

    if s in ('!.', '!!'):
        return s
    elif s.startswith('!'):
        return s[1:]

    return s


EXPORTED = object() # indicates variable is exported to a python variable


class SQLInteractor(binding.Component):

    editor = binding.Obtain(PropertyName('__main__.EDITOR'), default='vi')

    shell = binding.Obtain('..')
    con = binding.Require('The SQL connection')
    txnSvc = binding.Obtain(storage.ITransactionService)

    state = ''
    pushbuf = binding.Make(list)
    bufs = binding.Make(dict)
    buf = ''
    line = 1
    semi = -1


    vars = binding.Make(lambda: {'prompt':'$S$L$T> '})


    def obnames(self):
        """Object names for completer"""

        si = adapt(self.con, storage.ISQLObjectLister, None)
        if si is not None:
            return [x.obname
                for x in si.listObjects(False,
		('table','view','proc','synonym'))]

        return []

    obnames = binding.Make(obnames, suggestParent=False)


    def prompt(self):
        p = self.getVar('prompt')
        p = p.replace('$L', str(self.line))
        p = p.replace('$S', self.state)
        p = p.replace('$T', (not self.txnSvc.isActive()) and 'U' or '')
        return p



    def interact(self, object, shell):
        binding.suggestParentComponent(shell, None, object)

        self.con.connection # ensure it's opened immediately

        self.quit = False

        pushRLHistory('.n2sql_history', self.complete,
            ' \t\n`~@#%^&*()=+[]|;:\'",<>/?', self.shell.environ)

        while not self.quit:
            try:
                l = self.readline(self.prompt()) + '\n'
            except EOFError:
                print >>shell.stdout
                popRLHistory()
                return

            sl = l.strip()
            if ';' in sl:
                sl = sl.split(';', 1)[0].strip()

            if sl:
                cmd = sl.split(None, 1)[0].lower()

                if self.handleCommand(cmd, l) is not NOT_FOUND:
                    continue

            self.line += 1

            self.updateState(l)
            semi = self.semi

            if semi >= 0:
                b = self.getBuf()
                b, cmd = b[:semi] + '\n', b[semi+1:]
                self.setBuf(b)

                self.handleCommand('go', 'go ' + cmd)

        popRLHistory()



    def getVar(self, name):
        v = self.vars.get(name, '')
        if v is EXPORTED:
            return self.shell.getvar(name, '')

        return v



    def setVar(self, name, val, export=False):
        if not export:
            if self.vars.get(name, '') is EXPORTED:
                export = True

        if export:
            self.vars[name] = EXPORTED
            self.shell.setvar(name, val)
        else:
            self.vars[name] = val



    def importVar(self, name):
        self.vars[name] = EXPORTED



    def exportVar(self, name):
        self.setVar(name, self.getVar(name), True)



    def substVar(self, s):
        s = varpat.split(s)
        for i in range(1, len(s), 2):
            v = s[i]
            if v.startswith('='):
                try:
                    v = eval(s[i][1:], self.shell.idict, self.shell.idict)
                except Exception, x:
                    v = "${%s:ERROR:%s}" % (v, x)
            else:
                v = self.getVar(s[i])
            s[i] = str(v)

        return ''.join(s)



    def getBuf(self, name='!.'):
        name = bufname(name)
        if name.startswith('$'):
            try:
                return str(self.getVar(name[1:]))
            except:
                return ''

        return self.bufs.get(name, '')



    def setBuf(self, val, name='!.', append=False):
        name = bufname(name)

        if name.startswith('$'):
            name = name[1:]
            if append:
                self.setVar(name, self.getVar(name) + val)
            else:
                self.setVar(name, val)
        elif append:
            self.bufs[name] = self.bufs.get(name, '') + val
        else:
            self.bufs[name] = val



    def resetBuf(self):
        self.state = ''; self.line = 1; self.semi = - 1
        self.setBuf('')



    def command(self, cmd):
        return getattr(self, 'cmd_' + cmd.replace('-', '_'), None)



    def handleCommand(self, cmd, l):
        shell = self.shell

        r = NOT_FOUND

        cmd = cmd.lower()
        if cmd[0] == '\\' or cmd in (
            'go','commit','abort','begin','rollback','help'
        ):
            if cmd[0] == '\\':
                cmd = cmd[1:]

            cmdobj = self.command(cmd)
            if cmdobj is None:
                print >>shell.stderr, "command '%s' not found. Try 'help'." % cmd

                return
            else:
                cmdinfo = parseCmd(self.substVar(l), shell)

                r = cmdobj.run(
                    cmdinfo['stdin'], cmdinfo['stdout'], cmdinfo['stderr'],
                    cmdinfo['environ'], cmdinfo['argv']
                )

                # let files get closed, etc
                del cmdinfo

            if r is True:
                self.redraw(self.shell.stdout, True)

        return r



    def toStr(self, v, w=None):
        if v is None:
            if w is None:
                return "NULL"
            return "NULL".ljust(w)[:w]
        elif w is None:
            return str(v)
        elif type(v) in (int, long):
            return "%*d" % (w, v)
        elif type(v) is float:
            return "%*g" % (w, v)
        else:
            return str(v).ljust(w)[:w]



    def showResults(self, c, shower, opts, stdout):
        shower = self.showers.get(shower, 'showHoriz')
        shower = getattr(self, shower)
        if c._cursor.description:
            nr = shower(c, opts, stdout)
            if not opts.has_key('-f'):
                print >>stdout, "(%d rows)" % nr

        while c.nextset():
            if not c._cursor.description:
                continue
            print >>stdout
            nr = shower(c, opts, stdout)
            if not opts.has_key('-f'):
                print >>stdout, "(%d rows)" % nr



    showers = {
        'horiz' : 'showHoriz',
        'vert' : 'showVert',
        'plain' : 'showPlain',
        'python' : 'showPython',
        'ldif' : 'showLDIF',
    }



    def showHoriz(self, c, opts, stdout):
        out = stdout.write
        t, d, l = [], [], []
        first = 1
        nr = 0
        for r in c._cursor.description:
            w = r[2]
            if not w or w <= 0: w = r[3]
            if not w or w <= 0: w = 20 # XXX
            if w<len(r[0]): w = len(r[0])

            t.append(self.toStr(r[0], w)); d.append('-' * w); l.append(w)

        if '-h' not in opts:
            out(' '.join(t)); out('\n')
            out(' '.join(d)); out('\n')

        for r in c:
            nr += 1
            i = 0
            o = []
            for v in r:
                o.append(self.toStr(v, l[i]))
                i += 1

            out(' '.join(o))
            out('\n')

        return nr



    def showVert(self, c, opts, stdout):
        h = [x[0] for x in c._cursor.description]
        w = max([len(x) for x in h])
        nr = 0

        for r in c:
            i = 0
            nr += 1
            for v in r:
                print >>stdout, "%s %s" % (h[i].rjust(w), self.toStr(v))
                i += 1
            print >>stdout

        return nr



    def showPlain(self, c, opts, stdout):
        d = opts.get('-d', '|')
        nr = 0

        if not '-h' in opts:
            print >>stdout, d.join([x[0] for x in c._cursor.description])
        for r in c:
            nr += 1
            print >>stdout, d.join([self.toStr(v) for v in r])

        return nr



    def showPython(self, c, opts, stdout):
        nr = 0

        if not '-h' in opts:
            print >>stdout, c._cursor.description
        for r in c:
            nr += 1
            print >>stdout, r

        return nr



    def showLDIF(self, c, opts, stdout):
        nr = 0
        
        for r in c:
            nr += 1
            cols = r.keys()

            # dn must come first, according to RFC2849...
            try:
                dnix = cols.index('dn')
                del cols[dnix]
                cols.insert(0, 'dn')
            except ValueError:
                # ...though we can't be fully compliant if there is no dn!
                pass
                 
            for col in cols:
                vals = r[col]
                if type(vals) is not list:
                    vals = [vals]
                
                for val in vals:
                    if val is None:
                        continue
                        
                    if type(val) is unicode:
                        val = val.encode('utf8')
                    else:
                        val = str(val)

                    colname = "%s: " % col

                    ascii = True
                    for ch in val:
                        o = ord(ch)
                        if o < 32 or o > 126:
                            ascii = False
                            break

                    if not ascii:
                        colname = "%s:: " % col
                        val = ''.join(val.encode('base64').split())
                    
                    fl = 77 - len(colname)
                    stdout.write(colname + val[:fl] + '\n')
                    
                    val = val[fl:]
                    while val:
                        stdout.write(' ' + val[:76] + '\n')
                        val = val[76:]
                
            print >>stdout

        return nr

       
    def command_names(self):
        l = [k for k in dir(self) if k.startswith('cmd_')]
        l2 = [k[4:].replace('_','-') for k in l
            if getattr(getattr(self, k), 'noBackslash', False)]
        l = ['\\'+k[4:].replace('_','-') for k in l]
        l.sort(); l2.sort()

        return l2 + l



    class cmd_go(ShellCommand):
        """go [-d delim] [-m style] [-h] [-f] [-n] [-s n] [xacts] -- submit current input

-d delim\tuse specified delimiter
-m style\tuse specified format (one of: horiz, vert, plain, python, ldif)
-h\t\tsuppress header
-f\t\tsuppress footer
-n\t\tdon't expand variables in SQL
-s n\t\tsleep 'n' seconds between batches, if xacts is greater than 1

xacts\t\tnumber of times to repeat execution of the input. Only results
\t\tfrom the last time are displayed."""

        noBackslash = True

        args = ('d:m:hfs:n', 0, 1)

        def cmd(self, cmd, opts, args, stdout, stderr, **kw):
            secs = opts.get('-s', '0')
            try:
                secs = float(secs)
            except:
                print >>stderr, "Invalid value for -s: '%s'" % secs
                return

            xacts = 0
            if len(args) == 1:
                try:
                    xacts = int(args[0])
                    if xacts <= 0:
                        raise ValueError
                except:
                    print >>stderr, "Invalid value for xacts: '%s'" % args[0]
                    return

            i = self.interactor.getBuf()
            if i.strip():
                if self.interactor.state:
                    print >>stderr, "Please finish comment or quotes first."
                    return
            else:
                i = self.interactor.getBuf('!!')
                if not i.strip():
                    self.interactor.resetBuf()
                    return

            if opts.has_key('-n'):
                sql = i
            else:
                sql = self.interactor.substVar(i)

            try:
                con = self.interactor.con
                act = self.interactor.txnSvc.isActive()
                
                if xacts > 1:
                    for j in range(xacts - 1):
                        if act:
                            c = con(sql)
                        else:
                            c = con(sql, outsideTxn=True)
                        c.fetchall()    # XXX doesn't handle multiresults!

                        time.sleep(secs)

                if act:
                    c = con(sql, multiOK=True)
                else:
                    c = con(sql, multiOK=True, outsideTxn=True)
            except ZeroDivisionError:
                # currently the error is logged
                # sys.excepthook(*sys.exc_info()) # XXX
                self.interactor.resetBuf()
                return

            shower = opts.get('-m', 'horiz')
            self.interactor.showResults(c, shower, opts, stdout)

            self.interactor.setBuf(i, name='!!')

            self.interactor.resetBuf()

    cmd_go = binding.Make(cmd_go)



    class cmd_abort(ShellCommand):
        """abort -- abort current transaction
rollback -- abort current transaction"""

        noBackslash = True

        args = ('', 0, 0)

        def cmd(self, cmd, stderr, **kw):
            if not self.interactor.txnSvc.isActive():
                print >>stderr, "No transaction active."
            else:
                storage.abortTransaction(self)
                storage.beginTransaction(self)

                self.interactor.resetBuf()

    cmd_rollback = binding.Make(cmd_abort)
    cmd_abort = binding.Make(cmd_abort)



    class cmd_begin(ShellCommand):
        """begin -- begin a new transaction"""

        noBackslash = True

        args = ('', 0, 0)

        def cmd(self, cmd, stderr, **kw):
            if self.interactor.txnSvc.isActive():
                print >>stderr, "Already in a transaction."
            else:
                storage.beginTransaction(self)

            self.interactor.resetBuf()

    cmd_begin = binding.Make(cmd_begin)



    class cmd_commit(ShellCommand):
        """commit -- commit current transaction"""

        noBackslash = True

        args = ('', 0, 0)

        def cmd(self, cmd, stderr, **kw):
            if self.interactor.getBuf().strip():
                print >>stderr, "Use GO or semicolon to finish outstanding input first"
            elif not self.interactor.txnSvc.isActive():
                print >>stderr, "No transaction active."
            else:
                storage.commitTransaction(self)
                storage.beginTransaction(self)

                self.interactor.resetBuf()

    cmd_commit = binding.Make(cmd_commit)



    class cmd_reset(ShellCommand):
        """\\reset -- empty input buffer"""

        args = ('', 0, 0)

        def cmd(self, cmd, **kw):
            self.interactor.resetBuf()

    cmd_reset = binding.Make(cmd_reset)



    class cmd_outside(ShellCommand):
        """\\outside -- begin execution outside a transaction"""

        args = ('', 0, 0)

        def cmd(self, cmd, stderr, **kw):
            if self.interactor.con in self.interactor.txnSvc:
                print >>stderr, "Already active in a transaction; commit or abort first."
            else:
                storage.abortTransaction(self)

            self.interactor.resetBuf()

    cmd_outside = binding.Make(cmd_outside)



    class cmd_exit(ShellCommand):
        """\\exit -- exit SQL interactor
\\quit -- exit SQL interactor"""

        args = ('', 0, 0)

        def cmd(self, cmd, **kw):
            self.interactor.quit = True

    cmd_quit = binding.Make(cmd_exit)
    cmd_exit = binding.Make(cmd_exit)



    class cmd_python(ShellCommand):
        """\\python [code] -- enter python interactor or run code"""

        args = ('', 0, sys.maxint)

        def cmd(self, cmd, args, **kw):
            if args:
                try:
                    exec ' '.join(args) in self.shell.idict
                except:
                    sys.excepthook(*sys.exc_info()) # XXX
            else:
                self.shell.interact()

    cmd_python = binding.Make(cmd_python)



    class cmd_buf_copy(ShellCommand):
        """\\buf-copy dest [src] -- copy buffer src to dest

default for src is '!.', the current input buffer"""

        args = ('', 1, 2)

        def cmd(self, cmd, args, stdout, **kw):
            src = '!.'
            if len(args) == 2:
                src = args[1]

            self.interactor.setBuf(self.interactor.getBuf(src), name=args[0])

            if args[0] == '!.':
                return True

    cmd_buf_copy = binding.Make(cmd_buf_copy)



    class cmd_buf_get(ShellCommand):
        """\\buf-get src -- like \buf-append !. src"""

        args = ('', 1, 1)

        def cmd(self, cmd, args, stdout, **kw):
            self.interactor.setBuf(self.interactor.getBuf(args[0]), append=True)

            return True

    cmd_buf_get = binding.Make(cmd_buf_get)



    class cmd_buf_append(ShellCommand):
        """\\buf-append dest [src] -- append buffer src to dest

default for src is '!.', the current input buffer"""

        args = ('', 1, 2)

        def cmd(self, cmd, args, stdout, **kw):
            src = '!.'
            if len(args) == 2:
                src = args[1]

            self.interactor.setBuf(self.interactor.getBuf(src), name=args[0],
                append=True)

            if args[0] == '!.':
                return True

    cmd_buf_append = binding.Make(cmd_buf_append)



    class cmd_buf_save(ShellCommand):
        """\\buf-save [-a] filename [src] -- save buffer src in a file

-a\tappend to file instead of overwriting"""

        args = ('a', 1, 2)

        def cmd(self, cmd, opts, args, stderr, **kw):
            mode = 'w'
            if opts.has_key('-a'):
                mode = 'a'

            src = '!.'
            if len(args) == 2:
                src = args[1]

            try:
                f = open(args[0], mode)
                f.write(self.interactor.getBuf(src))
                f.close()
            except:
                sys.excepthook(*sys.exc_info()) # XXX

    cmd_buf_save = binding.Make(cmd_buf_save)



    class cmd_buf_load(ShellCommand):
        """\\buf-load [-a] filename [dest] -- load buffer dest from file

-a\tappend to buffer instead of overwriting"""

        args = ('a', 1, 2)

        def cmd(self, cmd, opts, args, stderr, **kw):
            try:
                dest = '!.'
                if len(args) == 2:
                    dest = args[1]

                f = open(args[0], 'r')
                l = f.read()
                self.interactor.setBuf(l, append=opts.has_key('-a'), name=dest)

                f.close()

                l = self.interactor.getBuf(dest)
                if l and not l.endswith('\n'):
                    self.interactor.setBuf('\n', append=True, name=dest)

            except:
                sys.excepthook(*sys.exc_info()) # XXX

            if dest == '!.':
                return True

    cmd_buf_load = binding.Make(cmd_buf_load)



    class cmd_buf_show(ShellCommand):
        """\\buf-show -- show buffer list
\\buf-show [buf] -- show named buffer"""

        args = ('', 0, 1)

        def cmd(self, cmd, args, stdout, **kw):
            if len(args) == 1:
                stdout.write(self.interactor.getBuf(args[0]))
            else:
                l = self.interactor.bufs.keys()
                l.sort()
                stdout.write('\n'.join(l))
                stdout.write('\n')

            stdout.flush()

    cmd_buf_show = binding.Make(cmd_buf_show)



    class cmd_buf_edit(ShellCommand):
        """\\buf-edit -- use external editor on current input buffer"""

        args = ('r:w:', 0, 0)

        def cmd(self, cmd, opts, stderr, **kw):
            t = mktemp()
            f = open(t, 'w')
            f.write(self.interactor.getBuf(opts.get('-r', '!.')))
            f.close()
            r = os.system('%s "%s"' % (self.interactor.editor, t))
            if r:
                print >>stderr, '[edit file unchanged]'
            else:
                f = open(t, 'r')
                l = f.read()
                f.close()
                wr = opts.get('-w', '!.')
                self.interactor.setBuf(l, name=wr)
                if l and not l.endswith('\n'):
                    self.interactor.setBuf('\n', append=True, name=wr)

            os.unlink(t)

            return True

    cmd_buf_edit = binding.Make(cmd_buf_edit)



    class cmd_source(ShellCommand):
        """\\source [-r] filename -- interpret input from file

-r\treset input buffer before sourcing file"""

        args = ('r', 1, 1)

        def cmd(self, cmd, opts, args, stderr, **kw):
            try:
                f = open(args[0], 'r')
                l = f.read()
                if l[-1] == '\n':
                    l = l[:-1]
                l = l.split('\n')
                l.reverse()
                self.interactor.pushbuf = l + self.interactor.pushbuf
                f.close()

                return opts.has_key('-r')
            except:
                sys.excepthook(*sys.exc_info()) # XXX

    cmd_source = binding.Make(cmd_source)



    class cmd_help(ShellCommand):
        """\\help [cmd] -- help on commands"""

        noBackslash = True

        args = ('', 0, 1)

        def cmd(self, stdout, stderr, args, **kw):
            if args:
                c = self.interactor.command(args[0])
                if c is None:
                    print >>stderr, 'help: no such command: ' + args[0]
                else:
                    print c.__doc__
            else:
                print >>stdout, 'Available commands:\n'
                self.shell.printColumns(
                    stdout, self.interactor.command_names(), sort=False)

    cmd_help = binding.Make(cmd_help)



    class cmd_reconnect(ShellCommand):
        """\\reconnect -- abort current transaction and reconnect to database"""

        args = ('', 0, 0)

        def cmd(self, cmd, **kw):
            self.interactor.con.closeASAP()
            storage.abortTransaction(self)

            try:
                del self.obnames
            except:
                pass

            self.interactor.con.connection
            storage.beginTransaction(self)

            self.interactor.resetBuf()

    cmd_reconnect = binding.Make(cmd_reconnect)



    class cmd_redraw(ShellCommand):
        """\\redraw -- redraw current input buffer"""

        args = ('', 0, 0)

        def cmd(self, cmd, **kw):
            self.interactor.redraw(self.shell.stdout)

    cmd_redraw = binding.Make(cmd_redraw)



    class cmd_echo(ShellCommand):
        """\\echo secs -- echo for 'secs' seconds"""

        args = ('-n', 0, sys.maxint)

        def cmd(self, cmd, opts, args, stdout, **kw):
            stdout.write(' '.join(args))
            if not opts.has_key('-n'):
                stdout.write('\n')
            stdout.flush()

    cmd_echo = binding.Make(cmd_echo)



    class cmd_sleep(ShellCommand):
        """\\sleep secs -- sleep for 'secs' seconds"""

        args = ('', 1, 1)

        def cmd(self, cmd, args, stderr, **kw):
            try:
                s = float(args[0])
            except:
                print >>stderr, "%s: invalid number '%s'" % (cmd, args[0])
                return

            time.sleep(s)

    cmd_sleep = binding.Make(cmd_sleep)



    class cmd_set(ShellCommand):
        """\\set [-x] name=val [name2=val2] [...] -- set variables

-x\texport variables to python"""

        args = ('x', 1, sys.maxint)

        def cmd(self, cmd, opts, args, stderr, **kw):
            export = opts.has_key('-x')
            for x in args:
                try:
                    k, v = x.split('=', 1)
                except:
                    print >>stderr, "%s: invalid syntax '%s'" % (cmd, x)
                    continue

                try:
                    self.interactor.setVar(k, v, export)
                except KeyError:
                    print >>stderr, "%s: unable to set '%s'" % (cmd, args[0])

    cmd_set = binding.Make(cmd_set)



    class cmd_import(ShellCommand):
        """\\import name -- import variable from python"""

        args = ('', 1, 1)

        def cmd(self, cmd, args, stderr, **kw):
            self.interactor.importVar(args[0])

    cmd_import = binding.Make(cmd_import)



    class cmd_export(ShellCommand):
        """\\export name -- export variable to python"""

        args = ('', 1, 1)

        def cmd(self, cmd, args, stderr, **kw):
            try:
                self.interactor.exportVar(args[0])
            except KeyError:
                print >>stderr, "%s: unable to export '%s'" % (cmd, args[0])
                return

    cmd_export = binding.Make(cmd_export)



    class cmd_describe(ShellCommand):
        """\\describe [-d delim] [-m style] [-h] [-f] [-v] [name] -- describe objects in database, or named object

-d delim\tuse specified delimiter
-m style\tuse specified format (one of: horiz, vert, plain, python, ldif)
-h\t\tsuppress header
-f\t\tsuppress footer
-v\t\tverbose; give more information
        """

        args = ('d:m:hfv', 0, 1)

        def cmd(self, cmd, opts, args, stdout, stderr, **kw):
            if args:
                print >>stderr, "Feature not implemented yet."
            else:
                si = adapt(self.interactor.con, storage.ISQLObjectLister, None)
                if si is None:
                    print >>stderr, "%s: database doesn't support describe" % cmd
                else:
                    shower = opts.get('-m', 'horiz')
                    c = si.listObjects('-v' in opts)
                    self.interactor.showResults(c, shower, opts, stdout)

    cmd_describe = binding.Make(cmd_describe)



    def redraw(self, stdout, add_hist=False):
        b = self.getBuf()
        self.resetBuf()
        out = self.shell.stdout

        if b.endswith('\n'):
            b = b[:-1]

        b = b.split('\n')

        for l in b:
            addRLHistoryLine(l)
            l += '\n'
            stdout.write(self.prompt())
            stdout.write(l)

            self.line += 1

            self.updateState(l)



    def updateState(self, s):
        state = self.state

        i = 0
        for c in s:
            if not state:
                if c in '\'"/':
                    state = c
                elif c == ';' and self.semi < 0:
                    self.semi = len(self.getBuf()) + i
            elif state == '/':
                if c == '*':
                    state = 'C'
                elif c == ';' and self.semi < 0:
                    self.semi = len(self.getBuf()) + i
                else:
                    state = ''
            elif state == 'C':
                if c == '*':
                    state = c
            elif state == '*':
                if c == '/':
                    state = ''
                else:
                    state = 'C'
            elif state in ("'", '"'):
                if c == state:
                    state = 'D' + c
            elif state[0] == 'D':
                if c == state[1]:
                    state = state[1]
                elif c == '/':
                    state = c
                elif c == ';' and self.semi < 0:
                    self.semi = len(self.getBuf()) + i
                else:
                    state = ''
            i += 1

        self.state = state
        self.setBuf(s, append=True)


    def readline(self, prompt):
        if self.pushbuf:
            l = self.pushbuf.pop()
            self.shell.stdout.write(prompt + l + '\n')
            return l
        else:
            return raw_input(prompt)


    def complete(self, s, state):
        if state == 0:
            #print s
            if s.startswith('!'):
                self.matches = m = []
                for b in self.bufs.keys():
                    if not b.startswith('!'):
                        b = '!' + b
                    m.append(b)
            elif s.startswith('${'):
                self.matches = ['${' + k + '}' for k in self.vars.keys()]
            elif s.startswith('$'):
                self.matches = ['$' + k for k in self.vars.keys()]
            else:
                self.matches = self.command_names() + self.obnames

            self.matches = [x for x in self.matches if x.startswith(s)]

        try:
            return self.matches[state]
        except IndexError:
            return None


protocols.declareAdapter(
    lambda con, proto: SQLInteractor(con=con),
    provides = [IN2Interactor],
    forProtocols = [storage.ISQLConnection]
)