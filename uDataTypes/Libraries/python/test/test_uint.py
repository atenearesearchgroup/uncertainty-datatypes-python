import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

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
        ''' add uint + uint '''
        adds(self.uia, self.uia, uint(-8, 4.243))
        adds(self.uia, self.uib, uint(-2, 5.000))
        adds(self.uib, self.uib, uint( 4, 5.657))
        adds(self.uib, self.uia, uint(-2, 5.000))

    def test_add_ufloat(self):
        ''' add uint + ufloat '''
        adds(self.uia, self.ufa, ufloat(-8.000, 4.243))
        adds(self.uia, self.ufb, ufloat(-2.000, 5.000))
        adds(self.uib, self.ufa, ufloat(-2.000, 5.000))
        adds(self.uib, self.ufb, ufloat( 4.000, 5.657))
        ''' add ufloat + uint '''
        adds(self.ufa, self.uia, ufloat(-8.000, 4.243))
        adds(self.ufa, self.uib, ufloat(-2.000, 5.000))
        adds(self.ufb, self.uia, ufloat(-2.000, 5.000))
        adds(self.ufb, self.uib, ufloat( 4.000, 5.657))

    def test_add_int(self):
        ''' add uint + int '''
        adds(self.uia, self.ia, uint(-8, 3.000))
        adds(self.uia, self.ib, uint(-2, 3.000))
        adds(self.uib, self.ia, uint(-2, 4.000))
        adds(self.uib, self.ib, uint( 4, 4.000))
        ''' add int + uint '''
        adds(self.ia, self.uia, uint(-8, 3.000))
        adds(self.ib, self.uia, uint(-2, 3.000))
        adds(self.ia, self.uib, uint(-2, 4.000))
        adds(self.ib, self.uib, uint( 4, 4.000))

    def test_add_float(self):
        ''' add uint + float '''
        adds(self.uia, self.fa, ufloat(-28.720, 3.000))
        adds(self.uia, self.fb, ufloat(  8.560, 3.000))
        adds(self.uib, self.fa, ufloat(-22.720, 4.000))
        adds(self.uib, self.fb, ufloat( 14.560, 4.000))
        ''' add float + uint'''
        adds(self.fa, self.uia, ufloat(-28.720, 3.000))
        adds(self.fb, self.uia, ufloat(  8.560, 3.000))
        adds(self.fa, self.uib, ufloat(-22.720, 4.000))
        adds(self.fb, self.uib, ufloat( 14.560, 4.000))

    def test_sub(self):
        ''' sub uint - uint '''
        subs(self.uia, self.uia, uint( 0, 0.000))
        subs(self.uia, self.uib, uint(-6, 5.000))
        subs(self.uib, self.uib, uint( 0, 0.000))
        subs(self.uib, self.uia, uint( 6, 5.000))

    def test_sub_ufloat(self):
        ''' sub uint - ufloat '''
        subs(self.uia, self.ufa, ufloat( 0.000, 4.243))
        subs(self.uia, self.ufb, ufloat(-6.000, 5.000))
        subs(self.uib, self.ufa, ufloat( 6.000, 5.000))
        subs(self.uib, self.ufb, ufloat( 0.000, 5.657))
        ''' sub ufloat - uint '''
        subs(self.ufa, self.uia, ufloat( 0.000, 4.243))
        subs(self.ufb, self.uia, ufloat( 6.000, 5.000))
        subs(self.ufa, self.uib, ufloat(-6.000, 5.000))
        subs(self.ufb, self.uib, ufloat( 0.000, 5.657))

    def test_sub_int(self):
        ''' sub uint - int '''
        subs(self.uia, self.ia, uint( 0, 3.000))
        subs(self.uia, self.ib, uint(-6, 3.000))
        subs(self.uib, self.ia, uint( 6, 4.000))
        subs(self.uib, self.ib, uint( 0, 4.000))
        ''' sub int - uint '''
        subs(self.ia, self.uia, uint( 0, 3.000))
        subs(self.ib, self.uia, uint( 6, 3.000))
        subs(self.ia, self.uib, uint(-6, 4.000))
        subs(self.ib, self.uib, uint( 0, 4.000))

    def test_sub_float(self):
        ''' sub uint - float '''
        subs(self.uia, self.fa, ufloat( 20.720, 3.000))
        subs(self.uia, self.fb, ufloat(-16.560, 3.000))
        subs(self.uib, self.fa, ufloat( 26.720, 4.000))
        subs(self.uib, self.fb, ufloat(-10.560, 4.000))
        ''' sub float - uint '''
        subs(self.fa, self.uia, ufloat(-20.720, 3.000))
        subs(self.fb, self.uia, ufloat( 16.560, 3.000))
        subs(self.fa, self.uib, ufloat(-26.720, 4.000))
        subs(self.fb, self.uib, ufloat( 10.560, 4.000))

    def test_mul(self):
        ''' mul uint * uint '''
        muls(self.uia, self.uia, uint(16, 16.971))
        muls(self.uia, self.uib, uint(-8, 17.088))
        muls(self.uib, self.uib, uint( 4, 11.314))
        muls(self.uib, self.uia, uint(-8, 17.088))
        
    def test_mul_ufloat(self):
        ''' mul uint * ufloat '''
        muls(self.uia, self.ufa, ufloat(16.000, 16.971))
        muls(self.uia, self.ufb, ufloat(-8.000, 17.088))
        muls(self.uib, self.ufa, ufloat(-8.000, 17.088))
        muls(self.uib, self.ufb, ufloat( 4.000, 11.314))
        ''' mul ufloat * uint '''
        muls(self.ufa, self.uia, ufloat(16.000, 16.971))
        muls(self.ufb, self.uia, ufloat(-8.000, 17.088))
        muls(self.ufa, self.uib, ufloat(-8.000, 17.088))
        muls(self.ufb, self.uib, ufloat( 4.000, 11.314))

    def test_mul_int(self):
        ''' mul uint * int '''
        muls(self.uia, self.ia, uint(16, 12.000))
        muls(self.uia, self.ib, uint(-8,  6.000))
        muls(self.uib, self.ia, uint(-8, 16.000))
        muls(self.uib, self.ib, uint( 4,  8.000))
        ''' mul int * uint '''
        muls(self.ia, self.uia, uint(16, 12.000))
        muls(self.ib, self.uia, uint(-8,  6.000))
        muls(self.ia, self.uib, uint(-8, 16.000))
        muls(self.ib, self.uib, uint( 4,  8.000))

    def test_mul_float(self):
        ''' mul uint * float '''
        muls(self.uia, self.fa, ufloat( 98.880, 74.160))
        muls(self.uia, self.fb, ufloat(-50.240, 37.680))
        muls(self.uib, self.fa, ufloat(-49.440, 98.880))
        muls(self.uib, self.fb, ufloat( 25.120, 50.240))
        ''' mul float * uint '''
        muls(self.fa, self.uia, ufloat( 98.880, 74.160))
        muls(self.fb, self.uia, ufloat(-50.240, 37.680))
        muls(self.fa, self.uib, ufloat(-49.440, 98.880))
        muls(self.fb, self.uib, ufloat( 25.120, 50.240))

    def test_div(self):
        ''' div uint / uint '''
        divs(self.uia, self.uia, ufloat( 1.000, 1.677))
        divs(self.uia, self.uib, ufloat(-2.000, 4.528))
        divs(self.uib, self.uib, ufloat( 1.000, 3.464))
        divs(self.uib, self.uia, ufloat(-0.500, 2.035))
        
    def test_div_ufloat(self):
        ''' div uint / ufloat '''
        divs(self.uia, self.ufa, ufloat( 1.000, 1.677))
        divs(self.uia, self.ufb, ufloat(-2.000, 4.528))
        divs(self.uib, self.ufa, ufloat(-0.500, 2.035))
        divs(self.uib, self.ufb, ufloat( 1.000, 3.464))
        ''' div ufloat / uint '''
        divs(self.ufa, self.uia, ufloat( 1.000, 1.677))
        divs(self.ufb, self.uia, ufloat(-0.500, 2.035))
        divs(self.ufa, self.uib, ufloat(-2.000, 4.528))
        divs(self.ufb, self.uib, ufloat( 1.000, 3.464))

    def test_div_int(self):
        ''' div uint / int '''
        divs(self.uia, self.ia, ufloat( 1.000, 0.750))
        divs(self.uia, self.ib, ufloat(-2.000, 1.500))
        divs(self.uib, self.ia, ufloat(-0.500, 1.000))
        divs(self.uib, self.ib, ufloat( 1.000, 2.000))
        ''' div int / uint '''
        divs(self.ia, self.uia, ufloat( 1.000, 0.188))
        divs(self.ib, self.uia, ufloat(-0.500, 0.188))
        divs(self.ia, self.uib, ufloat(-2.000, 1.000))
        divs(self.ib, self.uib, ufloat( 1.000, 1.000))

    def test_div_float(self):
        ''' div uint / float '''
        divs(self.uia, self.fa, ufloat(0.162, 0.121))
        divs(self.uia, self.fb, ufloat(-0.318, 0.239))
        divs(self.uib, self.fa, ufloat(-0.081, 0.162))
        divs(self.uib, self.fb, ufloat(0.159, 0.318))
        ''' div float / uint '''
        divs(self.fa, self.uia, ufloat(  6.180, 0.188))
        divs(self.fb, self.uia, ufloat(- 3.140, 0.188))
        divs(self.fa, self.uib, ufloat(-12.360, 1.000))
        divs(self.fb, self.uib, ufloat(  6.280, 1.000))
    
    def test_floordiv(self):
        ''' floordiv uint // uint '''
        floordivs(self.uia, self.uia, uint( 1, 0.000))
        floordivs(self.uia, self.uib, uint(-2, 4.528))
        floordivs(self.uib, self.uib, uint( 1, 0.000))
        floordivs(self.uib, self.uia, uint(-1, 2.035))
        
    def test_floordiv_ufloat(self):
        ''' floordiv uint // ufloat '''
        floordivs(self.uia, self.ufa, ufloat( 1.000, 1.677))
        floordivs(self.uia, self.ufb, ufloat(-2.000, 4.528))
        floordivs(self.uib, self.ufa, ufloat(-1.000, 2.035))
        floordivs(self.uib, self.ufb, ufloat( 1.000, 3.464))
        ''' floordiv ufloat // uint '''
        floordivs(self.ufa, self.uia, ufloat( 1.000, 1.677))
        floordivs(self.ufb, self.uia, ufloat(-1.000, 2.035))
        floordivs(self.ufa, self.uib, ufloat(-2.000, 4.528))
        floordivs(self.ufb, self.uib, ufloat( 1.000, 3.464))

    def test_floordiv_int(self):
        ''' floordiv uint // int '''
        floordivs(self.uia, self.ia, uint( 1, 0.750))
        floordivs(self.uia, self.ib, uint(-2, 1.500))
        floordivs(self.uib, self.ia, uint(-1, 1.000))
        floordivs(self.uib, self.ib, uint( 1, 2.000))
        ''' floordiv int // uint '''
        floordivs(self.ia, self.uia, uint( 1, 0.188))
        floordivs(self.ib, self.uia, uint(-1, 0.188))
        floordivs(self.ia, self.uib, uint(-2, 1.000))
        floordivs(self.ia, self.uib, uint(-2, 1.000))

    def test_floordiv_float(self):
        ''' floordiv uint // float '''
        floordivs(self.uia, self.fa, ufloat( 0.000, 0.121))
        floordivs(self.uia, self.fb, ufloat(-1.000, 0.239))
        floordivs(self.uib, self.fa, ufloat(-1.000, 0.162))
        floordivs(self.uib, self.fb, ufloat( 0.000, 0.318))
        ''' floordiv float // uint '''
        floordivs(self.fa, self.uia, ufloat(  6.000, 0.188))
        floordivs(self.fb, self.uia, ufloat(- 4.000, 0.188))
        floordivs(self.fa, self.uib, ufloat(-13.000, 1.000))
        floordivs(self.fb, self.uib, ufloat(  6.000, 1.000))
        
    def test_neg(self):
        ''' neg - '''
        negs(self.uia, uint( 4, 3.000))
        negs(self.uib, uint(-2, 4.000))
        negs(self.ufa, uint( 4, 3.000))
        negs(self.ufb, uint(-2, 4.000))     

    def test_pow(self):
        ''' pow ** '''
        pows(self.uia, 2, uint(   16,   24.000))
        pows(self.uia, 3, uint(  -64,  144.000))
        pows(self.uia, 5, uint(-1024, 3840.000))
        pows(self.uib, 2.50, ufloat( 5.657,  28.284))
        pows(self.uib, 3.25, ufloat( 9.514,  61.839))
        pows(self.uib, 5.03, ufloat(32.672, 328.684))

    '''
        Functions
    '''
    def test_abs(self):
        ''' abs '''
        abss(self.uia, ufloat( 4.0, 3.0))
        abss(self.uib, ufloat( 2.0, 4.0))
        abss(self.uic, ufloat(23.0, 5.3))

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
        t(max(self.uia, self.uib, self.uic), self.uic)
        t(max(abs(self.uia), abs(self.uib), abs(self.uic)), self.uic)
        t(max(uint(2, 12), uint(1, 12), uint(3, 12), uint(5, 12), uint(3, 12), uint(2, 12), uint(0, 12), uint(4, 12)), uint(5, 12))
        t(max(uint(2, 12), uint(-1, 12), uint(3, 12), uint(5, 12), uint(-3, 12), uint(2, 12), uint(-0, 12), uint(4, 12)), uint(5, 12))
        t(max(2, uint(-1, 12), 3, uint(5, 12), -3, uint(2, 12), uint(-0, 12), 6), 6)
        t(max(2, uint(-1, 1), ufloat(-3.5, 1.0), uint(3, 1), -2, uint(0, 1), -4, ufloat(5.5, 1.7)), ufloat(5.5, 1.7))

    def test_min(self):
        ''' min '''
        t(min(self.uia, self.uib, self.uic), self.uia)
        t(min(abs(self.uia), abs(self.uib), abs(self.uic)), self.uib)
        t(min(uint(2, 1), uint(1, 1), uint(3, 1), uint(3, 1), uint(2, 1), uint(0, 1), uint(4, 1), uint(5, 1)), uint(0, 1))
        t(min(uint(2, 1), uint(-1, 1), uint(3, 1), uint(3, 1), uint(-2, 1), uint(0, 1), uint(-4, 1), uint(5, 1)), uint(-4, 1))
        t(min(2, uint(-1, 1), -3, uint(3, 1), -2, uint(0, 1), -4, -5), -5)
        t(min(2, uint(-1, 1), ufloat(-3.5, 1.0), uint(3, 1), -2, uint(0, 1), -4, ufloat(-5.5, 1.7)), ufloat(-5.5, 1.7))

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