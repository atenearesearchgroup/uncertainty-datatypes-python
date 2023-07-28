import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class aboolTest(unittest.TestCase):

    def setUp(self):
        self.a = abool(0.623)
        self.b = abool('0.823')
        self.c = abool([True, False, True, False])

    def test_init(self):
        ''' init '''
        t(abool(0.923), abool(0.923))
        t(abool('0.923'), abool(0.923))
        t(abool([True, False, True, False]), abool(0.500))

    def test_not(self):
        ''' NOT '''
        nots(self.a, abool(1 - self.a.c))
        nots(self.b, abool(1 - self.b.c))
        nots(self.c, abool(1 - self.c.c))
        
    def test_ands(self):
        ''' AND '''
        ands(self.a, self.b, abool(self.a.toubool() & self.b.toubool()))
        ands(self.a, self.c, abool(self.a.toubool() & self.c.toubool()))
        ands(self.b, self.c, abool(self.b.toubool() & self.c.toubool()))
        
    def test_ors(self):
        ''' OR '''
        ors(self.a, self.b, abool(self.a.toubool() | self.b.toubool()))
        ors(self.a, self.c, abool(self.a.toubool() | self.c.toubool()))
        ors(self.b, self.c, abool(self.b.toubool() | self.c.toubool()))
        
    def test_xors(self):
        ''' XOR '''
        xors(self.a, self.b, abool(self.a.toubool() ^ self.b.toubool()))
        xors(self.a, self.c, abool(self.a.toubool() ^ self.c.toubool()))
        xors(self.b, self.c, abool(self.b.toubool() ^ self.c.toubool()))

    def test_implies(self):
        ''' Implies '''
        impliess(self.a, self.b, abool(self.a.toubool() >> self.b.toubool()))
        impliess(self.a, self.c, abool(self.a.toubool() >> self.c.toubool()))
        impliess(self.b, self.c, abool(self.b.toubool() >> self.c.toubool()))

    def test_equivalent(self):
        ''' Equivalent '''
        equivalents(self.a, self.b, abool(self.a.toubool() == self.b.toubool()))
        equivalents(self.a, self.c, abool(self.a.toubool() == self.c.toubool()))
        equivalents(self.b, self.c, abool(self.b.toubool() == self.c.toubool()))

    def test_distinct(self):
        ''' Distinct '''
        distincts(self.a, self.b, abool(self.a.toubool() != self.b.toubool()))
        distincts(self.a, self.c, abool(self.a.toubool() != self.c.toubool()))
        distincts(self.b, self.c, abool(self.b.toubool() != self.c.toubool()))

if __name__ == '__main__':
    unittest.main()