import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class uboolTest(unittest.TestCase):

    def setUp(self):
        self.x = ubool(0.7)
        self.y = ubool(0.4)
        self.z = ubool(0.6)
        self.w = ubool(0.3)
        self.f = ubool(0.0)
        self.t = ubool(1.0)

    def test_init(self):
        t(ubool(0.7), ubool(0.7))
        t(ubool('0.7'), ubool(0.7))

        t(ubool(0), ubool(0.0))
        t(ubool('0'), ubool(0.0))

        t(ubool(1), ubool(1.0))
        t(ubool('1'), ubool(1.0))

        t(ubool(True), ubool(1.0))
        t(ubool('True'), ubool(1.0))

        t(ubool(False), ubool(0.0))
        t(ubool('False'), ubool(0.0))

    '''
        Operators
    '''
    def test_and(self):
        ''' AND '''
        ands(self.x, self.y, ubool(0.280))
        ands(self.x, self.z, ubool(0.420))
        
    def test_and_booleans(self):
        ''' AND Booleans'''
        ands(self.x, True,  ubool(0.700))
        ands(self.x, False, ubool(0.000))
        ands(True, self.x,  ubool(0.700))
        ands(False, self.x, ubool(0.000))

    def test_or(self):
        ''' OR '''
        ors(self.x, self.z, ubool(0.880))
        ors(self.x, self.y, ubool(0.820))
        
    def test_or_booleans(self):
        ''' OR Booleans '''
        ors(self.x, True, ubool(1.000))
        ors(self.x, False, ubool(0.700))
        ors(True, self.x, ubool(1.000))
        ors(False, self.x, ubool(0.700))

    def test_xor(self):
        ''' XOR '''
        xors(self.x, self.z, ubool(0.100))
        xors(self.x, self.y, ubool(0.300))

    def test_xor_booleans(self):
        ''' XOR Booleans '''
        xors(self.x, True,  ubool(0.300))
        xors(self.x, False, ubool(0.700))
        xors(True, self.x,  ubool(0.300))
        xors(False, self.x, ubool(0.700))

    def test_not(self):
        ''' NOT '''
        nots(self.w, ubool(0.700))
        nots(self.x, ubool(0.300))
        nots(self.t, ubool(0.000))
        nots(self.f, ubool(1.000))

    def test_implies(self):
        ''' impliess '''
        impliess(self.w, self.x, ubool(0.910))
        impliess(self.x, self.w, ubool(0.510))

    def test_equivalent(self):
        ''' Equivalent '''
        equivalents(self.x, self.w, ubool(0.600))
        equivalents(self.w, self.x, ubool(0.600))
        equivalents(self.w, self.w, ubool(1.000))
        equivalents(self.t, self.f, ubool(0.000))
        equivalents(self.f, self.t, ubool(0.000))
    
    def test_equals(self):
        ''' Equals '''
        equalss(self.x, self.w, False)
        equalss(self.w, self.y, False)
        equalss(self.w, self.w, True)
        equalss(self.t, self.f, False)
        equalss(self.f, self.t, False)

    def test_distinct(self):
        ''' Distinct '''   
        distincts(self.w, self.y, True)
        distincts(self.x, self.w, True)
        distincts(self.w, self.x, True)
        distincts(self.w, self.w, False)
        distincts(self.t, self.f, True)
        distincts(self.f, self.t, True)


if __name__ == '__main__':
    unittest.main()

