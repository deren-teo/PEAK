from __future__ import generators
import protocols, inspect
from interfaces import *
from strategy import single_best_method, NullTest, DispatchNode
from protocols.advice import as,add_assignment_advisor
from protocols.interfaces import allocate_lock
from types import FunctionType

__all__ = [
    'GenericFunction', 'defmethod', 'when',
]






























class GenericFunction:

    """Extensible multi-dispatch generic function

    Note: this class is *not* threadsafe!  It probably needs to be, though.  :(
    """
    protocols.advise(instancesProvide=[IGenericFunction])

    def __init__(self, args=(), method_combiner=single_best_method):
        self.method_combiner = method_combiner
        self.args_by_name = abn = {}; self.args = args
        for n,p in zip(args,range(len(args))):
            abn[n] = self.__argByNameAndPos(n,p)
        self.__lock = allocate_lock()
        self.clear()

    def clear(self):
        self.__lock.acquire()
        try:
            self._clear()
        finally:
            self.__lock.release()

    def _clear(self):
        self.dirty = False
        self.cases = []
        self.disp_indexes = {}
        self.expr_map = {}
        self.expr_defs = [None,None,None]    # get,args,kw
        self._dispatcher = None


    def addMethod(self,predicate,function):
        for signature in IDispatchPredicate(predicate):
            self[signature] = function

    def testChanged(self):
        self.dirty = True
        self._dispatcher = None


    def _build_dispatcher(self, state=None):
        if state is None:
            self._rebuild_indexes()
            state = self.cases, tuple(self.disp_indexes), {}
        (cases,disp_ids,memo) = state

        key = (tuple(cases), disp_ids)
        if key in memo:
            return memo[key]
        elif not cases:
            node = None
        elif not disp_ids:
            # No more tests possible, so make a leaf node
            node = self.method_combiner(cases)
        else:
            best_id, case_map, remaining_ids = self._best_split(cases,disp_ids)
            if best_id is None:
                # None of our current cases had any meaningful tests on the
                # "best" expression, so don't bother building a dispatch node.
                # Instead, try again with the current expression removed.
                node = self._build_dispatcher((cases, remaining_ids, memo))
            else:
                def dispatch_table():
                    build = self._build_dispatcher
                    for key,subcases in case_map.items():
                        yield key,build((subcases,remaining_ids,memo))
                def reseed(key):
                    self.disp_indexes[best_id][key] = [
                        (s,m) for s,m in self.cases if key in s.get(best_id)
                    ]
                    case_map[key] = [
                        (s,m) for s,m in cases if key in s.get(best_id)
                    ]
                    node[key] = retval = self._build_dispatcher(
                        (case_map[key], remaining_ids, memo)
                    )
                    return retval
                node = DispatchNode(best_id, dispatch_table, reseed)
        memo[key] = node
        return node

    def __call__(self,*__args,**__kw):

        self.__lock.acquire()

        try:
            node = self._dispatcher

            if node is None:
                node = self._dispatcher = self._build_dispatcher()
                if node is None:
                    raise NoApplicableMethods

            def get(expr_id):
                if expr_id in cache:
                    return cache[expr_id]
                f,args = self.expr_defs[expr_id]
                return f(*map(get,args))

            cache = {
                EXPR_GETTER_ID: get, RAW_VARARGS_ID:__args, RAW_KWDARGS_ID:__kw
            }

            while node is not None and type(node) is DispatchNode:

                (expr, dispatch_function) = node.expr_id

                if node.contents:
                    node.build()

                node = dispatch_function(get(expr), node)
        finally:
            cache = None    # allow GC of values computed during dispatch
            self.__lock.release()

        if node is not None:
            return node(*__args,**__kw)
        else:
            raise NoApplicableMethods



    def __argByNameAndPos(self,name,pos):

        def getArg(args,kw):
            if len(args)<=pos:
                return kw[name]
            else:
                return args[pos]

        return getArg, (RAW_VARARGS_ID,RAW_KWDARGS_ID)


    def argByName(self,name):
        return self.args_by_name[name]

    def argByPos(self,pos):
        return self.args_by_name[self.args[pos]]


    def _rebuild_indexes(self):
        if self.dirty:
            cases = self.cases
            self._clear()
            map(self._addCase, cases)


    [as(classmethod)]
    def from_function(klass,func):
        # XXX nested args, var, kw, docstring...
        return klass(inspect.getargspec(func)[0])












    def __setitem__(self,signature,method):
        """Update indexes to include 'signature'->'method'"""
        from predicates import Signature

        self.__lock.acquire()
        try:
            signature = Signature(
                [(self._dispatch_id(expr,test),test)
                    for expr,test in ISignature(signature).items()
                        if test is not NullTest
                ]
            )
            self._addCase((signature, method))
        finally:
            self.__lock.release()


    def _addCase(self,case):
        (signature,method) = case

        for disp_id, caselists in self.disp_indexes.items():

            test = signature.get(disp_id)

            for key in test.seeds(caselists):
                if key not in caselists:
                    # Add in cases that didn't test this key  :(
                    caselists[key] = [
                        (s2,m2) for s2,m2 in self.cases
                            if key in s2.get(disp_id)
                    ]

            for key,lst in caselists.items():
                if key in test:
                    lst.append(case)

        self.cases.append(case)
        self._dispatcher = None



    def _best_split(self, cases, disp_ids):

        """Return best (disp_id,method_map,remaining_ids) for current subtree"""

        best_id = None
        best_map = None
        best_spread = None
        remaining_ids = list(disp_ids)
        cases = dict([(case,1) for case in cases])
        is_active = cases.has_key
        active_cases = len(cases)

        for disp_id in disp_ids:
            # XXX may need filtering for required ordering between exprs
            # XXX analyze cost to compute expression?

            casemap = {}
            total_cases = 0
            for key,caselist in self.disp_indexes[disp_id].items():
                caselist = filter(is_active,caselist)
                casemap[key] = caselist
                total_cases += len(caselist)

            if total_cases == active_cases * len(casemap):
                # None of the index keys for this expression eliminate any
                # cases, so this expression isn't needed for dispatching
                remaining_ids.remove(disp_id)
                continue

            spread = float(total_cases) / len(casemap)
            if spread < best_spread or best_spread is None:
                best_spread = spread
                best_id = disp_id
                best_map = casemap

        if best_id is not None:
            remaining_ids.remove(best_id)

        return best_id, best_map, tuple(remaining_ids)


    def _dispatch_id(self,(expr,disp_func),test):
        """Replace expr/test with a local key"""

        test.subscribe(self)
        expr = self.getExpressionId(expr)
        disp = expr, test.dispatch_function
        self.disp_indexes.setdefault(disp,{})
        return expr


    def getExpressionId(self,expr):
        """Replace 'expr' with a local expression ID number"""

        # XXX this isn't threadsafe if not called from 'asFuncAndIds'

        try:
            return self.expr_map[expr]

        except KeyError:
            expr_def = IDispatchableExpression(expr).asFuncAndIds(self)

            try:
                return self.expr_map[expr_def]
            except KeyError:
                expr_id = len(self.expr_defs)
                self.expr_map[expr] = self.expr_map[expr_def] = expr_id
                self.expr_defs.append(expr_def)
                return expr_id


    def parse(self,expr_string,local_dict,global_dict):
        self.__lock.acquire()
        try:
            from predicates import TestBuilder
            from ast_builder import parse_expr
            builder=TestBuilder(self.args,local_dict,global_dict,__builtins__)
            return parse_expr(expr_string,builder)
        finally:
            self.__lock.release()


def defmethod(gf,cond,func,local_dict=None,global_dict=None):
    """Add a method 'func' to 'gf' using 'cond', returning a GF"""

    def dm_simple(gf,cond,func,local_dict=None,global_dict=None):
        """Add a method to an existing GF, using a predicate object"""
        gf = IGenericFunction(gf)
        gf.addMethod(cond,func)
        return gf
    
    
    def dm_string(gf,cond,func,local_dict=None,global_dict=None):
        """Add a method to an existing GF, using a string condition"""
    
        if global_dict is None:
            global_dict = getattr(func,'func_globals',globals())
        if local_dict is None:
            local_dict = global_dict
    
        cond = gf.parse(cond,local_dict,global_dict)
        return defmethod(gf,cond,func)

    def dm_func(gf,cond,func,local_dict=None,global_dict=None):
        """Create a new generic function, using function to get args info"""
        return defmethod(
           GenericFunction.from_function(func),cond,func,local_dict,global_dict
        )
    
    global defmethod    
    defmethod = GenericFunction.from_function(dm_simple)
    
    dm_simple(defmethod,
        defmethod.parse(
            "gf in IGenericFunction and cond in IDispatchPredicate",
            locals(),globals()),
        dm_simple)
    
    dm_string(defmethod, "gf in IGenericFunction and cond in str", dm_string)
    dm_string(defmethod, "gf is None and func in FunctionType", dm_func)
    
    return defmethod(gf,cond,func,local_dict,global_dict)

def when(cond):
    """Add the following function to a generic function, w/'cond' as guard"""
    def callback(frm,name,value):
        frm.f_locals[name] = defmethod(
            frm.f_locals.get(name), cond, value, frm.f_locals, frm.f_globals
        )
    add_assignment_advisor(callback)
    
    
































