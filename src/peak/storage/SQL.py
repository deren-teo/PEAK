from __future__ import generators
from peak.api import *
from interfaces import *
from peak.util.Struct import makeStructType
from peak.util.imports import importObject
from connections import ManagedConnection, AbstractCursor, RowBase
from new import instancemethod

__all__ = [
    'SQLCursor', 'GenericSQL_URL', 'SQLConnection', 'SybaseConnection',
    'GadflyURL', 'GadflyConnection'
]


def _nothing():
    pass

def NullConverter(descr,value):
    return value






















class SQLCursor(AbstractCursor):

    """Iterable cursor bridge/proxy"""

    conn = binding.Obtain('..')
    multiOK = False

    _cursor = binding.Make(lambda self: self._conn.cursor())


    def close(self):

        if self._hasBinding('_cursor'):
            self._cursor.close()
            del self._cursor

        super(SQLCursor,self).close()


    def __setattr__(self,attr,val):

        if hasattr(self.__class__,attr):
            super(SQLCursor,self).__setattr__(attr,val)

        elif self._hasBinding(attr):
            self._setBinding(attr,val)

        else:
            setattr(self._cursor,attr,val)


    def __getattr__(self,attr):
        return getattr(self._cursor,attr)








    def nextset(self):
        try:
            return getattr(self._cursor, 'nextset', _nothing)()
        except self.conn.NotSupportedError:
            pass


    def _setOutsideTxn(self,value):
        self._delBinding('setTxnState')
        self._setBinding('outsideTxn',value)

    def _getOutsideTxn(self):
        return self._getBinding('outsideTxn',False)

    outsideTxn = property(_getOutsideTxn,_setOutsideTxn)


    def setTxnState(self):
        if self.outsideTxn:
            return self.conn.assertUntransacted
        else:
            return self.conn.joinTxn

    setTxnState = binding.Make(setTxnState)

















    logger = binding.Obtain(PropertyName('peak.logs.sql'))

    __path = binding.Make(lambda self: binding.getComponentPath(self))

    def execute(self, *args):

        self.setTxnState()

        try:

            # XXX need some sort of flags for timing/logging here
            # XXX perhaps best handled as cursor subclass(es) set on
            # XXX the SQLConnection?

            return self._cursor.execute(*args)

        except self.conn.Exceptions:

            __traceback_info__ = args

            self.logger.exception(
                "%s: error executing SQL query: %s\n"
                "Traceback:",
                self.__path, args
            )

            self.conn.closeASAP()    # close connection after error
            raise













    def __iter__(self):

        fetch = self._cursor.fetchmany
        rows = fetch()

        if rows:

            descr = self._cursor.description

            rowStruct = makeStructType('rowStruct',
                [d[0] for d in descr], RowBase,
                __module__ = __name__,
            )

            # mkTuple is a curried constructor for our new 'rowStruct' type
            mkTuple = instancemethod(tuple.__new__,rowStruct,None)

            # Now get a row conversion function for our description, using
            # our rowStruct constructor as a postprocessor
            converter = self.conn.getRowConverter(descr,mkTuple)

        while rows:

            for row in rows:
                yield converter(row)

            rows = fetch()


        if not self.multiOK and self.nextset():
            raise exceptions.TooManyResults










class SQLConnection(ManagedConnection):

    protocols.advise(
        instancesProvide=[ISQLConnection]
    )

    def commitTransaction(self, txnService):
        self.connection.commit()

    def abortTransaction(self, txnService):
        self.closeCursors()
        self.connection.rollback()

    cursorClass = SQLCursor

    DRIVER = binding.Require("DBAPI module name")  # Replace in subclasses

    API = binding.Make(lambda self: importObject(self.DRIVER))

    Error               = \
    Warning             = \
    NotSupportedError   = \
    Date                = \
    Time                = \
    Binary              = \
    Timestamp           = \
    DateFromTicks       = \
    TimeFromTicks       = \
    TimestampFromTicks  = binding.Delegate("API")
    Exceptions          = binding.Obtain(["Error", "Warning"])

    supportedTypes      = 'STRING','BINARY','NUMBER','DATETIME','ROWID'

    TYPES_NS = binding.Make(
        lambda self: config.Namespace('%s.sql_types' % self.DRIVER)
    )

    appConfig = binding.Make(
        lambda self: config.Namespace('%s.appConfig' % self.DRIVER)
    )

    def typeMap(self):
        tm = {}
        ps = self.TYPES_NS
        api = self.API

        for k in self.supportedTypes:
            tm[getattr(api,k)] = importObject(ps.get(k,NullConverter))

        return tm

    typeMap = binding.Make(typeMap)


    def getRowConverter(self,description,post=None):
        """See ISQLConnection.getRowConverter()"""

        typeMap = self.typeMap

        converters = [
            instancemethod(
                typeMap.get(d[1],NullConverter), d, None
            ) for d in description
        ]

        for conv in converters:
            if conv.im_func is not NullConverter:
                # At least one conversion, so we must create a row converter
                if post is None:
                    return lambda row: [
                        conv(col) for (col,conv) in zip(row,converters)
                    ]
                else:
                    return lambda row: post(
                        [conv(col) for (col,conv) in zip(row,converters)]
                    )
        else:
            return post     # No conversions other than postprocessor




class MockSQLConnection(SQLConnection):

    DRIVER = "peak.util.mockdb"

    def _open(self):
        return self.API.connect()

    expect = alsoExpect = provide = binding.Delegate('connection')

    def getRowConverter(self,description,post=None):
        return post     # provide() should be given pre-converted values


class ValueBasedTypeConn(SQLConnection):

    def typeMap(self):

        tm = {}
        ps = self.TYPES_NS
        api = self.API

        for k in self.supportedTypes:

            c = importObject(ps.get(k,NullConverter))

            for v in getattr(api,k).values:
                try:
                    v+''
                except:
                    tm[v] = c
                else:
                    # We support either '.int4' or '.INTEGER' style properties
                    tm[v] = importObject(
                        ps.get(PropertyName.fromString(v),c)
                    )

        return tm

    typeMap = binding.Make(typeMap)


class SybaseConnection(ValueBasedTypeConn):

    DRIVER    = "Sybase"
    hostname  = binding.Obtain(PropertyName('Sybase.client.hostname'), default=None)
    appname   = binding.Obtain(PropertyName('Sybase.client.appname'),  default=None)
    textlimit = binding.Obtain(PropertyName('Sybase.client.textlimit'),default=None)
    textsize  = binding.Obtain(PropertyName('Sybase.client.textsize'), default=None)

    otmap = {
        'systable' : 'S',
        'fkey' : 'RI',
        'defaults' : 'D',
        'proc' : 'P',
        'table' : 'U',
        'view' : 'V',
    }

    def _open(self):
        a = self.address
        db = self.API.connect(
            a.server, a.user, a.passwd, a.db, auto_commit=1, delay_connect=1
        )

        if self.hostname is not None:
            db.set_property(self.API.CS_HOSTNAME, self.hostname)

        if self.appname is not None:
            db.set_property(self.API.CS_APPNAME, str(self.appname))

        if self.textlimit is not None:
            db.set_property(self.API.CS_TEXTLIMIT, int(self.textlimit))

        db.connect()

        if self.textsize is not None:
            db.execute('set textsize %d' % int(self.textsize))

        return db



    def onJoinTxn(self, txnService):
        # Sybase doesn't auto-chain transactions...
        self.connection.begin()


    def txnTime(self):

        # First, ensure that we're in a transaction
        self.joinedTxn

        # Then retrieve the server's idea of the current time
        r = ~ self('SELECT getdate()')
        return r[0]

    txnTime = binding.Make(txnTime)


    def listObjects(self, full=False, obtypes=NOT_GIVEN):
        addsel = addwhere = ''

        if full:
            addsel = ', id, uid, type, userstat, sysstat, sysstat2, indexdel, schemacnt, expdate, deltrig, instrig, updtrig, seltrig, ckfirst, cache, objspare '

        if obtypes is not NOT_GIVEN:
            addwhere = ' where type in (%s)' % \
                ', '.join(["'%s'" % self.otmap.get(s, '') for s in obtypes])

        typecase = ' '.join([
            ("when type = '%s' THEN '%s'" % (v, k))
            for (k, v) in self.otmap.items()
        ])

        return self('''select name as obname, obtype = CASE %s END, crdate%s
            from sysobjects%s''' % (typecase, addsel, addwhere))

    protocols.advise(
        instancesProvide=[ISQLIntrospector]
    )



class PGSQLConnection(ValueBasedTypeConn):

    DRIVER = "pgdb"

    def _open(self):

        a = self.address

        return self.API.connect(
            host=a.server, database=a.db, user=a.user, password=a.passwd
        )


    def txnTime(self):
        self.joinedTxn              # Ensure that we're in a transaction,
        r = ~ self('SELECT now()')  # retrieve the server's idea of the time
        return r[0]

    txnTime = binding.Make(txnTime)

    supportedTypes = (
        'BINARY','BOOL','DATETIME','FLOAT','INTEGER',
        'LONG','MONEY','ROWID','STRING',
    )


class PsycopgConnection(PGSQLConnection):

    DRIVER = "psycopg"

    supportedTypes = (
        'BINARY', 'BOOLEAN', 'DATE', 'DATETIME', 'FLOAT', 'INTEGER',
        'INTERVAL', 'LONGINTEGER', 'NUMBER', 'ROWID', 'STRING', 'TIME'
    )







class SqliteConnection(ValueBasedTypeConn):

    DRIVER = "sqlite"

    supportedTypes = (
        'DATE', 'INT', 'NUMBER', 'ROWID', 'STRING', 'TIME', 'TIMESTAMP',
    )

    def _open(self):
        return self.API.connect(self.address.getFilename())

    def listObjects(self, full=False, obtypes=NOT_GIVEN):
        addsel = addwhere = ''

        if full:
            addsel = ', rootpage, sql '

        if obtypes is not NOT_GIVEN:
            addwhere = ' where type in (%s)' % \
                ', '.join(["'%s'" % s for s in obtypes])

        return self('''select name as obname, type as obtype%s
            from SQLITE_MASTER%s''' % (addsel, addwhere))

    protocols.advise(
        instancesProvide=[ISQLIntrospector]
    )














class GadflyConnection(SQLConnection):

    DRIVER = "gadfly"

    Error    = Exception    # Gadfly doesn't really do DBAPI...  Sigh.
    Warning  = Warning

    supportedTypes = ()

    def _open(self):
        a = self.address
        return self.API.gadfly(a.db, a.dir)

    def createDB(self):
        """Close, clear, and re-create the database"""

        self.close()
        a = self.address

        from gadfly import gadfly
        g = gadfly()
        g.startup(self.address.db, self.address.dir)
        g.commit()
        g.close()


class GadflyURL(naming.URL.Base):

    supportedSchemes = ('gadfly',)
    defaultFactory = 'peak.storage.SQL.GadflyConnection'

    class db(naming.URL.RequiredField):
        pass

    class dir(naming.URL.RequiredField):
        pass

    syntax = naming.URL.Sequence(
        ('//',), db, '@', dir
    )

from peak.naming.factories.openable import FileURL

class SqliteURL(FileURL):
    supportedSchemes = 'sqlite',
    defaultFactory = 'peak.storage.SQL.SqliteConnection'


class GenericSQL_URL(naming.URL.Base):

    supportedSchemes = {
        'sybase':  'peak.storage.SQL.SybaseConnection',
        'pgsql':   'peak.storage.SQL.PGSQLConnection',
        'psycopg': 'peak.storage.SQL.PsycopgConnection',
        'mockdb':  'peak.storage.SQL.MockSQLConnection',
    }

    defaultFactory = property(
        lambda self: self.supportedSchemes[self.scheme]
    )

    class user(naming.URL.Field):
        pass

    class passwd(naming.URL.Field):
        pass

    class server(naming.URL.RequiredField):
        pass

    class db(naming.URL.Field):
        pass

    syntax = naming.URL.Sequence(
        ('//',), (user, (':', passwd), '@'), server, ('/', db)
    )






class OracleURL(naming.URL.Base):

    supportedSchemes = {
        'cxoracle':  'peak.storage.SQL.CXOracleConnection',
        'dcoracle2': 'peak.storage.SQL.DCOracle2Connection',
    }

    defaultFactory = property(
        lambda self: self.supportedSchemes[self.scheme]
    )

    class user(naming.URL.Field):
        pass

    class passwd(naming.URL.Field):
        pass

    class server(naming.URL.RequiredField):
        pass

    syntax = naming.URL.Sequence(
        ('//',), (user, (':', passwd), '@'), server, ('/',)
    )


















class CXOracleConnection(SQLConnection):

    DRIVER = "cx_Oracle"

    def _open(self):
        a = self.address

        return self.API.connect(a.user, a.passwd, a.server)


    def txnTime(self):
        self.joinedTxn              # Ensure that we're in a transaction,
        r = ~ self('SELECT SYSDATE FROM DUAL')  # retrieve the server's idea of the time
        return r[0]

    txnTime = binding.Make(txnTime)

    supportedTypes = (
        'BINARY','CURSOR','DATETIME','FIXED_CHAR','LONG_BINARY',
        'LONG_STRING','NUMBER','ROWID','STRING',
    )




















class DCOracle2Connection(ValueBasedTypeConn):

    protocols.advise(
        instancesProvide=[ISQLIntrospector]
    )

    DRIVER = "DCOracle2"

    def _open(self):
        a = self.address
        return self.API.connect(
            user=a.user, password=a.passwd, database=a.server,
        )

    def txnTime(self):
        self.joinedTxn              # Ensure that we're in a transaction,
        r = ~ self('SELECT SYSDATE FROM DUAL')  # retrieve the server's idea of the time
        return r[0]

    txnTime = binding.Make(txnTime)

    supportedTypes = (
        'BINARY','DATETIME','NUMBER','ROWID','STRING',
    )

















    def typeMap(self):

        tm = {}
        ps = self.TYPES_NS
        api = self.API

        for k in self.supportedTypes:

            c = importObject(ps.get(k,NullConverter))

            for v in getattr(api,k).values:
                v = api.Type(v) # needed to get usable typemap keys
                tm[v] = importObject(ps.get(PropertyName.fromString(v),c))

        return tm

    typeMap = binding.Make(typeMap)


    def listObjects(self, full=False, obtypes=NOT_GIVEN):
        addsel = addwhere = ''

        if full:
            addsel = ', subobject_name, object_id, data_object_id, last_ddl_time, timestamp, status, temporary, generated, secondary'

        if obtypes is not NOT_GIVEN:
            addwhere = ' where object_type in (%s)' % \
                ', '.join(["'%s'" %
                    {'proc':'FUNCTION'}.get(s, s.upper()) for s in obtypes])

        return self('''select lower(object_name) as "obname",
        DECODE(object_type, 'FUNCTION', 'proc', lower(object_type))
        as "obtype", created as "created"%s
            from user_objects%s''' % (addsel, addwhere))







