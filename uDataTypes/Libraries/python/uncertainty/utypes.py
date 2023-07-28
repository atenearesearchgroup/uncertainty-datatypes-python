from __future__ import annotations

from collections.abc import Iterable

from uncertainty.ubool import ubool
from uncertainty.abool import abool
from uncertainty.sbool import sbool
from uncertainty.result import Result
from uncertainty.unumbers import uint
from uncertainty.unumbers import ufloat
from uncertainty.anumbers import aint
from uncertainty.anumbers import afloat
from uncertainty.ustr import ustr
from uncertainty.uenum import uenum
	
# Operator Class
class infix:
    def __init__(self, function):
        self.function = function
    def __or__(self, other):
        return self.function(other)
    def __ror__(self, other):
        return infix(lambda x, self=self, other=other: self.function(other, x))
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    
# Operator functions
AND = infix(lambda l, r: l.AND(r) if isinstance(l, (ubool, abool, sbool)) else r.AND(l))
OR = infix(lambda l, r: l.OR(r) if isinstance(l, (ubool, abool, sbool)) else r.OR(l))
XOR = infix(lambda l, r: l.XOR(r) if isinstance(l, (ubool, abool, sbool)) else r.XOR(l))
IMPLIES = infix(lambda l, r: l.IMPLIES(r) if isinstance(l, (ubool, abool, sbool)) else r.IMPLIES(l))
EQUIVALENT = infix(lambda l, r: l.EQUIVALENT(r) if isinstance(l, (ubool, abool, sbool)) else r.EQUIVALENT(l))
EQUALS = infix(lambda l, r: l.EQUALS(r) if isinstance(l, (ubool, abool, sbool)) else r.EQUALS(l))
DISTINCT = infix(lambda l, r: l.DISTINCT(r) if isinstance(l, (ubool, abool, sbool)) else r.DISTINCT(l))
NOT = lambda x: x.NOT()

add = infix(lambda l, r: l + r)
concat = infix(lambda l, r: l + r)
sub = infix(lambda l, r: l - r)
mul = infix(lambda l, r: l * r)
div = infix(lambda l, r: l / r)
floordiv = infix(lambda l, r: l // r)
neg = lambda l: -l
pow = infix(lambda l, r: l ** r)
mod = infix(lambda l, r: l % r)

lt = infix(lambda l, r: l < r)
le = infix(lambda l, r: l <= r)
gt = infix(lambda l, r: l > r)
ge = infix(lambda l, r: l >= r)
eq = infix(lambda l, r: l == r)
ne = infix(lambda l, r: l != r)

# Data Functions
def is_utype(obj) -> bool:
    return isinstance(obj, (uint, ufloat, ubool, ustr, uenum, abool, aint, afloat))

def is_ubool(obj) -> bool:
    return isinstance(obj, ubool)

def is_ufloat(obj) -> bool:
    return isinstance(obj, ufloat)

def is_uint(obj) -> bool:
    return isinstance(obj, uint)

def is_unumber(obj) -> bool:
    return isinstance(obj, (uint, ufloat))

def __call_func(obj: uint|ufloat, funcname: str):
    #attrname: str = '_' + str(type(obj).__name__) + '__' + funcname
    if hasattr(obj, funcname):
        func = getattr(obj, funcname)
        return func()
    
    raise NotImplemented

def __check_obj(obj):
    if not is_unumber(obj):
        raise ValueError('Object is not a uint, ufloat or unat')
    
def __check_objs(objs: Iterable):
    for o in objs:
        __check_obj(o)

# abs
def abs(obj: uint|ufloat) -> uint|ufloat:
    if is_unumber(obj):
        return __call_func(obj, abs.__name__)
    else:
        obj.__abs__()

# sqrt
def sqrt(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), sqrt.__name__)

# inverse
def inverse(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj, inverse.__name__)

def __search(rs: Iterable, eval):
    if len(rs) == 0:
        raise ValueError('expected at least 1 argument, got 0')
    if len(rs) == 1:
        return rs[0]
    
    ev = eval(rs[0], rs[1]); rev = eval(rs[1], rs[0])
    best = rs[0] if ev.uncertainty > rev.uncertainty else rs[1]
    for i in range(2, len(rs)):
        r = rs[i]
        ur = r if is_utype(r) else ufloat(r)
        ev = eval(best, ur); rev = eval(ur, best)
        if ev.uncertainty < rev.uncertainty:
            best = r
    
    if is_utype(best):
        return best.copy()
    else:
        return best

# min
def min(*rs):
    return __search(rs, lambda r, min : r < min)

#max
def max(*rs):
    return __search(rs, lambda r, max : r > max)

# sin
def sin(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), sin.__name__)

# cos
def cos(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), cos.__name__)

# tan
def tan(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), tan.__name__)

# atan
def atan(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), atan.__name__)

# asin
def asin(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), asin.__name__)

# acos
def acos(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    return __call_func(obj.toufloat(), acos.__name__)

# floor
def floor(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    if isinstance(obj, uint):
        return obj
    return __call_func(obj.toufloat(), floor.__name__)

# round
def round(obj: uint|ufloat) -> uint|ufloat:
    __check_obj(obj)
    if isinstance(obj, uint):
        return obj
    return __call_func(obj.toufloat(), round.__name__)

def beliefConstraintFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.beliefConstraintFusion(opinions)

def minimumBeliefFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.minimumBeliefFusion(opinions)

def majorityBeliefFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.majorityBeliefFusion(opinions)

def averageBeliefFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.averageBeliefFusion(opinions)

def productOfUncertainties(opinions: Iterable[sbool]) -> sbool:
    return sbool.productOfUncertainties(opinions)

def cumulativeBeliefFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.cumulativeBeliefFusion(opinions)

def epistemicCumulativeBeliefFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.epistemicCumulativeBeliefFusion(opinions)

def weightedBeliefFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.weightedBeliefFusion(opinions)

def consensusAndCompromiseFusion(opinions: Iterable[sbool]) -> sbool:
    return sbool.consensusAndCompromiseFusion(opinions)
