import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class uintTest(unittest.TestCase):
    
    def setUp(self):
        self.a = aint(-4, 3.0)
        self.b = aint( 2, 4.0)
        self.af = afloat(-4.5, 3.1)
        self.bf = afloat( 2.3, 4.2)
        self.c = aint(23, 5.3)
        self.d = aint(-4, 3.0)

    def test_init(self):
        ''' init '''
        t(aint([1,2,3,4,5,6,7,8,9,10]), aint(5, 3))
        t(aint([0,-1,2,-3,4,-5,6,-7,8,-9]), aint(0, 5.6))
        t(aint([10,14,22,35,43,56,68,79,83,92]), aint(50, 30))

    '''
        Operators
    '''
    def test_add(self):
        ''' add aint + aint '''
        adds(self.a, self.a, aint(-7,  5.700))
        adds(self.a, self.b, aint(-2,  4.600))
        adds(self.b, self.c, aint(24,  6.400))
        adds(self.a, self.c, aint(19,  6.100))

    def test_add_afloat(self):
        ''' add aint + afloat '''
        adds(self.a, self.af, afloat(-8.000, 4.250))
        adds(self.a, self.bf, afloat(-2.000, 5.000))
        adds(self.b, self.bf, afloat( 4.000, 5.250))
        adds(self.b, self.af, afloat(-2.200, 4.700))
        ''' add afloat + aint '''
        adds(self.af, self.a, afloat(-8.000, 4.250))
        adds(self.bf, self.a, afloat(-1.000, 4.750))
        adds(self.bf, self.b, afloat( 4.000, 5.250))
        adds(self.af, self.b, afloat(-2.000, 5.000))

    def test_add_int(self):
        ''' add aint + int '''
        adds(self.a, 0, aint(-4, 3.000))
        adds(self.a, 1, aint(-3, 3.000))
        adds(self.b, 2, aint( 4, 4.000))
        adds(self.c, 3, aint(26, 5.300))
        ''' add int + aint '''
        adds(0, self.a, aint(-4, 3.000))
        adds(1, self.a, aint(-3, 2.800))
        adds(2, self.b, aint( 4, 3.600))
        adds(3, self.c, aint(26, 5.300))

    def test_add_float(self):
        ''' add aint + float '''
        adds(self.a, 0.0, afloat(-4.000, 3.000))
        adds(self.a, 1.0, afloat(-3.000, 3.000))
        adds(self.b, 2.5, afloat( 4.000, 3.600))
        adds(self.c, 3.7, afloat(26.000, 5.300))
        ''' add float + aint '''
        adds(0.0, self.a, afloat(-4.000, 3.000))
        adds(1.0, self.a, afloat(-3.000, 3.000))
        adds(2.5, self.b, afloat( 4.000, 3.609))
        adds(3.7, self.c, afloat(26.000, 5.300))
    
    def test_sub(self):
        ''' sub aint - aint '''
        subs(self.a, self.a, aint(  0,  0.000))
        subs(self.a, self.b, aint( -5,  4.600))
        subs(self.b, self.c, aint(-21,  6.400))
        subs(self.a, self.c, aint(-26,  6.100))

    def test_sub_afloat(self):
        ''' sub aint - afloat '''
        subs(self.a, self.af, afloat( 0.450, 4.100))
        subs(self.a, self.bf, afloat(-5.750, 4.750))
        subs(self.b, self.bf, afloat(-0.300, 5.250))
        subs(self.b, self.af, afloat( 5.900, 4.650))
        ''' sub afloat - aint '''
        subs(self.af, self.a, afloat( -0.450, 4.150))
        subs(self.bf, self.a, afloat( 5.750, 4.750))
        subs(self.bf, self.b, afloat( 0.250, 5.250))
        subs(self.af, self.b, afloat(-5.950, 4.650))

    def test_sub_int(self):
        ''' sub aint - int '''
        subs(self.a, 0, aint(-4, 3.0))
        subs(self.a, 1, aint(-5, 2.8))
        subs(self.b, 2, aint( 0, 3.6))
        subs(self.c, 3, aint(20, 5.3))
        ''' sub int - aint '''
        subs(0, self.a, aint(  4, 2.8))
        subs(1, self.a, aint(  5, 2.8))
        subs(2, self.b, aint(  0, 3.6))
        subs(3, self.c, aint(-20, 5.3))

    def test_sub_float(self):
        ''' sub aint - float '''
        subs(self.a, 0.0, afloat(-4.000, 3.000))
        subs(self.a, 1.0, afloat(-5.000, 3.000))
        subs(self.b, 2.5, afloat(-0.650, 3.600))
        subs(self.c, 3.7, afloat(18.800, 5.300))
        ''' sub float - aint '''
        subs(0.0, self.a, afloat(  4.000, 3.000))
        subs(1.0, self.a, afloat(  5.000, 3.000))
        subs(2.5, self.b, afloat(  0.650, 3.600))
        subs(3.7, self.c, afloat(-18.750, 5.300))
    
    def test_mul(self):
        ''' mul aint * aint '''
        muls(self.a, self.a, aint( 21, 22.7))
        muls(self.a, self.b, aint( -7, 17.5))
        muls(self.b, self.c, aint( 41, 84.0))
        muls(self.a, self.c, aint(-81, 68.5))

    def test_mul_afloat(self):
        ''' mul aint * afloat '''
        muls(self.a, self.af, afloat(15.000, 17.950))
        muls(self.a, self.bf, afloat(-7.900, 18.700))
        muls(self.b, self.bf, afloat( 4.000, 17.250))
        muls(self.b, self.af, afloat(-7.500, 19.000))
        ''' mul afloat * aint '''
        muls(self.af, self.a, afloat(14.850, 18.000))
        muls(self.bf, self.a, afloat(-7.900, 18.700))
        muls(self.bf, self.b, afloat( 4.000, 17.250))
        muls(self.af, self.b, afloat(-7.500, 19.000))

    def test_mul_int(self):
        ''' mul aint * int '''
        muls(self.a, 0, aint( 0, 0.000))
        muls(self.a, 1, aint(-4, 3.000))
        muls(self.b, 2, aint( 4, 7.200))
        muls(self.c, 3, aint(67,15.900))
        ''' mul int * aint '''
        muls(0, self.a, aint( 0, 0.000))
        muls(1, self.a, aint(-4, 3.000))
        muls(2, self.b, aint( 4, 7.200))
        muls(3, self.c, aint(67,15.900))
        
    def test_mul_float(self):
        ''' mul aint * float '''
        muls(self.a, 0.0, afloat( 0.000, 0.000))
        muls(self.a, 1.0, afloat(-4.000, 3.000))
        muls(self.b, 2.5, afloat( 5.000, 9.000))
        muls(self.c, 3.7, afloat(83.200, 19.600))
        ''' mul float * aint '''
        muls(0.0, self.a, afloat( 0.000,  0.000))
        muls(1.0, self.a, afloat(-4.000,  3.000))
        muls(2.5, self.b, afloat( 4.648,  9.030))
        muls(3.7, self.c, afloat(83.250, 19.600))
       
    def test_div(self):
        ''' div aint / aint '''
        divs(self.a, self.a, afloat( 0.900,  0.4))
        divs(self.a, self.b, afloat(-0.150, 2.100))
        divs(self.b, self.c, afloat( 0.100, 0.200))
        divs(self.a, self.c, afloat(-0.200, 0.150))

    def test_div_afloat(self):
        ''' div aint / afloat '''
        divs(self.a, self.af, afloat( 1.000, 1.500))
        divs(self.a, self.bf, afloat(-0.200, 2.100))
        divs(self.b, self.bf, afloat( 0.100, 1.800))
        divs(self.b, self.af, afloat(-0.500, 1.500))
        ''' div afloat / aint '''
        divs(self.af, self.a, afloat( 1.000, 1.800))
        divs(self.bf, self.a, afloat(-0.500, 1.700))
        divs(self.bf, self.b, afloat( 0.100, 2.000))
        divs(self.af, self.b, afloat(-0.200, 2.300))
    
    def test_div_int(self):
        ''' div aint / int ''' # --> FLOAT
        divs(self.a, 1, afloat(-4.000, 3.000))
        divs(self.b, 2, afloat( 1.000, 1.800))
        divs(self.c, 4, afloat( 5.600, 1.300))
        ''' div int / aint '''
        divs(2, self.b, afloat(0.100, 0.900))
        divs(3, self.c, afloat(0.140, 0.035))
    
    def test_div_float(self):
        ''' div aint / float '''
        divs(self.a, 1.0, afloat(-4.000, 3.000))
        divs(self.b, 2.5, afloat( 0.750, 1.450))
        divs(self.c, 3.7, afloat( 6.100, 1.400))
        ''' div float / aint '''
        divs(0.0, self.a, afloat( 0.000, 0.000))
        divs(1.0, self.a, afloat(-0.250, 0.330))
        divs(2.5, self.b, afloat( 0.100, 1.150))
        divs(3.7, self.c, afloat( 0.175, 0.050))

    def test_floordiv(self):
        ''' floordiv aint // aint '''
        floordivs(self.a, self.a, aint( 1, 0.4))
        floordivs(self.a, self.b, aint( 0, 2.1))
        floordivs(self.b, self.c, aint( 0, 0.4))
        floordivs(self.a, self.c, aint(-1, 0.4))
    
    def test_floordiv_afloat(self):
        ''' floordiv aint // afloat '''
        floordivs(self.a, self.af, afloat( 1.000, 1.500))
        floordivs(self.a, self.bf, afloat( 0.000, 2.100))
        floordivs(self.b, self.bf, afloat( 0.000, 1.850))
        floordivs(self.b, self.af, afloat(-1.000, 1.450))
        ''' floordiv afloat // aint '''
        floordivs(self.af, self.a, afloat( 1.000, 1.800))
        floordivs(self.bf, self.a, afloat(-1.000, 1.730))
        floordivs(self.bf, self.b, afloat( 0.000, 2.030))
        floordivs(self.af, self.b, afloat( 0.000, 2.360))
    
    def test_floordiv_int(self):
        ''' floordiv aint // int '''
        floordivs(self.a, 1, aint(-4, 3.000))
        floordivs(self.b, 2, aint( 1, 1.800))
        floordivs(self.c, 3, aint( 7, 1.800))
        ''' floordiv int // aint '''
        floordivs(1, self.a, aint(-1, 0.500))
        floordivs(2, self.b, aint( 0, 0.900))
        floordivs(3, self.c, aint( 0, 0.000))
    
    def test_floordiv_float(self):
        ''' floordiv aint // float '''
        floordivs(self.a, 1.0, afloat(-4.000, 3.000))
        floordivs(self.b, 2.5, afloat( 0.000, 1.500))
        floordivs(self.c, 3.7, afloat( 6.000, 1.400))
        ''' floordiv float / aint '''
        floordivs(0.0, self.a, afloat( 0.000, 0.000))
        floordivs(1.0, self.a, afloat(-1.000, 0.460))
        floordivs(2.5, self.b, afloat( 0.000, 1.150))
        floordivs(3.7, self.c, afloat( 0.000, 0.000))
    
    def test_neg(self):
        ''' neg - '''
        negs(self.a, aint(  4, 3.0))
        negs(self.b, aint( -2, 4.0))
        negs(self.c, aint(-23, 5.3))
        
    def test_power(self):
        ''' power ** '''
        pows(self.a, 2, aint(    16,  24.000))
        pows(self.b, 5, aint(  4193,8939.381))
        pows(self.c, 3, aint(13286, 8499.250))

    '''
        Comparison Operators
    '''
    def test_eq(self):
        ''' eq == '''
        eqs(self.a, self.a, ubool(1.000))
        eqs(self.b, self.c, ubool(0.024))
        eqs(self.a, self.d, ubool(1.000))
        
    def test_ne(self):
        ''' ne != '''
        nes(self.a, self.a, ubool(0.000))
        nes(self.b, self.c, ubool(0.976))
        nes(self.a, self.d, ubool(0.000))

    def test_lt(self):
        ''' lt < '''
        lts(self.a, self.a, ubool(0.000))
        lts(self.b, self.c, ubool(0.976))
        lts(self.a, self.d, ubool(0.000))
        
    def test_le(self):
        ''' le <= '''
        les(self.a, self.a, ubool(1.000))
        les(self.b, self.c, ubool(1.000))
        les(self.a, self.d, ubool(1.000))

    def test_gt(self):
        ''' gt > '''
        gts(self.a, self.a, ubool(0.000))
        gts(self.b, self.c, ubool(0.000))
        gts(self.a, self.d, ubool(0.000))

    def test_ge(self):
        ''' ge >= '''
        ges(self.a, self.a, ubool(1.000))
        ges(self.b, self.c, ubool(0.024))
        ges(self.a, self.d, ubool(1.000))
  
if __name__ == '__main__':
    unittest.main()