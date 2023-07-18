import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from udatatypes.utypes import *
from funcs_testing import *

def execute(l, r, e, func, method, op, rev_op):
    t(func(l, r), e)            #   add(l, r)
    if isinstance(l, ufloat): 
        t(method(l, r), e)      #   l.add(r)
        t(op(l, r),     e)      #   l + r
    elif isinstance(r, ufloat): 
        t(rev_op(l, r), e)      #   5 + r

def negs(l, e):
    t(neg(l),  e)
    t(l.neg(), e)
    t(-l,      e)

def adds(l, r, e):
    execute(l, r, e, add, ufloat.add, ufloat.__add__,  ufloat.__radd__)

def subs(l, r, e):
    execute(l, r, e, sub, ufloat.sub, ufloat.__sub__,  ufloat.__rsub__)

def muls(l, r, e):
    execute(l, r, e, mul, ufloat.mul, ufloat.__mul__,  ufloat.__rmul__)

def divs(l, r, e):
    execute(l, r, e, div, ufloat.div, ufloat.__truediv__,  ufloat.__rtruediv__)

def floordivs(l, r, e):
    execute(l, r, e, floordiv, ufloat.floordiv, ufloat.__floordiv__,  ufloat.__rfloordiv__)

def pows(l, r, e):
    execute(l, r, e, pow, ufloat.power, ufloat.__pow__,  ufloat.__pow__)

def func_execute(l, e, func, method):
    t(func(l,), e)    #   sqrt(l)
    t(method(l,), e)  #   sqrt(l)

def sqrts(l, e):
    func_execute(l, e, sqrt, ufloat.sqrt)

def sins(l, e):
    func_execute(l, e, sin, ufloat.sin)

def coss(l, e):
    func_execute(l, e, coss, ufloat.coss)

def sins(l, e):
    func_execute(l, e, sin, ufloat.sin)
    
def coss(l, e):
    func_execute(l, e, cos, ufloat.cos)

def tans(l, e):
    func_execute(l, e, tan, ufloat.tan)
    
def atans(l, e):
    func_execute(l, e, atan, ufloat.atan)

def asins(l, e):
    func_execute(l, e, asin, ufloat.asin)
    
def acoss(l, e):
    func_execute(l, e, acos, ufloat.acos)

def inverses(l, e):
    func_execute(l, e, inverse, ufloat.inverse)

def floors(l, e):
    func_execute(l, e, floor, ufloat.floor)

def rounds(l, e):
    func_execute(l, e, round, ufloat.round)

def comparison_execute(l, r, e, func, method, op):
    t(func(l, r),   e)  #   lt(l, r)
    t(method(l, r), e)  #   l.lt(r)
    t(op(l, r),     e)  #   l < r

def eqs(l, r, e):
    comparison_execute(l, r, e, eq, ufloat.eq,  ufloat.__eq__)

def nes(l, r, e):
    comparison_execute(l, r, e, ne, ufloat.ne,  ufloat.__ne__)

def lts(l, r, e):
    comparison_execute(l, r, e, lt, ufloat.lt,  ufloat.__lt__)
    
def les(l, r, e):
    comparison_execute(l, r, e, le, ufloat.le,  ufloat.__le__)
    
def gts(l, r, e):
    comparison_execute(l, r, e, gt, ufloat.gt,  ufloat.__gt__)
    
def ges(l, r, e):
    comparison_execute(l, r, e, ge, ufloat.ge,  ufloat.__ge__)

class ufloatTest(unittest.TestCase):
    
    def setUp(self):
        self.ufa = ufloat(-4.0, 3.0)
        self.ufb = ufloat(2.0, 4.0)
        self.ufc = ufloat(23.0, 5.3)
        self.uia = uint(-4, 3.0)
        self.uib = uint(2, 4.0)
        self.ia = -4
        self.ib = 2
        self.fa = -24.72
        self.fb = 12.56

    def test_init(self):
        t(ufloat(20.0, 1.7), ufloat(20.0, 1.7))
        t(ufloat(20, 1.7),   ufloat(20.0, 1.7))
        t(ufloat(23.4, 1.7), ufloat(23.4, 1.7))
        t(ufloat(25, 1.7),   ufloat(25.0, 1.7))

        t(ufloat('20.0', 1.7), ufloat(20.0, 1.7))
        t(ufloat('20', 1.7),   ufloat(20.0, 1.7))
        t(ufloat('23.4', 1.7), ufloat(23.4, 1.7))
        t(ufloat('25', 1.7),   ufloat(25.0, 1.7))
        
        t(ufloat(20.0, 1.7),   ufloat(20.0, 1.7))
        t(ufloat(20, 1),       ufloat(20.0, 1.0))
        t(ufloat('23.4', 1.7), ufloat(23.4, 1.7))
        t(ufloat('25', 1),     ufloat(25.0, 1.0))

        t(ufloat('20.0', '1.7'), ufloat(20.0, 1.7))
        t(ufloat('20', '1'),     ufloat(20.0, 1.0))
        t(ufloat('23.4', '1.7'), ufloat(23.4, 1.7))
        t(ufloat('25', '1'),     ufloat(25.0, 1.0))

    '''
        Operators
    '''
    def test_add(self):
        ''' add + ufloat '''
        adds(self.ufa, self.ufa, ufloat(-8.000, 4.243))
        adds(self.ufa, self.ufb, ufloat(-2.000, 5.000))
        adds(self.ufb, self.ufb, ufloat( 4.000, 5.657))
        adds(self.ufb, self.ufa, ufloat(-2.000, 5.000))

    def test_add_uint(self):
        ''' add + uint '''
        adds(self.ufa, self.uia, ufloat(-8.000, 4.243))
        adds(self.ufa, self.uib, ufloat(-2.000, 5.000))
        adds(self.ufb, self.uia, ufloat(-2.000, 5.000))
        adds(self.ufb, self.uib, ufloat( 4.000, 5.657))

    def test_add_int(self):
        ''' add + int '''
        adds(self.ufa, self.ia, ufloat(-8.000, 3.000))
        adds(self.ufa, self.ib, ufloat(-2.000, 3.000))
        adds(self.ufb, self.ia, ufloat(-2.000, 4.000))
        adds(self.ufb, self.ib, ufloat( 4.000, 4.000))

    def test_add_float(self):
        ''' add + float '''
        adds(self.ufa, self.fa, ufloat(-28.720, 3.000))
        adds(self.ufa, self.fb, ufloat(8.560, 3.000))
        adds(self.ufb, self.fa, ufloat(-22.720, 4.000))
        adds(self.ufb, self.fb, ufloat(14.560, 4.000))

    def test_sub(self):
        ''' sub - ufloat '''
        subs(self.ufa, self.ufa, ufloat( 0.000, 0.000))
        subs(self.ufa, self.ufb, ufloat(-6.000, 5.000))
        subs(self.ufb, self.ufb, ufloat( 0.000, 0.000))
        subs(self.ufb, self.ufa, ufloat( 6.000, 5.000))

    def test_sub_uint(self):
        ''' sub - uint '''
        subs(self.ufa, self.uia, ufloat( 0.000, 4.243))
        subs(self.ufa, self.uib, ufloat(-6.000, 5.000))
        subs(self.ufb, self.uia, ufloat( 6.000, 5.000))
        subs(self.ufb, self.uib, ufloat( 0.000, 5.657))

    def test_sub_int(self):
        ''' sub - int '''
        subs(self.ufa, self.ia, ufloat( 0.000, 3.000))
        subs(self.ufa, self.ib, ufloat(-6.000, 3.000))
        subs(self.ufb, self.ia, ufloat( 6.000, 4.000))
        subs(self.ufb, self.ib, ufloat( 0.000, 4.000))

    def test_sub_float(self):
        ''' sub - float '''
        subs(self.ufa, self.fa, ufloat( 20.720, 3.000))
        subs(self.ufa, self.fb, ufloat(-16.560, 3.000))
        subs(self.ufb, self.fa, ufloat( 26.720, 4.000))
        subs(self.ufb, self.fb, ufloat(-10.560, 4.000))
        
    def test_mul(self):
        ''' mul * ufloat '''
        muls(self.ufa, self.ufa, ufloat(16.000, 16.971))
        muls(self.ufa, self.ufb, ufloat(-8.000, 17.088))
        muls(self.ufb, self.ufb, ufloat( 4.000, 11.314))
        muls(self.ufb, self.ufa, ufloat(-8.000, 17.088))
        
    def test_mul_uint(self):
        ''' mul * uint '''
        muls(self.ufa, self.uia, ufloat(16.000, 16.971))
        muls(self.ufa, self.uib, ufloat(-8.000, 17.088))
        muls(self.ufb, self.uia, ufloat(-8.000, 17.088))
        muls(self.ufb, self.uib, ufloat( 4.000, 11.314))

    def test_mul_int(self):
        ''' mul * int '''
        muls(self.ufa, self.ia, ufloat(16.000, 12.000))
        muls(self.ufa, self.ib, ufloat(-8.000,  6.000))
        muls(self.ufb, self.ia, ufloat(-8.000, 16.000))
        muls(self.ufb, self.ib, ufloat( 4.000,  8.000))

    def test_mul_float(self):
        ''' mul * float '''
        muls(self.ufa, self.fa, ufloat( 98.880, 74.160))
        muls(self.ufa, self.fb, ufloat(-50.240, 37.680))
        muls(self.ufb, self.fa, ufloat(-49.440, 98.880))
        muls(self.ufb, self.fb, ufloat( 25.120, 50.240))

    def test_div(self):
        ''' div / ufloat '''
        divs(self.ufa, self.ufa, ufloat( 1.000, 0.000))
        divs(self.ufa, self.ufb, ufloat(-2.000, 4.528))
        divs(self.ufb, self.ufb, ufloat( 1.000, 0.000))
        divs(self.ufb, self.ufa, ufloat(-0.500, 2.035))
        
    def test_div_uint(self):
        ''' div / uint '''
        divs(self.ufa, self.uia, ufloat( 1.000, 1.677))
        divs(self.ufa, self.uib, ufloat(-2.000, 4.528))
        divs(self.ufb, self.uia, ufloat(-0.500, 2.035))
        divs(self.ufb, self.uib, ufloat( 1.000, 3.464))

    def test_div_int(self):
        ''' div / int '''
        divs(self.ufa, self.ia, ufloat( 1.000, 0.750))
        divs(self.ufa, self.ib, ufloat(-2.000, 1.500))
        divs(self.ufb, self.ia, ufloat(-0.500, 1.000))
        divs(self.ufb, self.ib, ufloat( 1.000, 2.000))

    def test_div_float(self):
        ''' div / float '''
        divs(self.ufa, self.fa, ufloat(0.162, 0.121))
        divs(self.ufa, self.fb, ufloat(-0.318, 0.239))
        divs(self.ufb, self.fa, ufloat(-0.081, 0.162))
        divs(self.ufb, self.fb, ufloat(0.159, 0.318))

    def test_floordiv(self):
        ''' floor div // ufloat '''
        floordivs(self.ufa, self.ufa, ufloat( 1.000, 0.000))
        floordivs(self.ufa, self.ufb, ufloat(-2.000, 4.528))
        floordivs(self.ufb, self.ufb, ufloat( 1.000, 0.000))
        floordivs(self.ufb, self.ufa, ufloat(-1.000, 2.035))
        
    def test_floordiv_uint(self):
        ''' floor div // uint '''
        floordivs(self.ufa, self.uia, ufloat( 1.000, 1.677))
        floordivs(self.ufa, self.uib, ufloat(-2.000, 4.528))
        floordivs(self.ufb, self.uia, ufloat(-1.000, 2.035))
        floordivs(self.ufb, self.uib, ufloat( 1.000, 3.464))

    def test_floordiv_int(self):
        ''' floor div // int '''
        floordivs(self.ufa, self.ia, ufloat( 1.000, 0.750))
        floordivs(self.ufa, self.ib, ufloat(-2.000, 1.500))
        floordivs(self.ufb, self.ia, ufloat(-1.000, 1.000))
        floordivs(self.ufb, self.ib, ufloat( 1.000, 2.000))

    def test_floordiv_float(self):
        ''' floor div // float '''
        floordivs(self.ufa, self.fa, ufloat(0.000, 0.121))
        floordivs(self.ufa, self.fb, ufloat(-1.000, 0.239))
        floordivs(self.ufb, self.fa, ufloat(-1.000, 0.162))
        floordivs(self.ufb, self.fb, ufloat(0.000, 0.318))

    def test_neg(self):
        ''' neg - '''
        negs(self.ufa, ufloat( 4.000, 3.000))
        negs(self.ufb, ufloat(-2.000, 4.000))
        negs(self.uia, ufloat( 4.000, 3.000))
        negs(self.uib, ufloat(-2.000, 4.000))     

    def test_power(self):
        ''' power ** '''
        pows(self.ufa, 2, ufloat(   16.000,   24.000))
        pows(self.ufa, 3, ufloat(  -64.000,  144.000))
        pows(self.ufa, 5, ufloat(-1024.000, 3840.000))
        pows(self.ufb, 2.50, ufloat( 5.657,  28.284))
        pows(self.ufb, 3.25, ufloat( 9.514,  61.839))
        pows(self.ufb, 5.03, ufloat(32.672, 328.684))


    '''
        Functions
    '''

    def test_sqrt(self):
        ''' sqrt '''
        sqrts(self.ufb, ufloat(1.414, 1.414))
        sqrts(self.ufc, ufloat(4.796, 0.553))

    def test_sin(self):
        ''' sin '''
        sins(self.ufb,  ufloat(0.909, 1.665))
        sins(self.ufc, ufloat(-0.846, 2.824))

    def test_cos(self):
        ''' cos '''
        coss(self.ufb, ufloat(-0.416, 3.637))
        coss(self.ufc, ufloat(-0.533, 4.485))

    def test_tan(self):
        ''' tan '''
        tans(self.ufb, ufloat(-2.185, 19.271))
        tans(self.ufc, ufloat( 1.588, 13.916))

    def test_atan(self):
        ''' atan '''
        atans(self.ufb, ufloat(1.107, 0.800))
        atans(self.ufc, ufloat(1.527, 0.010))

    def test_asin(self):
        ''' asin '''
        asins(sin(self.ufb), ufloat(1.142, 4.000))
        asins(sin(self.ufc), ufloat(-1.009, 5.300))
        
    def test_acos(self):
        ''' acos '''
        acoss(cos(self.ufb), ufloat(2.000, 4.000))
        acoss(cos(self.ufc), ufloat(2.133, 5.300))

    def test_inverse(self):
        ''' inverse '''
        inverses(self.ufa, ufloat(-0.250, 0.188))
        inverses(self.ufb, ufloat(0.500, 1.000))
        inverses(self.ufc, ufloat(0.043, 0.010))

    def test_floor(self):
        ''' floor '''
        floors(mul(self.ufa, self.fa), ufloat( 98.000, 74.160))
        floors(mul(self.ufa, self.fb), ufloat(-51.000, 37.680))
        floors(mul(self.ufb, self.fa), ufloat(-50.000, 98.880))
        floors(mul(self.ufb, self.fb), ufloat( 25.000, 50.240))

    def test_round(self):
        ''' round '''
        rounds(mul(self.ufa, self.fa), ufloat( 99.000, 74.160))
        rounds(mul(self.ufa, self.fb), ufloat(-50.000, 37.680))
        rounds(mul(self.ufb, self.fa), ufloat(-49.000, 98.880))
        rounds(mul(self.ufb, self.fb), ufloat( 25.000, 50.240))

    '''
        Comparison Operators
    '''
    def test_eq(self):
        ''' eq == '''
        eqs(self.ufa, self.ufa, ubool(1.000))
        eqs(self.ufa, self.ufb, ubool(0.385))
        eqs(self.ufa, self.ufc, ubool(0.001))
        
    def test_ne(self):
        ''' ne != '''
        nes(self.ufa, self.ufa, ubool(0.000))
        nes(self.ufa, self.ufb, ubool(0.615))
        nes(self.ufa, self.ufc, ubool(0.999))

    def test_lt(self):
        ''' lt < '''
        lts(self.ufa,  self.ufa, ubool(0.000))
        lts(self.ufa,  self.ufb, ubool(0.615))
        lts(self.ufa,  self.ufc, ubool(0.999))
        
    def test_le(self):
        ''' le <= '''
        les(self.ufa, self.ufa, ubool(1.000))
        les(self.ufa, self.ufb, ubool(1.000))
        les(self.ufa, self.ufc, ubool(1.000))

    def test_gt(self):
        ''' gt > '''
        gts(self.ufa,  self.ufa, ubool(0.000))
        gts(self.ufa,  self.ufb, ubool(0.000))
        gts(self.ufa,  self.ufc, ubool(0.000))

    def test_ge(self):
        ''' ge >= '''
        ges(self.ufa, self.ufa, ubool(1.000))
        ges(self.ufa, self.ufb, ubool(0.385))
        ges(self.ufa, self.ufc, ubool(0.001))

if __name__ == '__main__':
    unittest.main()