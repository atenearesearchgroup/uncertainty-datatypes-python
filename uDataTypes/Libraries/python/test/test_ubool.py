import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

def execute(l, r, e, func, special_op, method, op, rev_op):
    t(func(l, r), e)            #   AND(l, r)
    t(l |special_op| r, e)      #   l |AND| r
    if isinstance(l, ubool): 
        t(method(l, r), e)      #   l.AND(r)
        t(op(l, r),     e)      #   l & r
    elif isinstance(r, ubool): 
        t(rev_op(l, r), e)      #   True & r

def ands(l, r, e):
    execute(l, r, e, AND, AND, ubool.AND, ubool.__and__, ubool.__rand__)

def ors(l, r, e):
    execute(l, r, e, OR, OR, ubool.OR, ubool.__or__, ubool.__ror__)

def xors(l, r, e):
    execute(l, r, e, XOR, XOR, ubool.XOR, ubool.__xor__, ubool.__rxor__)

def implies(l, r, e):
    execute(l, r, e, IMPLIES, IMPLIES, ubool.IMPLIES, ubool.__rshift__, ubool.__rrshift__)

def equivalent(l, r, e):
    execute(l, r, e, EQUIVALENT, EQUIVALENT, ubool.EQUIVALENT, ubool.__eq__, ubool.__eq__)

def equals(l, r, e):
    execute(l, r, e, EQUALS, EQUALS, ubool.EQUALS, ubool.__eq__, ubool.__eq__)

def distinct(l, r, e):
    execute(l, r, e, DISTINCT, DISTINCT, ubool.DISTINCT, ubool.__ne__, ubool.__ne__)

def nots(l, e):
    t(NOT(l),  e)
    t(l.NOT(), e)
    t(~l,      e)

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
        ''' Implies '''
        implies(self.w, self.x, ubool(0.910))
        implies(self.x, self.w, ubool(0.510))

    def test_equivalent(self):
        ''' Equivalent '''
        equivalent(self.x, self.w, ubool(0.600))
        equivalent(self.w, self.x, ubool(0.600))
        equivalent(self.w, self.w, ubool(1.000))
        equivalent(self.t, self.f, ubool(0.000))
        equivalent(self.f, self.t, ubool(0.000))
    
    def test_equals(self):
        ''' Equals '''
        equals(self.x, self.w, ubool(0.600))
        equals(self.w, self.y, ubool(0.900))
        equals(self.w, self.w, ubool(1.000))
        equals(self.t, self.f, ubool(0.000))
        equals(self.f, self.t, ubool(0.000))

    def test_distinct(self):
        ''' Distinct '''   
        distinct(self.w, self.y, ubool(0.100))
        distinct(self.x, self.w, ubool(0.400))
        distinct(self.w, self.x, ubool(0.400))
        distinct(self.t, self.f, ubool(1.000))
        distinct(self.f, self.t, ubool(1.000))


if __name__ == '__main__':
    unittest.main()

