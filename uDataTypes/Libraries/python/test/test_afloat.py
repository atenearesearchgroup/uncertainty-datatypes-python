import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class ufloatTest(unittest.TestCase):
    
    def setUp(self):
        self.a = afloat(-4.5, 3.1)
        self.b = afloat( 2.3, 4.2)
        self.c = afloat(23.7, 5.3)
        self.d = afloat(-4.9, 3.6)
        self.ai = aint(-4, 3.0)
        self.bi = aint( 2, 4.0)

    def test_init(self):
        ''' init '''
        t(afloat([1,2,3,4,5,6,7,8,9,10]), afloat(5, 3))
        t(afloat([0,-1,2,-3,4,-5,6,-7,8,-9]), afloat(0, 5.6))
        t(afloat([10,14,22,35,43,56,68,79,83,92]), afloat(50, 30))

    '''
        Operators
    '''
    def test_add(self):
        ''' add afloat + afloat '''
        adds(self.a, self.a, afloat(-8.150, 6.000))
        adds(self.a, self.b, afloat(-1.900, 4.800))
        adds(self.b, self.c, afloat(25.350, 6.500))
        adds(self.a, self.c, afloat(19.130, 6.100))

    def test_add_aint(self):
        ''' add aint + afloat '''
        adds(self.ai, self.a, afloat(-8.000, 4.250))
        adds(self.ai, self.b, afloat(-2.000, 5.000))
        adds(self.bi, self.b, afloat( 4.000, 5.250))
        adds(self.bi, self.a, afloat(-2.200, 4.700))
        ''' add afloat + aint '''
        adds(self.a, self.ai, afloat(-8.000, 4.250))
        adds(self.b, self.ai, afloat(-2.000, 5.000))
        adds(self.b, self.bi, afloat( 4.000, 5.250))
        adds(self.a, self.bi, afloat(-2.000, 5.000))

    def test_add_int(self):
        ''' add afloat + int '''
        adds(self.a, 0, afloat(-4, 3.0))
        adds(self.a, 1, afloat(-3, 3.0))
        adds(self.b, 2, afloat( 4, 4.0))
        adds(self.c, 3, afloat(26, 5.3))
        ''' add int + afloat '''
        adds(0, self.a, afloat(-4, 3.0))
        adds(1, self.a, afloat(-3, 2.8))
        adds(2, self.b, afloat( 4, 3.6))
        adds(3, self.c, afloat(26, 5.3))

    def test_add_float(self):
        ''' add afloat + float '''
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
        ''' sub afloat - afloat '''
        subs(self.a, self.a, afloat(  0.000, 0.000))
        subs(self.a, self.b, afloat( -6.223, 4.847))
        subs(self.b, self.c, afloat(-21.000, 6.543))
        subs(self.a, self.c, afloat(-27.300, 6.100))

    def test_sub_aint(self):
        ''' sub afloat - aint '''
        subs(self.ai, self.a, afloat( 0.450, 4.100))
        subs(self.ai, self.b, afloat(-5.750, 4.750))
        subs(self.bi, self.b, afloat(-0.300, 5.250))
        subs(self.bi, self.a, afloat( 5.900, 4.650))
        ''' sub aint - afloat '''
        subs(self.a, self.ai, afloat( -0.450, 4.150))
        subs(self.b, self.ai, afloat( 5.750, 4.750))
        subs(self.b, self.bi, afloat( 0.250, 5.250))
        subs(self.a, self.bi, afloat(-5.950, 4.650))

    def test_add_int(self):
        ''' add afloat + int '''
        subs(self.a, 0, afloat(-4, 3.0))
        subs(self.a, 1, afloat(-5, 2.8))
        subs(self.b, 2, afloat( 0, 3.6))
        subs(self.c, 3, afloat(20, 5.3))
        ''' add int + afloat '''
        subs(0, self.a, afloat(  4, 2.8))
        subs(1, self.a, afloat(  5, 2.8))
        subs(2, self.b, afloat(  0, 3.6))
        subs(3, self.c, afloat(-20, 5.3))

    def test_sub_float(self):
        ''' sub afloat - float '''
        subs(self.a, 0.0, afloat(-4.000, 3.000))
        subs(self.a, 1.0, afloat(-5.000, 3.000))
        subs(self.b, 2.5, afloat(-0.650, 3.600))
        subs(self.c, 3.7, afloat(18.800, 5.300))
        ''' sub float - afloat '''
        subs(0.0, self.a, afloat(  4.000, 3.000))
        subs(1.0, self.a, afloat(  5.000, 3.000))
        subs(2.5, self.b, afloat(  0.650, 3.600))
        subs(3.7, self.c, afloat(-18.750, 5.300))

    def test_mul(self):
        ''' mul afloat * afloat '''
        muls(self.a, self.a, afloat(26.0, 26.516))
        muls(self.a, self.b, afloat( -7, 17.5))
        muls(self.b, self.c, afloat( 41, 84.0))
        muls(self.a, self.c, afloat(-81, 68.5))
   
    def test_mul_aint(self):
        ''' mul afloat * aint '''
        muls(self.ai, self.a, afloat(15.000, 17.950))
        muls(self.ai, self.b, afloat(-7.900, 18.700))
        muls(self.bi, self.b, afloat( 4.000, 17.250))
        muls(self.bi, self.a, afloat(-7.500, 19.000))
        ''' mul aint * afloat '''
        muls(self.a, self.ai, afloat(14.850, 18.000))
        muls(self.b, self.ai, afloat(-7.900, 18.700))
        muls(self.b, self.bi, afloat( 4.000, 17.250))
        muls(self.a, self.bi, afloat(-7.500, 19.000))

    def test_mul_int(self):
        ''' mul afloat * int '''
        muls(self.a, 0, afloat( 0, 0.0))
        muls(self.a, 1, afloat(-4, 3.0))
        muls(self.b, 2, afloat( 4, 7.2))
        muls(self.c, 3, afloat(67,15.9))
        ''' mul int * afloat '''
        muls(0, self.a, afloat( 0, 0.0))
        muls(1, self.a, afloat(-4, 3.0))
        muls(2, self.b, afloat( 4, 8.0))
        muls(3, self.c, afloat(69,15.9))
    def test_mul_float(self):
        ''' mul afloat * float '''
        muls(self.a, 0.0, afloat( 0.000, 0.000))
        muls(self.a, 1.0, afloat(-4.000, 3.000))
        muls(self.b, 2.5, afloat( 5.000, 9.000))
        muls(self.c, 3.7, afloat(83.200, 19.600))
        ''' mul float * afloat '''
        muls(0.0, self.a, afloat( 0.000,  0.000))
        muls(1.0, self.a, afloat(-4.000,  3.000))
        muls(2.5, self.b, afloat( 4.648,  9.030))
        muls(3.7, self.c, afloat(83.250, 19.600))
        
    def test_div(self):
        ''' div afloat / afloat '''
        divs(self.a, self.a, afloat( 0.820, 0.380))
        divs(self.a, self.b, afloat(-0.200, 2.250))
        divs(self.b, self.c, afloat( 0.100, 0.180))
        divs(self.a, self.c, afloat(-0.190, 0.140))

    def test_div_ufloat(self):
        ''' div afloat / afloat '''
        divs(self.ai, self.a, afloat( 1.000, 1.500))
        divs(self.ai, self.b, afloat(-0.200, 2.100))
        divs(self.bi, self.b, afloat( 0.100, 1.800))
        divs(self.bi, self.a, afloat(-0.500, 1.500))
        ''' div afloat / aint '''
        divs(self.a, self.ai, afloat( 1.000, 1.800))
        divs(self.b, self.ai, afloat(-0.500, 1.700))
        divs(self.b, self.bi, afloat( 0.100, 2.000))
        divs(self.a, self.bi, afloat(-0.200, 2.300))
    
    def test_div_int(self):
        ''' div afloat / int '''
        divs(self.a, 1, afloat(-4.000, 3.000))
        divs(self.b, 2, afloat( 1.000, 1.800))
        divs(self.c, 4, afloat( 6.00, 1.300))
        ''' div int * afloat '''
        divs(2, self.b, afloat(0.100, 0.900))
        divs(3, self.c, afloat(0.140, 0.030))
    
    def test_div_float(self):
        ''' div afloat / float '''
        divs(self.a, 1.0, afloat(-4.000, 3.000))
        divs(self.b, 2.5, afloat( 0.750, 1.450))
        divs(self.c, 3.7, afloat( 6.100, 1.400))
        ''' div float / afloat '''
        divs(0.0, self.a, afloat( 0.000, 0.000))
        divs(1.0, self.a, afloat(-0.250, 0.330))
        divs(2.5, self.b, afloat( 0.100, 1.150))
        divs(3.7, self.c, afloat( 0.170, 0.040))

    def test_floordiv(self):
        ''' floordiv afloat // afloat '''
        floordivs(self.a, self.a, afloat( 1, 0.4))
        floordivs(self.a, self.b, afloat( 0, 2.1))
        floordivs(self.b, self.c, afloat( 0, 0.4))
        floordivs(self.a, self.c, afloat(-1, 0.4))

    def test_floordiv_ufloat(self):
        ''' floordiv afloat // aint '''
        floordivs(self.ai, self.a, afloat( 1.000, 1.500))
        floordivs(self.ai, self.b, afloat( 0.000, 2.100))
        floordivs(self.bi, self.b, afloat( 0.000, 1.850))
        floordivs(self.bi, self.a, afloat(-1.000, 1.450))
        ''' floordiv aint // afloat '''
        floordivs(self.a, self.ai, afloat( 1.000, 1.800))
        floordivs(self.b, self.ai, afloat(-1.000, 1.730))
        floordivs(self.b, self.bi, afloat( 0.000, 2.030))
        floordivs(self.a, self.bi, afloat( 0.000, 2.360))

    def test_floordiv_int(self):
        ''' floordiv afloat // int '''
        floordivs(self.a, 1, afloat(-4.000, 3.0))
        floordivs(self.b, 2, afloat( 1.000, 1.8))
        floordivs(self.c, 3, afloat( 7.000, 1.8))
        ''' floordiv int // afloat '''
        floordivs(1, self.a, afloat(-1.000, 0.379))
        floordivs(2, self.b, afloat( 0.000, 0.9))
        floordivs(3, self.c, afloat( 0.000, 0.0))

    def test_floordiv_float(self):
        ''' floordiv afloat // float '''
        floordivs(self.a, 1.0, afloat(-4.000, 3.000))
        floordivs(self.b, 2.5, afloat( 0.000, 1.500))
        floordivs(self.c, 3.7, afloat( 6.000, 1.400))
        ''' floordiv float / afloat '''
        floordivs(0.0, self.a, afloat( 0.000, 0.000))
        floordivs(1.0, self.a, afloat(-1.000, 0.460))
        floordivs(2.5, self.b, afloat( 0.000, 1.150))
        floordivs(3.7, self.c, afloat( 0.000, 0.000))

    def test_neg(self):
        ''' neg - '''
        negs(self.a, afloat(  4, 3.0))
        negs(self.b, afloat( -2, 4.0))
        negs(self.c, afloat(-23, 5.3))
        
    def test_power(self):
        ''' power ** '''
        pows(self.a, 2, afloat(  26.0,    26.365))
        pows(self.b, 5, afloat(6546.0, 13983.474))
        pows(self.c, 4, afloat(342818,277783.947))

    '''
        Comparison Operators
    '''
    def test_eq(self):
        ''' eq == '''
        eqs(self.a, self.a, ubool(1.000))
        eqs(self.b, self.c, ubool(0.024))
        eqs(self.a, self.d, ubool(0.917))
        
    def test_ne(self):
        ''' ne != '''
        nes(self.a, self.a, ubool(0.000))
        nes(self.b, self.c, ubool(0.976))
        nes(self.a, self.d, ubool(0.083))

    def test_lt(self):
        ''' lt < '''
        lts(self.a, self.a, ubool(0.000))
        lts(self.b, self.c, ubool(0.976))
        lts(self.a, self.d, ubool(0.014))
        
    def test_le(self):
        ''' le <= '''
        les(self.a, self.a, ubool(1.000))
        les(self.b, self.c, ubool(1.000))
        les(self.a, self.d, ubool(0.930))

    def test_gt(self):
        ''' gt > '''
        gts(self.a, self.a, ubool(0.000))
        gts(self.b, self.c, ubool(0.000))
        gts(self.a, self.d, ubool(0.070))

    def test_ge(self):
        ''' ge >= '''
        ges(self.a, self.a, ubool(1.000))
        ges(self.b, self.c, ubool(0.024))
        ges(self.a, self.d, ubool(0.986))
    
if __name__ == '__main__':
    unittest.main()