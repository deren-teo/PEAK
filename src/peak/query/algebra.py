"""Relational Algebra"""

from peak.api import *
from peak.util.hashcmp import HashAndCompare
import interfaces
from interfaces import *
from kjbuckets import kjSet, kjGraph

__all__ = []

class _expr:

    protocols.advise(
        instancesProvide = [IBooleanExpression],
    )

    def conjuncts(self):
        return [self]

    def disjuncts(self):
        return [self]

    def __invert__(self):
        return Not(self)

    def __and__(self,other):
        if self==other or other is EMPTY:
            return self
        return And(self,other)

    def __or__(self,other):
        if self==other or other is EMPTY:
            return self
        return Or(self,other)







class EMPTY(binding.Singleton):

    protocols.advise(
        classProvides = [IBooleanExpression],
    )

    def conjuncts(self):
        return ()

    def disjuncts(self):
        return ()

    def __invert__(self):
        return self

    def __and__(self,other):
        return other

    def __or__(self,other):
        return other

    def simpleSQL(self):
        return ''


class PhysicalDB(binding.Component):

    tables = binding.Make(list)

    tableMap = binding.Make(
        lambda self: dict(self.tables)
    )

    def __getitem__(self,name):
        return Table(name,self.tableMap[name],self)






class Table:

    protocols.advise(
        instancesProvide = [IRelationVariable]
    )

    condition = EMPTY
    outers = ()

    def __init__(self,name,columns,db=None):
        self.name = name
        self.columns = kjGraph([(c,Column(c,self)) for c in columns])
        self.db = db

    def __call__(self,where=None,join=(),outer=(),rename=(),keep=None):
        cols = kjGraph(self.columns)
        rename = kjGraph(rename)
        for rv in tuple(join)+tuple(outer):
            cols = cols + rv.attributes()
        if keep:
            cols = (kjSet(keep)+kjSet(rename)) * cols
        if rename:
            cols = ~rename * cols + (cols-cols.restrict(rename))
        if where is None:
            where = EMPTY
        return BasicJoin(
            self.condition & where, (self,)+tuple(join), tuple(outer), cols
        )

    def __repr__(self):
        return self.name

    def attributes(self):
        return self.columns

    def getDB(self):
        return self.db

    def getInnerRVs(self):
        return (self,)

    def getOuterRVs(self):
        return self.outers

    def getCondition(self):
        return self.condition

    def getReferencedRVs(self):
        all = kjSet([self])
        for rv in self.getInnerRVs()+self.getOuterRVs():
            if not all.has_key(rv):
                all += kjSet(rv.getReferencedRVs())
        return all.items()

    def __getitem__(self,key):
        return self.columns[key]

    def keys(self):
        return self.columns.keys()

    def simpleSQL(self):
        return "SELECT * FROM %s" % self.name




















class Column:

    protocols.advise(
        instancesProvide = [IRelationAttribute]
    )

    def __init__(self,name,table):
        self.name = name
        self.table = table

    def getRV(self):
        return self.table

    def getDB(self):
        return self.table.getDB()

    def simpleSQL(self):
        return self.table.name+'.'+self.name

    def eq(self,dv):
        return Cmp(self,'=',dv)

    def ne(self,dv):
        return Cmp(self,'<>',dv)

    def lt(self,dv):
        return Cmp(self,'<',dv)

    def ge(self,dv):
        return Cmp(self,'>=',dv)

    def gt(self,dv):
        return Cmp(self,'>',dv)

    def le(self,dv):
        return Cmp(self,'<=',dv)





class BasicJoin(Table, HashAndCompare):

    def __init__(self,condition,relvars,outers=(),columns=()):
        myrels = []
        outers=list(outers)
        relUsage = {}

        for rv in relvars:
            myrels.extend(rv.getInnerRVs())
            outers.extend(rv.getOuterRVs())
            condition = condition & rv.getCondition()

        for rv in myrels+outers:
            for r in rv.getReferencedRVs():
                relUsage[r] = relUsage.setdefault(r,0)+1

        if len(myrels)<1:
            raise TypeError("BasicJoin requires at least 1 relvar")

        for k,v in relUsage.items():
            if v>1:
                raise ValueError("Relvar used more than once",k)

        myrels.sort()
        outers.sort()
        self.relvars = tuple(myrels)
        self.outers = tuple(outers)
        self.condition = condition
        self.columns = kjGraph(columns)

        self._hashAndCompare = (
            self.__class__.__name__, condition,
            self.relvars, self.outers, self.columns
        )







    def __repr__(self):
        parms=(
            self.condition, list(self.relvars), list(self.outers),
            list(self.columns.items())
        )
        return '%s%r' % (self._hashAndCompare[0], parms)


    def getInnerRVs(self):
        return self.relvars


    def getDB(self):
        db = self.relvars[0].getDB()
        for rv in self.relvars[1:]:
            if rv.getDB() is not db:
                return None
        return db

    def simpleSQL(self):
        condSQL = self.condition.simpleSQL()
        tablenames = [tbl.name for tbl in self.relvars]
        tablenames.sort()
        sql = "SELECT * FROM "+", ".join(tablenames)
        if condSQL:
            sql += " WHERE " + condSQL
        return sql














class _compound(_expr,HashAndCompare):

    def __init__(self,*args):

        operands = {}

        for op in args:
            for item in self._getPromotable(op):
                operands[item]=1

        operands = list(operands)
        operands.sort()
        self.operands = tuple(operands)

        if len(operands)<2:
            raise TypeError,"Compounds require more than one operand"

        self._hashAndCompare = self.__class__.__name__, self.operands


    def __repr__(self):
        return '%s%r' % self._hashAndCompare



















class And(_compound):

    def _getPromotable(self,op):
        return adapt(op,IBooleanExpression).conjuncts()

    def conjuncts(self):
        return self.operands

    def __invert__(self):
        return Or(*tuple([~op for op in self.operands]))

    def simpleSQL(self):
        return ' AND '.join([op.simpleSQL() for op in self.operands])

class Or(_compound):

    def _getPromotable(self,op):
        return adapt(op,IBooleanExpression).disjuncts()

    def disjuncts(self):
        return self.operands

    def __invert__(self):
        return And(*tuple([~op for op in self.operands]))

    def simpleSQL(self):
        return '('+' OR '.join([op.simpleSQL() for op in self.operands])+')'

class Not(_compound):

    def __init__(self,operand):
        self.operands = operand,
        self._hashAndCompare = self.__class__.__name__, self.operands

    def __invert__(self):
        return self.operands[0]

    def simpleSQL(self):
        return 'NOT (%s)' % self.operands[0].simpleSQL()


class Cmp(_expr, HashAndCompare):

    invOps = {'=':'<>', '<':'>=', '>':'<='}
    invOps = kjGraph(invOps.items())
    invOps = invOps + ~invOps

    def __init__(self,arg1,op,arg2):
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2
        self._hashAndCompare = op,arg1,arg2

    def __invert__(self):
        try:
            revOp = self.invOps[self.op]
        except KeyError:
            return Not(self)
        else:
            return self.__class__(self.arg1,revOp,self.arg2)

    def __repr__(self):
        return 'Cmp%r' % (self.arg1,self.op,self.arg2)

    def simpleSQL(self):
        return '%s%s%s' % (self.sqlize(self.arg1),self.op,self.sqlize(self.arg2))

    def sqlize(self,arg):
        v = adapt(arg,IRelationAttribute,None)
        if v is not None:
            return v.simpleSQL()
        return `arg`










