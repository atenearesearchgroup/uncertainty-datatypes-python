import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class sboolTest(unittest.TestCase):

    def setUp(self):
        self.x = sbool(0.7, 0.1, 0.2, 0.5)
        self.y = sbool(0.85, 0.05, 0.10, 0.9)
        self.z = sbool(ubool(0.7))
        self.w = sbool(ubool(0.3))
        self.r = sbool(0.2, 0.6, 0.2, 0.5)
        self.g = sbool(0.6, 0.2, 0.2, 0.5)
        
        self.t = sbool()
        self.f = sbool(False)
        self.b = sbool(0.7, 0.1, 0.2, 0.5)
        self.b0 = sbool(0.85, 0.05, 0.10, 0.9)
        self.b1 = sbool(ubool(0.7))
        self.b2 = sbool(ubool(0.3))
        self.b3 = sbool(0.2, 0.6, 0.2, 0.5)
        self.b4 = sbool(0.6, 0.2, 0.2, 0.5)
        self.b5 = sbool(0.154, 0.150, 0.696, 0.1)

        self.c1= sbool(0.55, 0.3, 0.15, 0.38)
        self.c2 = sbool(0.6, 0.3, 0.1, 0.38)
        self.c3 = sbool(0.7, 0.2, 0.1, 0.38)
        self.c4 = sbool(0.8, 0.1, 0.1, 0.38)
        self.c5 = sbool(0.9, 0.05, 0.05, 0.38)

    def test_init(self):
        t(sbool(),                   sbool(1.000, 0.000, 0.000, 1.000))
        t(sbool(sbool()),            sbool(1.000, 0.000, 0.000, 1.000))
        t(sbool(ubool(0.75)),        sbool(0.750, 0.250, 0.000, 0.750))
        t(sbool(0.7, 0.1, 0.2, 0.5), sbool(0.700, 0.100, 0.200, 0.500))

    '''
        Operators
    '''
    def test_and(self):
        ''' AND '''
        ands(self.x, self.y, sbool(0.668, 0.145, 0.187, 0.450))
        ands(self.z, self.w, sbool(0.210, 0.790, 0.000, 0.210))
        ands(self.r, self.g, sbool(0.173, 0.680, 0.147, 0.250))

    def test_and_booleans(self):
        ''' AND Booleans'''
        ands(self.x, True,  sbool(0.700, 0.100, 0.200, 0.500))
        ands(self.x, False, sbool(0.000, 1.000, 0.000, 0.000))
        ands(True, self.x,  sbool(0.700, 0.100, 0.200, 0.500))
        ands(False, self.x, sbool(0.000, 1.000, 0.000, 0.000))

    def test_or(self):
        ''' OR '''
        ors(self.x, self.y, sbool(0.955, 0.010, 0.035, 0.950))
        ors(self.z, self.w, sbool(0.790, 0.210, 0.000, 0.790))
        ors(self.r, self.g, sbool(0.680, 0.173, 0.147, 0.750))
       
    def test_or_booleans(self):
        ''' OR Booleans '''
        ors(self.x, True,  sbool(1.000, 0.000, 0.000, 1.000))
        ors(self.x, False, sbool(0.700, 0.100, 0.200, 0.500))
        ors(True, self.x,  sbool(1.000, 0.000, 0.000, 1.000))
        ors(False, self.x, sbool(0.700, 0.100, 0.200, 0.500))

    def test_not(self):
        ''' OR Booleans '''
        nots(self.x, sbool(0.100, 0.700, 0.200, 0.500))
        nots(self.y, sbool(0.050, 0.850, 0.100, 0.100))
        nots(self.z, sbool(0.300, 0.700, 0.000, 0.300))
        nots(self.w, sbool(0.700, 0.300, 0.000, 0.700))

    def test_xor(self):
        ''' XOR '''
        xors(self.x, self.y, sbool(0.150, 0.830, 0.020, 0.400))
        xors(self.z, self.w, sbool(0.400, 0.600, 0.000, 0.400))
        xors(self.r, self.g, sbool(0.400, 0.560, 0.040, 0.000))

    def test_xor_booleans(self):
        ''' XOR Booleans '''
        xors(self.x, True,  sbool(0.300, 0.700, 0.000, 0.500))
        xors(self.x, False, sbool(0.700, 0.300, 0.000, 0.500))
        xors(True, self.x,  sbool(0.300, 0.700, 0.000, 0.500))
        xors(False, self.x, sbool(0.700, 0.300, 0.000, 0.500))

    def test_implies(self):
        ''' impliess '''
        impliess(self.x, self.y, sbool(0.865, 0.043, 0.092, 0.950))
        impliess(self.z, self.w, sbool(0.510, 0.490, 0.000, 0.510))
        impliess(self.r, self.g, sbool(0.840, 0.067, 0.093, 0.750))

    def test_equals(self):
        ''' Equals '''
        equalss(self.x, self.x, True)
        equalss(self.x, self.w, False)
        equalss(self.w, self.y, False)
        equalss(self.w, self.w, True)
        equalss(self.g, self.r, False)
        equalss(self.r, self.g, False)
        equalss(self.r, self.r, True)

    def test_distinct(self):
        ''' Distinct '''   
        distincts(self.w, self.y, True)
        distincts(self.x, self.w, True)
        distincts(self.w, self.x, True)
        distincts(self.w, self.w, False)
        distincts(self.g, self.r, True)
        distincts(self.r, self.g, True)
        distincts(self.r, self.r, False)

    def test_uncertainty_maximized(self):
        ''' uncertainty maximized '''
        uncertainty_maximized(self.t)
        uncertainty_maximized(self.f)
        uncertainty_maximized(self.b)
        uncertainty_maximized(self.b0)
        uncertainty_maximized(self.b1)
        uncertainty_maximized(self.b2)
        uncertainty_maximized(self.b3)
        uncertainty_maximized(self.b4)
        uncertainty_maximized(self.b5)
        uncertainty_maximized(self.c1)
        uncertainty_maximized(self.c2)
        uncertainty_maximized(self.c3)
        uncertainty_maximized(self.c4)
        uncertainty_maximized(self.c5)

    def test_or_and_uncertainty_maximized(self):
        ''' uncertainty maximized '''
        uncertainty_maximized(self.t |OR| self.f)
        uncertainty_maximized(self.t |AND| self.f)
        uncertainty_maximized(self.t |OR| self.b1)
        uncertainty_maximized(self.t |AND| self.b1)
        uncertainty_maximized(self.b3 |OR| self.b4)
        uncertainty_maximized(self.b3 |AND| self.b4)    
        uncertainty_maximized(self.b1 |XOR| self.b2)
        uncertainty_maximized(self.b1 |EQUIVALENT| self.b2)
        uncertainty_maximized(self.b3 |XOR| self.b4)
        uncertainty_maximized(self.b3 |EQUIVALENT| self.b4)
        uncertainty_maximized(self.b3.IMPLIES(self.b4).AND(self.b4.IMPLIES(self.b3)))
        uncertainty_maximized(sbool(0.75, 0.15, 0.1, 0.5).OR(sbool(0.35, 0, 0.65, 0.2)))
        uncertainty_maximized(sbool(0.837, 0.065, 0.098, 0.6))

    def test_deduceY(self):
        deducey_given(
            sbool(0.0, 0.0, 1, 0.8), 
            sbool(0.4, 0.5, 0.1, 0.4), 
            sbool(0.0, 0.4, 0.6, 0.4),
            sbool(0.320, 0.480, 0.200, 0.400) 
        )

        deducey_given(
            sbool(0.10, 0.8, 0.1, 0.8), 
            sbool(0.4, 0.5, 0.1, 0.4),
            sbool(0.0, 0.4, 0.6, 0.4),
            sbool(0.072, 0.418, 0.510, 0.400) 
        )

        deducey_given(
            sbool(0.0, 0.40, 0.6, 0.5), 
            sbool(0.55, 0.3, 0.15, 0.38), 
            sbool(0.1, 0.75, 0.15, 0.38),
            sbool(0.151, 0.48, 0.369, 0.382) 
        )

    def test_weighted_belief_fusion(self):
        ''' Weighted belief fusion '''
        opinions = [self.c1, self.c2, self.c3, self.c4, self.c5]

        uncertainty_maximized(sbool.weightedOpinionsFusion(opinions))        	    
        uncertainty_maximized_equals(sbool.majorityOpinionsFusion(opinions), sbool(1, 0, 0, 0.5))
        uncertainty_maximized_equals(sbool.minimumOpinionsFusion(opinions), sbool(0.55, 0.3, 0.15, 0.38))
        uncertainty_maximized_equals(sbool.averagingOpinionsFusion(opinions), sbool(0.753, 0.159, 0.088, 0.38))
        uncertainty_maximized_equals(sbool.aleatoryCumulativeOpinionsFusion(opinions), sbool(0.810, 0.171, 0.019, 0.38))
        uncertainty_maximized_equals(sbool.epistemicCumulativeOpinionsFusion(opinions), sbool(0.705, 0.0, 0.295, 0.38))
        uncertainty_maximized_equals(sbool.cbOpinionsFusion(opinions), sbool(0.997, 0.003, 0, 0.38))
        
    def test_consensus_And_Compromise_Fusion(self):
        ''' consensus And Compromise Fusion '''
        opinions = [self.c1, self.c2, self.c3, self.c4, self.c5]

        uncertainty_maximized_equals(sbool.ccOpinionsFusion(opinions), sbool(0.564, 0.057, 0.379, 0.380))
        uncertainty_maximized_equals(sbool.cbOpinionsFusion(opinions), sbool(0.997, 0.003, 0.000, 0.380))
    
    def test_tfui(self):       
        ''' '''
        r = sbool(1, 0, 0, 0.5) # True but with 0.5 mass
        f = sbool(0, 1, 0, 0.5) # False but with 0.5 mass
        u = sbool(0, 0, 1, 0.5) # the Vacuous opinion
        i = sbool(0.5, 0.5, 0, 0.5) # Dogmatic ignorance

        tf = [f, r]

        ccf = sbool.ccOpinionsFusion(tf)
        uncertainty_maximized(ccf)
        t(u,ccf)

        acf = sbool.averagingOpinionsFusion(tf)
        uncertainty_maximized(acf)
        t(i,acf)

        accf = sbool.aleatoryCumulativeOpinionsFusion(tf)
        uncertainty_maximized(accf)
        t(i, accf)

        eccf = sbool.epistemicCumulativeOpinionsFusion(tf)
        uncertainty_maximized(eccf)
        t(u, eccf)

        wcf = sbool.weightedOpinionsFusion(tf)
        uncertainty_maximized(wcf)
        t(i, wcf)

        t(r.ccFusion(u), u)
        t(f.ccFusion(u), u)
        t(r.ccFusion(r), r)
        t(f.ccFusion(f), f)
        t(u.ccFusion(u), u)
        t(u.ccFusion(r), u)
        t(u.ccFusion(f), u)
        t(u.ccFusion(i), u)
        t(i.ccFusion(i), i)
        t(i.ccFusion(u), u)
        t(i.ccFusion(r), sbool(0.5,0.0,0.5,0.5))
        t(i.ccFusion(f), sbool(0.0,0.5,0.5,0.5))

        res = sbool(0.25, 0.15, 0.6, 0.5)
        uncertainty_maximized(res)
        t(res.ccFusion(u) ,res)
        t(u.ccFusion(res) ,res)
        t(res.ccFusion(res) ,res)

    def testOpinionsThree(self):
        ''' Opinions Three '''
        opinions = [sbool(0.1,0.3,0.6,0.5), sbool(0.4,0.2,0.4,0.5), sbool(0.7,0.1,0.2,0.5)]
                
        uncertainty_maximized_equals(sbool.ccOpinionsFusion(opinions), sbool(0.629, 0.182, 0.189, 0.5) )
        uncertainty_maximized_equals(sbool.cbOpinionsFusion(opinions), sbool(0.738, 0.184, 0.078, 0.5))
        uncertainty_maximized_equals(sbool.averagingOpinionsFusion(opinions), sbool(0.509, 0.164, 0.327, 0.5))
        uncertainty_maximized_equals(sbool.aleatoryCumulativeOpinionsFusion(opinions), sbool(0.651, 0.209, 0.140, 0.5))
        uncertainty_maximized_equals(sbool.epistemicCumulativeOpinionsFusion(opinions), sbool(0.442, 0, 0.558, 0.5))
        uncertainty_maximized_equals(sbool.weightedOpinionsFusion(opinions), sbool(0.562, 0.146, 0.292, 0.5))

    def test_cbFusion(self):
        uno = sbool(0.9, 0.1, 0, 0.5)
        dos = sbool(0.1, 0.9, 0, 0.5)
        res = sbool(0.5, 0.5, 0, 0.5) 
        uncertainty_maximized(uno)
        uncertainty_maximized(dos)
        uncertainty_maximized(res)
        t(0.8, uno.degreeOfConflict(dos))
        t(0.8, dos.degreeOfConflict(uno))
        t(res, uno.cbFusion(dos))

    def test_average_fusion1(self):
        ''' Average Fusion '''
        uno = sbool(0.9,0.1,0,0.5)
        dos = sbool(0.1,0.9,0,0.5)
        t(uno.averagingFusion(dos), sbool(0.5,0.5,0,0.5))

        opinions = [uno, dos]
        t(sbool.averagingOpinionsFusion(opinions), sbool(0.5,0.5,0,0.5))

    def test_average_fusion2(self):
        ''' Average Fusion '''
        opinions = [sbool(0.1,0.3,0.6,0.5), sbool(0.4,0.2,0.4,0.5), sbool(0.7,0.1,0.2,0.5)]
        t(sbool.averagingOpinionsFusion(opinions), sbool(0.509,0.164,0.327,0.5))
        t(sbool.ccOpinionsFusion(opinions), sbool(0.629,0.182,0.189,0.5))
        t(sbool.cbOpinionsFusion(opinions), sbool(0.738,0.184,0.078,0.5))
        t(sbool.aleatoryCumulativeOpinionsFusion(opinions), sbool(0.651,0.209,0.140,0.5))
        t(sbool.epistemicCumulativeOpinionsFusion(opinions), sbool(0.442,0,0.558,0.5))
        t(sbool.weightedOpinionsFusion(opinions), sbool(0.562,0.146,0.292,0.5))

        t(sbool(0.33,0.33,0.34,0.5).averagingFusion(sbool(0.33,0.33,0.34,0.5)), sbool(0.33,0.33,0.34,0.5))
        t(sbool(0.35,0.15,0.5,0.5).averagingFusion(sbool(0.15,0.55,0.3,0.5)), sbool(0.225,0.4,0.375,0.5)) 
        t(sbool(0.9,0.1,0,0.5).averagingFusion(sbool(0.1,0.9,0,0.5)), sbool(0.5,0.5,0,0.5))
        t(sbool(0.9,0.1,0,0.5).averagingFusion(sbool(0.1,0.9,0,0.5)), sbool(0.5,0.5,0,0.5))

    def test_random_opinion(self):
        ''' Random Opinion '''
        adam = sbool(0.0,0.95,0.05,0.5)
        beth = sbool(0.0,0.33,0.67,0.5)
        charles = sbool(0.67,0.0,0.33,0.5)
        diana = sbool(0.95,0.0,0.05,0.5)

        opinions = []
        for i in range(18): opinions.append(adam) 
        for i in range(114): opinions.append(beth) 
        for i in range(33): opinions.append(charles) 
        for i in range(34): opinions.append(diana) 

        acf = sbool.averagingOpinionsFusion(opinions)
        wcf = sbool.weightedOpinionsFusion(opinions)
        uncertainty_maximized(acf)
        uncertainty_maximized(wcf)

    def test_discount(self):
        ''' Discount '''
        AonB = sbool(0.0, 0.0, 1, 0.9) 
        uncertainty_maximized(AonB) 
        BonX = sbool(0.95, 0, 0.05, 0.20) 
        uncertainty_maximized(BonX)

        t(BonX.discount(AonB), sbool(0.855, 0, 0.145, 0.2)) 
        uncertainty_maximized(BonX.discount(AonB))

        AonB = sbool(0.2, 0.4, 0.4, 0.75)  
        uncertainty_maximized(AonB) 
        BonX = sbool(0.45, 0.35, 0.20, 0.25) 
        uncertainty_maximized(BonX)

        uncertainty_maximized(BonX.discount(AonB))
        t(BonX.discount(AonB), sbool(0.225, 0.175, 0.6, 0.25) )
        
        A1onX = sbool(0.45, 0.35, 0.20, 0.25) 
        uncertainty_maximized(BonX.discount(A1onX))
        opinions = []

        A2onA1 = sbool(0.95, 0, 0.05, 0.5) 
        uncertainty_maximized(BonX.discount(A2onA1))
        opinions.append(A2onA1)
        t(A1onX.discount(opinions), sbool(0.439, 0.341, 0.22, 0.25))

        A3onA2 = sbool(0.95, 0, 0.05, 0.5) 
        uncertainty_maximized(BonX.discount(A3onA2))
        opinions.append(A3onA2)
        t(A1onX.discount(opinions), sbool(0.428, 0.333, 0.24, 0.25))
        
        A4onA3 = sbool(0.95, 0, 0.05, 0.5) 
        uncertainty_maximized(BonX.discount(A4onA3))
        opinions.append(A4onA3)
        t(A1onX.discount(opinions), sbool(0.417, 0.324, 0.259, 0.25))

        A1onX = sbool(0.8, 0.2, 0.0, 0.1) 
        opinions = []
        opinions.append(sbool(0.2, 0.1, 0.7, 0.8))
        t(A1onX.discount(opinions), sbool(0.608, 0.152, 0.240, 0.1))
        opinions.append(sbool(0.2, 0.1, 0.7, 0.8))
        t(A1onX.discount(opinions), sbool(0.462, 0.116, 0.422, 0.1))
        opinions.append(sbool(0.2, 0.1, 0.7, 0.8))
        t(A1onX.discount(opinions), sbool(0.351, 0.088, 0.561, 0.1) )
		
    def test_fusion(self):
        ''' weightedFusion, cumulativeFusion y epistemicCumulativeFusion'''
        a = sbool(0.300, 0.100, 0.600, 0.900)
        b = sbool(0.000, 0.000, 1.000, 0.500)

        t(a.weightedFusion(b), sbool(0.300, 0.100, 0.600, 0.900))
        t(a.aleatoryCumulativeFusion(b), sbool(0.300, 0.100, 0.600, 0.900))
        t(a.epistemicCumulativeFusion(b), sbool(0.000, 0.067, 0.933, 0.900))

        q = sbool(0.400, 0.000, 0.600, 0.000)
        w = sbool(0.000, 0.000, 1.000, 0.500)
        t(q.weightedFusion(w), sbool(0.400, 0.000, 0.600, 0.000))
        t(q.aleatoryCumulativeFusion(w), sbool(0.400, 0.000, 0.600, 0.000))
        t(q.epistemicCumulativeFusion(w), sbool(0.400, 0.000, 0.600, 0.000))

        r = sbool(0.800, 0.000, 0.200, 0.800)
        g = sbool(0.000, 0.000, 1.000, 0.500)
        t(r.weightedFusion(g), sbool(0.800, 0.000, 0.200, 0.800))
        t(r.aleatoryCumulativeFusion(g), sbool(0.800, 0.000, 0.200, 0.800))
        t(r.epistemicCumulativeFusion(g), sbool(0.800, 0.000, 0.200, 0.800))

def uncertainty_maximized(x: sbool):
    t(x.uncertaintyMaximized().projection(), x.projection())
    t(x.uncertaintyMaximized().isMaximizedUncertainty(), True)

def deducey_given(x, yGivenX, yGivenNotX, res):
    y = x.deduceY(yGivenX, yGivenNotX) 
    uncertainty_maximized(x) 
    uncertainty_maximized(yGivenX)
    uncertainty_maximized(yGivenNotX)
    uncertainty_maximized(y)
    uncertainty_maximized(res)
    t(res, y)

def uncertainty_maximized_equals(x, e):
    uncertainty_maximized(x)
    uncertainty_maximized(e)
    t(x, e)

if __name__ == '__main__':
    unittest.main()

