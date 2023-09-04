import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

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
        ''' add ufloat + ufloat '''
        adds(self.ufa, self.ufa, ufloat(-8.000, 4.243))
        adds(self.ufa, self.ufb, ufloat(-2.000, 5.000))
        adds(self.ufb, self.ufb, ufloat( 4.000, 5.657))
        adds(self.ufb, self.ufa, ufloat(-2.000, 5.000))

    def test_add_uint(self):
        ''' add ufloat + uint '''
        adds(self.ufa, self.uia, ufloat(-8.000, 4.243))
        adds(self.ufa, self.uib, ufloat(-2.000, 5.000))
        adds(self.ufb, self.uia, ufloat(-2.000, 5.000))
        adds(self.ufb, self.uib, ufloat( 4.000, 5.657))
        ''' add uint + ufloat '''
        adds(self.uia, self.ufa, ufloat(-8.000, 4.243))
        adds(self.uib, self.ufa, ufloat(-2.000, 5.000))
        adds(self.uia, self.ufb, ufloat(-2.000, 5.000))
        adds(self.uib, self.ufb, ufloat( 4.000, 5.657))

    def test_add_int(self):
        ''' add ufloat + int '''
        adds(self.ufa, self.ia, ufloat(-8.000, 3.000))
        adds(self.ufa, self.ib, ufloat(-2.000, 3.000))
        adds(self.ufb, self.ia, ufloat(-2.000, 4.000))
        adds(self.ufb, self.ib, ufloat( 4.000, 4.000))
        ''' add int + ufloat '''
        adds(self.ia, self.ufa, ufloat(-8.000, 3.000))
        adds(self.ib, self.ufa, ufloat(-2.000, 3.000))
        adds(self.ia, self.ufb, ufloat(-2.000, 4.000))
        adds(self.ib, self.ufb, ufloat( 4.000, 4.000))

    def test_add_float(self):
        ''' add ufloat + float '''
        adds(self.ufa, self.fa, ufloat(-28.720, 3.000))
        adds(self.ufa, self.fb, ufloat(8.560, 3.000))
        adds(self.ufb, self.fa, ufloat(-22.720, 4.000))
        adds(self.ufb, self.fb, ufloat(14.560, 4.000))
        ''' add float + ufloat '''
        adds(self.fa, self.ufa, ufloat(-28.720, 3.000))
        adds(self.fb, self.ufa, ufloat(8.560, 3.000))
        adds(self.fa, self.ufb, ufloat(-22.720, 4.000))
        adds(self.fb, self.ufb, ufloat(14.560, 4.000))

    def test_sub(self):
        ''' sub ufloat - ufloat '''
        subs(self.ufa, self.ufa, ufloat( 0.000, 0.000))
        subs(self.ufa, self.ufb, ufloat(-6.000, 5.000))
        subs(self.ufb, self.ufb, ufloat( 0.000, 0.000))
        subs(self.ufb, self.ufa, ufloat( 6.000, 5.000))

    def test_sub_uint(self):
        ''' sub ufloat - uint '''
        subs(self.ufa, self.uia, ufloat( 0.000, 4.243))
        subs(self.ufa, self.uib, ufloat(-6.000, 5.000))
        subs(self.ufb, self.uia, ufloat( 6.000, 5.000))
        subs(self.ufb, self.uib, ufloat( 0.000, 5.657))
        ''' sub uint - ufloat '''
        subs(self.uia, self.ufa, ufloat( 0.000, 4.243))
        subs(self.uib, self.ufa, ufloat( 6.000, 5.000))
        subs(self.uia, self.ufb, ufloat(-6.000, 5.000))
        subs(self.uib, self.ufb, ufloat( 0.000, 5.657))

    def test_sub_int(self):
        ''' sub ufloat - int '''
        subs(self.ufa, self.ia, ufloat( 0.000, 3.000))
        subs(self.ufa, self.ib, ufloat(-6.000, 3.000))
        subs(self.ufb, self.ia, ufloat( 6.000, 4.000))
        subs(self.ufb, self.ib, ufloat( 0.000, 4.000))
        ''' sub int - ufloat '''
        subs(self.ia, self.ufa, ufloat( 0.000, 3.000))
        subs(self.ib, self.ufa, ufloat( 6.000, 3.000))
        subs(self.ia, self.ufb, ufloat(-6.000, 4.000))
        subs(self.ib, self.ufb, ufloat( 0.000, 4.000))

    def test_sub_float(self):
        ''' sub ufloat - float '''
        subs(self.ufa, self.fa, ufloat( 20.720, 3.000))
        subs(self.ufa, self.fb, ufloat(-16.560, 3.000))
        subs(self.ufb, self.fa, ufloat( 26.720, 4.000))
        subs(self.ufb, self.fb, ufloat(-10.560, 4.000))
        ''' sub float - ufloat'''
        subs(self.fa, self.ufa, ufloat(-20.720, 3.000))
        subs(self.fb, self.ufa, ufloat( 16.560, 3.000))
        subs(self.fa, self.ufb, ufloat(-26.720, 4.000))
        subs(self.fb, self.ufb, ufloat( 10.560, 4.000))
        
    def test_mul(self):
        ''' mul ufloat * ufloat '''
        muls(self.ufa, self.ufa, ufloat(16.000, 16.971))
        muls(self.ufa, self.ufb, ufloat(-8.000, 17.088))
        muls(self.ufb, self.ufb, ufloat( 4.000, 11.314))
        muls(self.ufb, self.ufa, ufloat(-8.000, 17.088))
        
    def test_mul_uint(self):
        ''' mul ufloat * uint '''
        muls(self.ufa, self.uia, ufloat(16.000, 16.971))
        muls(self.ufa, self.uib, ufloat(-8.000, 17.088))
        muls(self.ufb, self.uia, ufloat(-8.000, 17.088))
        muls(self.ufb, self.uib, ufloat( 4.000, 11.314))
        ''' mul uint * ufloat '''
        muls(self.uia, self.ufa, ufloat(16.000, 16.971))
        muls(self.uib, self.ufa, ufloat(-8.000, 17.088))
        muls(self.uia, self.ufb, ufloat(-8.000, 17.088))
        muls(self.uib, self.ufb, ufloat( 4.000, 11.314))

    def test_mul_int(self):
        ''' mul ufloat * int '''
        muls(self.ufa, self.ia, ufloat(16.000, 12.000))
        muls(self.ufa, self.ib, ufloat(-8.000,  6.000))
        muls(self.ufb, self.ia, ufloat(-8.000, 16.000))
        muls(self.ufb, self.ib, ufloat( 4.000,  8.000))
        ''' mul int * ufloat '''
        muls(self.ia, self.ufa, ufloat(16.000, 12.000))
        muls(self.ib, self.ufa, ufloat(-8.000,  6.000))
        muls(self.ia, self.ufb, ufloat(-8.000, 16.000))
        muls(self.ib, self.ufb, ufloat( 4.000,  8.000))

    def test_mul_float(self):
        ''' mul ufloat * float '''
        muls(self.ufa, self.fa, ufloat( 98.880, 74.160))
        muls(self.ufa, self.fb, ufloat(-50.240, 37.680))
        muls(self.ufb, self.fa, ufloat(-49.440, 98.880))
        muls(self.ufb, self.fb, ufloat( 25.120, 50.240))
        ''' mul float * ufloat '''
        muls(self.fa, self.ufa, ufloat( 98.880, 74.160))
        muls(self.fb, self.ufa, ufloat(-50.240, 37.680))
        muls(self.fa, self.ufb, ufloat(-49.440, 98.880))
        muls(self.fb, self.ufb, ufloat( 25.120, 50.240))

    def test_div(self):
        ''' div ufloat / ufloat '''
        divs(self.ufa, self.ufa, ufloat( 1.000, 0.000))
        divs(self.ufa, self.ufb, ufloat(-2.000, 4.528))
        divs(self.ufb, self.ufb, ufloat( 1.000, 0.000))
        divs(self.ufb, self.ufa, ufloat(-0.500, 2.035))
        
    def test_div_uint(self):
        ''' div ufloat / uint '''
        divs(self.ufa, self.uia, ufloat( 1.000, 1.677))
        divs(self.ufa, self.uib, ufloat(-2.000, 4.528))
        divs(self.ufb, self.uia, ufloat(-0.500, 2.035))
        divs(self.ufb, self.uib, ufloat( 1.000, 3.464))
        ''' div uint / ufloat '''
        divs(self.uia, self.ufa, ufloat( 1.000, 1.677))
        divs(self.uib, self.ufa, ufloat(-0.500, 2.035))
        divs(self.uia, self.ufb, ufloat(-2.000, 4.528))
        divs(self.uib, self.ufb, ufloat( 1.000, 3.464))

    def test_div_int(self):
        ''' div ufloat / int '''
        divs(self.ufa, self.ia, ufloat( 1.000, 0.750))
        divs(self.ufa, self.ib, ufloat(-2.000, 1.500))
        divs(self.ufb, self.ia, ufloat(-0.500, 1.000))
        divs(self.ufb, self.ib, ufloat( 1.000, 2.000))
        ''' div int / ufloat '''
        divs(self.ia, self.ufa, ufloat( 1.000, 0.188))
        divs(self.ib, self.ufa, ufloat(-0.500, 0.188))
        divs(self.ia, self.ufb, ufloat(-2.000, 1.000))
        divs(self.ib, self.ufb, ufloat( 1.000, 1.000))

    def test_div_float(self):
        ''' div ufloat / float '''
        divs(self.ufa, self.fa, ufloat( 0.162, 0.121))
        divs(self.ufa, self.fb, ufloat(-0.318, 0.239))
        divs(self.ufb, self.fa, ufloat(-0.081, 0.162))
        divs(self.ufb, self.fb, ufloat( 0.159, 0.318))
        ''' div float / ufloat '''
        divs(self.fa, self.ufa, ufloat(  6.180, 0.188))
        divs(self.fb, self.ufa, ufloat(- 3.140, 0.188))
        divs(self.fa, self.ufb, ufloat(-12.360, 1.000))
        divs(self.fb, self.ufb, ufloat(  6.280, 1.000))

    def test_floordiv(self):
        ''' floordiv ufloat // ufloat '''
        floordivs(self.ufa, self.ufa, ufloat( 1.000, 0.000))
        floordivs(self.ufa, self.ufb, ufloat(-2.000, 4.528))
        floordivs(self.ufb, self.ufb, ufloat( 1.000, 0.000))
        floordivs(self.ufb, self.ufa, ufloat(-1.000, 2.035))
        
    def test_floordiv_uint(self):
        ''' floordiv ufloat // uint '''
        floordivs(self.ufa, self.uia, ufloat( 1.000, 1.677))
        floordivs(self.ufa, self.uib, ufloat(-2.000, 4.528))
        floordivs(self.ufb, self.uia, ufloat(-1.000, 2.035))
        floordivs(self.ufb, self.uib, ufloat( 1.000, 3.464))
        ''' floordiv uint // ufloat '''
        floordivs(self.uia, self.ufa, ufloat( 1.000, 1.677))
        floordivs(self.uib, self.ufa, ufloat(-1.000, 2.035))
        floordivs(self.uia, self.ufb, ufloat(-2.000, 4.528))
        floordivs(self.uib, self.ufb, ufloat( 1.000, 3.464))

    def test_floordiv_int(self):
        ''' floordiv ufloat // int '''
        floordivs(self.ufa, self.ia, ufloat( 1.000, 0.750))
        floordivs(self.ufa, self.ib, ufloat(-2.000, 1.500))
        floordivs(self.ufb, self.ia, ufloat(-1.000, 1.000))
        floordivs(self.ufb, self.ib, ufloat( 1.000, 2.000))
        ''' floordiv int // ufloat '''
        floordivs(self.ia, self.ufa, ufloat( 1.000, 0.188))
        floordivs(self.ib, self.ufa, ufloat(-1.000, 0.188))
        floordivs(self.ia, self.ufb, ufloat(-2.000, 1.000))
        floordivs(self.ib, self.ufb, ufloat( 1.000, 1.000))

    def test_floordiv_float(self):
        ''' floordiv ufloat // float '''
        floordivs(self.ufa, self.fa, ufloat( 0.000, 0.121))
        floordivs(self.ufa, self.fb, ufloat(-1.000, 0.239))
        floordivs(self.ufb, self.fa, ufloat(-1.000, 0.162))
        floordivs(self.ufb, self.fb, ufloat( 0.000, 0.318))
        ''' floordiv float // ufloat '''
        floordivs(self.fa, self.ufa, ufloat(  6.000, 0.188))
        floordivs(self.fb, self.ufa, ufloat(- 4.000, 0.188))
        floordivs(self.fa, self.ufb, ufloat(-13.000, 1.000))
        floordivs(self.fb, self.ufb, ufloat(  6.000, 1.000))

    def test_neg(self):
        ''' neg - '''
        negs(self.ufa, ufloat( 4.000, 3.000))
        negs(self.ufb, ufloat(-2.000, 4.000))
        negs(self.uia, ufloat( 4.000, 3.000))
        negs(self.uib, ufloat(-2.000, 4.000))     

    def test_pow(self):
        ''' pow ** '''
        pows(self.ufa, 2, ufloat(   16.000,   24.000))
        pows(self.ufa, 3, ufloat(  -64.000,  144.000))
        pows(self.ufa, 5, ufloat(-1024.000, 3840.000))
        pows(self.ufb, 2.50, ufloat( 5.657,  28.284))
        pows(self.ufb, 3.25, ufloat( 9.514,  61.839))
        pows(self.ufb, 5.03, ufloat(32.672, 328.684))


    '''
        Functions
    '''
    def test_abs(self):
        ''' abs '''
        abss(self.ufa, ufloat( 4.0, 3.0))
        abss(self.ufb, ufloat( 2.0, 4.0))
        abss(self.ufc, ufloat(23.0, 5.3))

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

    def test_max(self):
        ''' max '''
        t(max(self.ufa, self.ufb, self.ufc), self.ufc)
        t(max(abs(self.ufa), abs(self.ufb), abs(self.ufc)), self.ufc)
        t(max(ufloat(2.2, 12), ufloat(1.3, 12), ufloat(3.7, 12), ufloat(5.3, 12), ufloat(3.1, 12), ufloat(2.6, 12), ufloat(0.6, 12), ufloat(4.4, 12)), ufloat(5.3, 12))
        t(max(ufloat(2.2, 12), ufloat(-1.3, 12), ufloat(3.7, 12), ufloat(5.3, 12), ufloat(-3.1, 12), ufloat(2.6, 12), ufloat(-0.6, 12), ufloat(4.4, 12)), ufloat(5.3, 12))
        t(max(2, ufloat(-1, 12), 3, ufloat(5, 12), -3, ufloat(2, 12), ufloat(-0, 12), 6), 6)
        t(max(2, uint(-1, 1), ufloat(-3.5, 1.0), uint(3, 1), -2, uint(0, 1), -4, ufloat(5.5, 1.7)), ufloat(5.5, 1.7))

    def test_min(self):
        ''' min '''
        t(min(self.ufa, self.ufb, self.ufc), self.ufa)
        t(min(abs(self.ufa), abs(self.ufb), abs(self.ufc)), self.ufb)
        t(min(ufloat(2.2, 1), ufloat(1.3, 1), ufloat(3.7, 1), ufloat(3.3, 1), ufloat(2.1, 1), ufloat(0.6, 1), ufloat(4.6, 1), ufloat(5.4, 1)), ufloat(0.6, 1))
        t(min(ufloat(2.2, 1), ufloat(-1.3, 1), ufloat(3.7, 1), ufloat(3.3, 1), ufloat(-2.1, 1), ufloat(0.6, 1), ufloat(-4.6, 1), ufloat(5.4, 1)), ufloat(-4.6, 1))
        t(min(2, ufloat(-1, 1), -3, ufloat(3, 1), -2, ufloat(0, 1), -4, -5), -5)
        t(min(2, uint(-1, 1), ufloat(-3.5, 1.0), uint(3, 1), -2, uint(0, 1), -4, ufloat(-5.5, 1.7)), ufloat(-5.5, 1.7))
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