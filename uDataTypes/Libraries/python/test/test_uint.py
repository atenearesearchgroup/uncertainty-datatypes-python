import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from udatatypes.utypes import *
from funcs_testing import *

def execute(l, r, e, func, method, op, rev_op):
    t(func(l, r), e)            #   add(l, r)
    if isinstance(l, uint): 
        t(method(l, r), e)      #   l.add(r)
        t(op(l, r),     e)      #   l + r
    elif isinstance(r, uint): 
        t(rev_op(l, r), e)      #   5 + r

def negs(l, e):
    t(neg(l),  e)
    t(l.neg(), e)
    t(-l,      e)

def adds(l, r, e):
    execute(l, r, e, add, uint.add, uint.__add__,  uint.__radd__)

def subs(l, r, e):
    execute(l, r, e, sub, uint.sub, uint.__sub__,  uint.__rsub__)

def muls(l, r, e):
    execute(l, r, e, mul, uint.mul, uint.__mul__,  uint.__rmul__)

def divs(l, r, e):
    execute(l, r, e, div, uint.div, uint.__truediv__,  uint.__rtruediv__)

def floordivs(l, r, e):
    execute(l, r, e, floordiv, uint.floordiv, uint.__floordiv__,  uint.__rfloordiv__)

def pows(l, r, e):
    execute(l, r, e, pow, uint.power, uint.__pow__,  uint.__pow__)

def mods(l, r, e):
    execute(l, r, e, mod, uint.mod, uint.__mod__,  uint.__rmod__)

def func_execute(l, e, func, method = None):
    t(func(l,), e)    #   sqrt(l)
    if method is not None:
        t(method(l,), e)  #   l.sqrt())

def sqrts(l, e):
    func_execute(l, e, sqrt)

def sins(l, e):
    func_execute(l, e, sin)

def coss(l, e):
    func_execute(l, e, coss)

def coss(l, e):
    func_execute(l, e, cos)

def tans(l, e):
    func_execute(l, e, tan)
    
def atans(l, e):
    func_execute(l, e, atan)

def asins(l, e):
    func_execute(l, e, asin)
    
def acoss(l, e):
    func_execute(l, e, acos)

def inverses(l, e):
    func_execute(l, e, inverse)

def floors(l, e):
    func_execute(l, e, floor)

def rounds(l, e):
    func_execute(l, e, round)

def mods(l, r, e):
    execute(l, r, e, mod, uint.mod, uint.__mod__,  uint.__rmod__)

def comparison_execute(l, r, e, func, method, op):
    t(func(l, r),   e)  #   lt(l, r)
    t(method(l, r), e)  #   l.lt(r)
    t(op(l, r),     e)  #   l < r

def eqs(l, r, e):
    comparison_execute(l, r, e, eq, uint.eq,  uint.__eq__)

def nes(l, r, e):
    comparison_execute(l, r, e, ne, uint.ne,  uint.__ne__)

def lts(l, r, e):
    comparison_execute(l, r, e, lt, uint.lt,  uint.__lt__)
    
def les(l, r, e):
    comparison_execute(l, r, e, le, uint.le,  uint.__le__)
    
def gts(l, r, e):
    comparison_execute(l, r, e, gt, uint.gt,  uint.__gt__)
    
def ges(l, r, e):
    comparison_execute(l, r, e, ge, uint.ge,  uint.__ge__)

class uintTest(unittest.TestCase):
    
    def setUp(self):
        self.uia = uint(-4, 3.0)
        self.uib = uint(2, 4.0)
        self.uic = uint(23, 5.3)
        self.ufa = ufloat(-4.0, 3.0)
        self.ufb = ufloat(2.0, 4.0)
        self.ia = -4
        self.ib = 2
        self.fa = -24.72
        self.fb = 12.56

    def test_init(self):
        t(uint(20, 1.7),   uint(20, 1.7))
        t(uint(23, 1.7),   uint(23, 1.7))
        t(uint(25, 1.7),   uint(25, 1.7))

        t(uint('20', 1.7), uint(20, 1.7))
        t(uint('25', 1.7), uint(25, 1.7))
        
        t(uint(20, 1),     uint(20, 1.0))
        t(uint('25', 1),   uint(25, 1.0))

        t(uint('20', '1'), uint(20, 1.0))
        t(uint('25', '1'), uint(25, 1.0))

    '''
        Operators
    '''
    def test_add(self):
        ''' add + uint '''
        adds(self.uia, self.uia, uint(-8, 4.243))
        adds(self.uia, self.uib, uint(-2, 5.000))
        adds(self.uib, self.uib, uint( 4, 5.657))
        adds(self.uib, self.uia, uint(-2, 5.000))
    def test_add_uint(self):
        ''' add + uint '''
        adds(self.uia, self.ufa, uint(-8, 4.243))
        adds(self.uia, self.ufb, uint(-2, 5.000))
        adds(self.uib, self.ufa, uint(-2, 5.000))
        adds(self.uib, self.ufb, uint( 4, 5.657))

    def test_add_int(self):
        ''' add + int '''
        adds(self.uia, self.ia, uint(-8, 3.000))
        adds(self.uia, self.ib, uint(-2, 3.000))
        adds(self.uib, self.ia, uint(-2, 4.000))
        adds(self.uib, self.ib, uint( 4, 4.000))

    def test_add_float(self):
        ''' add + float '''
        adds(self.uia, self.fa, ufloat(-28.720, 3.000))
        adds(self.uia, self.fb, ufloat(8.560, 3.000))
        adds(self.uib, self.fa, ufloat(-22.720, 4.000))
        adds(self.uib, self.fb, ufloat(14.560, 4.000))

    def test_sub(self):
        ''' sub - uint '''
        subs(self.uia, self.uia, uint( 0, 0.000))
        subs(self.uia, self.uib, uint(-6, 5.000))
        subs(self.uib, self.uib, uint( 0, 0.000))
        subs(self.uib, self.uia, uint( 6, 5.000))

    def test_sub_uint(self):
        ''' sub - uint '''
        subs(self.uia, self.ufa, uint( 0, 4.243))
        subs(self.uia, self.ufb, uint(-6, 5.000))
        subs(self.uib, self.ufa, uint( 6, 5.000))
        subs(self.uib, self.ufb, uint( 0, 5.657))

    def test_sub_int(self):
        ''' sub - int '''
        subs(self.uia, self.ia, uint( 0, 3.000))
        subs(self.uia, self.ib, uint(-6, 3.000))
        subs(self.uib, self.ia, uint( 6, 4.000))
        subs(self.uib, self.ib, uint( 0, 4.000))

    def test_sub_float(self):
        ''' sub - float '''
        subs(self.uia, self.fa, ufloat( 20.720, 3.000))
        subs(self.uia, self.fb, ufloat(-16.560, 3.000))
        subs(self.uib, self.fa, ufloat( 26.720, 4.000))
        subs(self.uib, self.fb, ufloat(-10.560, 4.000))

    def test_mul(self):
        ''' mul * uint '''
        muls(self.uia, self.uia, uint(16, 16.971))
        muls(self.uia, self.uib, uint(-8, 17.088))
        muls(self.uib, self.uib, uint( 4, 11.314))
        muls(self.uib, self.uia, uint(-8, 17.088))
        
    def test_mul_uint(self):
        ''' mul * uint '''
        muls(self.uia, self.ufa, uint(16, 16.971))
        muls(self.uia, self.ufb, uint(-8, 17.088))
        muls(self.uib, self.ufa, uint(-8, 17.088))
        muls(self.uib, self.ufb, uint( 4, 11.314))

    def test_mul_int(self):
        ''' mul * int '''
        muls(self.uia, self.ia, uint(16, 12.000))
        muls(self.uia, self.ib, uint(-8,  6.000))
        muls(self.uib, self.ia, uint(-8, 16.000))
        muls(self.uib, self.ib, uint( 4,  8.000))

    def test_mul_float(self):
        ''' mul * float '''
        muls(self.uia, self.fa, ufloat( 98.880, 74.160))
        muls(self.uia, self.fb, ufloat(-50.240, 37.680))
        muls(self.uib, self.fa, ufloat(-49.440, 98.880))
        muls(self.uib, self.fb, ufloat( 25.120, 50.240))

    def test_div(self):
        ''' div / uint '''
        divs(self.uia, self.uia, ufloat( 1.000, 1.677))
        divs(self.uia, self.uib, ufloat(-2.000, 4.528))
        divs(self.uib, self.uib, ufloat( 1.000, 3.464))
        divs(self.uib, self.uia, ufloat(-0.500, 2.035))
        
    def test_div_uint(self):
        ''' div / uint '''
        divs(self.uia, self.ufa, ufloat( 1.000, 1.677))
        divs(self.uia, self.ufb, ufloat(-2.000, 4.528))
        divs(self.uib, self.ufa, ufloat(-0.500, 2.035))
        divs(self.uib, self.ufb, ufloat( 1.000, 3.464))

    def test_div_int(self):
        ''' div / int '''
        divs(self.uia, self.ia, ufloat( 1.000, 0.750))
        divs(self.uia, self.ib, ufloat(-2.000, 1.500))
        divs(self.uib, self.ia, ufloat(-0.500, 1.000))
        divs(self.uib, self.ib, ufloat( 1.000, 2.000))

    def test_div_float(self):
        ''' div / float '''
        divs(self.uia, self.fa, ufloat(0.162, 0.121))
        divs(self.uia, self.fb, ufloat(-0.318, 0.239))
        divs(self.uib, self.fa, ufloat(-0.081, 0.162))
        divs(self.uib, self.fb, ufloat(0.159, 0.318))
    def test_floordiv(self):
        ''' floor div // uint '''
        floordivs(self.uia, self.uia, uint( 1, 0.000))
        floordivs(self.uia, self.uib, uint(-2, 4.528))
        floordivs(self.uib, self.uib, uint( 1, 0.000))
        floordivs(self.uib, self.uia, uint(-1, 2.035))
        
    def test_floordiv_uint(self):
        ''' floor div // uint '''
        floordivs(self.uia, self.ufa, uint( 1, 1.677))
        floordivs(self.uia, self.ufb, uint(-2, 4.528))
        floordivs(self.uib, self.ufa, uint(-1, 2.035))
        floordivs(self.uib, self.ufb, uint( 1, 3.464))

    def test_floordiv_int(self):
        ''' floor div // int '''
        floordivs(self.uia, self.ia, uint( 1, 0.750))
        floordivs(self.uia, self.ib, uint(-2, 1.500))
        floordivs(self.uib, self.ia, uint(-1, 1.000))
        floordivs(self.uib, self.ib, uint( 1, 2.000))

    def test_floordiv_float(self):
        ''' floor div // float '''
        floordivs(self.uia, self.fa, uint( 0, 0.121))
        floordivs(self.uia, self.fb, uint(-1, 0.239))
        floordivs(self.uib, self.fa, uint(-1, 0.162))
        floordivs(self.uib, self.fb, uint( 0, 0.318))
        
    def test_neg(self):
        ''' neg - '''
        negs(self.uia, uint( 4, 3.000))
        negs(self.uib, uint(-2, 4.000))
        negs(self.ufa, uint( 4, 3.000))
        negs(self.ufb, uint(-2, 4.000))     

    def test_power(self):
        ''' power ** '''
        pows(self.uia, 2, uint(   16,   24.000))
        pows(self.uia, 3, uint(  -64,  144.000))
        pows(self.uia, 5, uint(-1024, 3840.000))
        pows(self.uib, 2.50, ufloat( 5.657,  28.284))
        pows(self.uib, 3.25, ufloat( 9.514,  61.839))
        pows(self.uib, 5.03, ufloat(32.672, 328.684))

    '''
        Functions
    '''

    def test_sqrt(self):
        ''' sqrt '''
        sqrts(self.uib, ufloat(1.414, 1.414))
        sqrts(self.uic, ufloat(4.796, 0.553))

    def test_sin(self):
        ''' sin '''
        sins(self.uib,  ufloat(0.909, 1.665))
        sins(self.uic, ufloat(-0.846, 2.824))

    def test_cos(self):
        ''' cos '''
        coss(self.uib, ufloat(-0.416, 3.637))
        coss(self.uic, ufloat(-0.533, 4.485))

    def test_tan(self):
        ''' tan '''
        tans(self.uib, ufloat(-2.185, 19.271))
        tans(self.uic, ufloat( 1.588, 13.916))

    def test_atan(self):
        ''' atan '''
        atans(self.uib, ufloat(1.107, 0.800))
        atans(self.uic, ufloat(1.527, 0.010))

    def test_asin(self):
        ''' asin '''
        asins(sin(self.uib), ufloat(1.142, 4.000))
        asins(sin(self.uic), ufloat(-1.009, 5.300))
        
    def test_acos(self):
        ''' acos '''
        acoss(cos(self.uib), ufloat(2, 4.000))
        acoss(cos(self.uic), ufloat(2.133, 5.300))

    def test_inverse(self):
        ''' inverse '''
        inverses(self.uia, ufloat(-0.250, 0.188))
        inverses(self.uib, ufloat(0.500, 1.000))
        inverses(self.uic, ufloat(0.043, 0.010))

    def test_floor(self):
        ''' floor '''
        floors(mul(self.uia, self.fa), uint( 98, 74.160))
        floors(mul(self.uia, self.fb), uint(-51, 37.680))
        floors(mul(self.uib, self.fa), uint(-50, 98.880))
        floors(mul(self.uib, self.fb), uint( 25, 50.240))

    def test_round(self):
        ''' round '''
        rounds(mul(self.uia, self.fa), uint( 99, 74.160))
        rounds(mul(self.uia, self.fb), uint(-50, 37.680))
        rounds(mul(self.uib, self.fa), uint(-49, 98.880))
        rounds(mul(self.uib, self.fb), uint( 25, 50.240))

    def test_max(self):
        ''' max '''

    def test_min(self):
        ''' min '''

    '''
        Comparison Operators
    '''
    def test_eq(self):
        ''' eq == '''
        eqs(self.uia, self.uia, ubool(1.000))
        eqs(self.uia, self.uib, ubool(0.385))
        eqs(self.uia, self.uic, ubool(0.001))
        
    def test_ne(self):
        ''' ne != '''
        nes(self.uia, self.uia, ubool(0.000))
        nes(self.uia, self.uib, ubool(0.615))
        nes(self.uia, self.uic, ubool(0.999))

    def test_lt(self):
        ''' lt < '''
        lts(self.uia,  self.uia, ubool(0.000))
        lts(self.uia,  self.uib, ubool(0.615))
        lts(self.uia,  self.uic, ubool(0.999))
        
    def test_le(self):
        ''' le <= '''
        les(self.uia, self.uia, ubool(1.000))
        les(self.uia, self.uib, ubool(1.000))
        les(self.uia, self.uic, ubool(1.000))

    def test_gt(self):
        ''' gt > '''
        gts(self.uia,  self.uia, ubool(0.000))
        gts(self.uia,  self.uib, ubool(0.000))
        gts(self.uia,  self.uic, ubool(0.000))

    def test_ge(self):
        ''' ge >= '''
        ges(self.uia, self.uia, ubool(1.000))
        ges(self.uia, self.uib, ubool(0.385))
        ges(self.uia, self.uic, ubool(0.001))
    
if __name__ == '__main__':
    unittest.main()