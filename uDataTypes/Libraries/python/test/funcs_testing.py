import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from uncertainty.utypes import *

def check_equals(o, e):
    if hasattr(o, 'uEquals'):
        func = getattr(o, 'uEquals')
        return func(e)
    elif hasattr(o, 'equals'):
        func = getattr(o, 'equals')
        return func(e)
    else:
        return o == e

def err_msg(o, e):
    return 'Obtained: ' + str(o) + ' | Expected: ' + str(e)

def t(o, e):
    assert o.equals(e) if isinstance(o, (ustr, uint, ufloat, ubool, abool, aint, afloat, sbool)) else o == e, err_msg(o, e)

def execute(l, r, e, func, method, op, rev_op, special_op = None):
    t(func(l, r), e)            #   add(l, r)
    if special_op is not None:
        t(l |special_op| r, e)  #   l |AND| r
    if method is not None and is_utype(l): 
        t(method(l, r), e)      #   l.add(r)
    if op is not None and is_utype(l): 
        t(op(l, r),     e)      #   l + r
    elif rev_op is not None and is_utype(r): 
        t(rev_op(r, l), e)      #   5 + r

def negs(l, e):
    t(neg(l),  e)
    t(l.neg(), e)
    t(-l,      e)

def adds(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, add, c.concat if isinstance(l, ustr) or isinstance(r, ustr) else c.add, c.__add__,  c.__radd__)

def subs(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, sub, c.sub, c.__sub__,  c.__rsub__)

def muls(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, mul, c.mul, c.__mul__,  c.__rmul__)

def divs(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, div, c.div, c.__truediv__,  c.__rtruediv__)

def floordivs(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, floordiv, c.floordiv, c.__floordiv__,  c.__rfloordiv__)

def pows(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, pow, c.pow, c.__pow__,  c.__pow__)

def mods(l, r, e):
    c = l.__class__ if is_utype(l) else r.__class__
    execute(l, r, e, mod, c.mod, c.__mod__,  c.__rmod__)

def func_execute(l, e, func, method = None):
    t(func(l), e)    #   sqrt(l)
    if method is not None: 
        t(method(l), e)  #   sqrt(l)

def abss(l, e):
    func_execute(l, e, abs, l.__class__.abs if hasattr(l, 'abs') else None)

def sqrts(l, e):
    func_execute(l, e, sqrt, l.__class__.sqrt if hasattr(l, 'sqrt') else None)

def sins(l, e):
    func_execute(l, e, sin, l.__class__.sin if hasattr(l, 'sin') else None)
    
def coss(l, e):
    func_execute(l, e, cos, l.__class__.cos if hasattr(l, 'cos') else None)

def tans(l, e):
    func_execute(l, e, tan, l.__class__.tan if hasattr(l, 'tan') else None)
    
def atans(l, e):
    func_execute(l, e, atan, l.__class__.atan if hasattr(l, 'atan') else None)

def asins(l, e):
    func_execute(l, e, asin, l.__class__.asin if hasattr(l, 'asin') else None)
    
def acoss(l, e):
    func_execute(l, e, acos, l.__class__.acos if hasattr(l, 'acos') else None)

def inverses(l, e):
    func_execute(l, e, inverse, l.__class__.inverse if hasattr(l, 'inverse') else None)

def floors(l, e):
    func_execute(l, e, floor, l.__class__.floor if hasattr(l, 'floor') else None)

def rounds(l, e):
    func_execute(l, e, round, l.__class__.round if hasattr(l, 'round') else None)

def maxs(l, e):
    func_execute(l, e, max)
    
def mins(l, e):
    func_execute(l, e, min)

def comparison_execute(l, r, e, func, method, op):
    t(func(l, r),   e)  #   lt(l, r)
    t(method(l, r), e)  #   l.lt(r)
    t(op(l, r),     e)  #   l < r

def eqs(l, r, e):
    comparison_execute(l, r, e, eq, l.__class__.eq,  l.__class__.__eq__)

def nes(l, r, e):
    comparison_execute(l, r, e, ne, l.__class__.ne,  l.__class__.__ne__)

def lts(l, r, e):
    comparison_execute(l, r, e, lt, l.__class__.lt,  l.__class__.__lt__)
    
def les(l, r, e):
    comparison_execute(l, r, e, le, l.__class__.le,  l.__class__.__le__)
    
def gts(l, r, e):
    comparison_execute(l, r, e, gt, l.__class__.gt,  l.__class__.__gt__)
    
def ges(l, r, e):
    comparison_execute(l, r, e, ge, l.__class__.ge,  l.__class__.__ge__)
    
def ands(l, r, e):
    execute(l, r, e, AND, l.__class__.AND if hasattr(l, 'AND') else None, l.__class__.__and__, r.__class__.__rand__, AND)

def ors(l, r, e):
    execute(l, r, e, OR, l.__class__.OR if hasattr(l, 'OR') else None, l.__class__.__or__, r.__class__.__ror__, OR)

def xors(l, r, e):
    execute(l, r, e, XOR, l.__class__.XOR if hasattr(l, 'XOR') else None, l.__class__.__xor__, r.__class__.__rxor__, XOR)

def impliess(l, r, e):
    execute(l, r, e, IMPLIES, l.__class__.IMPLIES if hasattr(l, 'IMPLIES') else None, l.__class__.__rshift__, r.__class__.__rrshift__, IMPLIES)

def equivalents(l, r, e):
    execute(l, r, e, EQUIVALENT, l.__class__.EQUIVALENT if hasattr(l, 'EQUIVALENT') else None, None, None, EQUIVALENT)

def equalss(l, r, e):
    execute(l, r, e, EQUALS, l.__class__.EQUALS if hasattr(l, 'EQUALS') else None, l.__class__.__eq__, r.__class__.__eq__, EQUALS)

def distincts(l, r, e):
    execute(l, r, e, DISTINCT, l.__class__.DISTINCT if hasattr(l, 'DISTINCT') else None, l.__class__.__ne__, r.__class__.__ne__, DISTINCT)

def nots(l, e):
    t(NOT(l),  e)
    t(l.NOT(), e)
    t(~l,      e)