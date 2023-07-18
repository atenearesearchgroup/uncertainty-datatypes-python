from __future__ import annotations

from collections.abc import Iterable

from udatatypes.ubool import ubool
from udatatypes.result import Result
from udatatypes.unumbers import uint
from udatatypes.unumbers import ufloat
	
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
AND = infix(lambda l, r: l.AND(r) if isinstance(l, ubool) else r.AND(l))
OR = infix(lambda l, r: l.OR(r) if isinstance(l, ubool) else r.OR(l))
XOR = infix(lambda l, r: l.XOR(r) if isinstance(l, ubool) else r.XOR(l))
IMPLIES = infix(lambda l, r: l.IMPLIES(r) if isinstance(l, ubool) else r.IMPLIES(l))
EQUIVALENT = infix(lambda l, r: l.EQUIVALENT(r) if isinstance(l, ubool) else r.EQUIVALENT(l))
EQUALS = infix(lambda l, r: l.EQUALS(r) if isinstance(l, ubool) else r.EQUALS(l))
DISTINCT = infix(lambda l, r: l.DISTINCT(r) if isinstance(l, ubool) else r.DISTINCT(l))
NOT = lambda x: x.NOT()

add = infix(lambda l, r: l + r)
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
    return isinstance(obj, (uint, ufloat, ubool))

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
    __check_obj(obj)
    return __call_func(obj, abs.__name__)

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
        raise ValueError('max expected at least 1 argument, got 0')
    
    best = rs[0]
    for r in rs:
        if eval(r, best):
            best = r
    
    if is_utype(best):
        return best.copy()
    else:
        best

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
