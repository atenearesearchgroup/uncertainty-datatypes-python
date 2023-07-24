import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class aboolTest(unittest.TestCase):

    def setUp(self):
        self.ar = abool(0.623)
        self.br = abool('0.823')
        self.cr = abool([True, False, True, False])

    def test_init(self):
        t(abool(0.923), abool(0.923))
        t(abool('0.923'), abool(0.923))
        t(abool([True, False, True, False]), abool(0.500))

    def test_not(self):
        ''' NOT '''
        nots(self.ar, abool(1 - self.ar.c))
        nots(self.br, abool(1 - self.br.c))
        nots(self.cr, abool(1 - self.cr.c))
        
    def test_ands(self):
        ''' AND '''
        ands(self.ar, self.br, abool(self.ar.toubool() & self.br.toubool()))
        ands(self.ar, self.cr, abool(self.ar.toubool() & self.cr.toubool()))
        ands(self.br, self.cr, abool(self.br.toubool() & self.cr.toubool()))
        
    def test_ors(self):
        ''' OR '''
        ors(self.ar, self.br, abool(self.ar.toubool() | self.br.toubool()))
        ors(self.ar, self.cr, abool(self.ar.toubool() | self.cr.toubool()))
        ors(self.br, self.cr, abool(self.br.toubool() | self.cr.toubool()))
        
    def test_xors(self):
        ''' XOR '''
        xors(self.ar, self.br, abool(self.ar.toubool() ^ self.br.toubool()))
        xors(self.ar, self.cr, abool(self.ar.toubool() ^ self.cr.toubool()))
        xors(self.br, self.cr, abool(self.br.toubool() ^ self.cr.toubool()))

    def test_implies(self):
        ''' Implies '''
        impliess(self.ar, self.br, abool(self.ar.toubool() >> self.br.toubool()))
        impliess(self.ar, self.cr, abool(self.ar.toubool() >> self.cr.toubool()))
        impliess(self.br, self.cr, abool(self.br.toubool() >> self.cr.toubool()))

    def test_equivalent(self):
        ''' Equivalent '''
        equivalents(self.ar, self.br, abool(self.ar.toubool() == self.br.toubool()))
        equivalents(self.ar, self.cr, abool(self.ar.toubool() == self.cr.toubool()))
        equivalents(self.br, self.cr, abool(self.br.toubool() == self.cr.toubool()))

    def test_distinct(self):
        ''' Distinct '''
        distincts(self.ar, self.br, abool(self.ar.toubool() != self.br.toubool()))
        distincts(self.ar, self.cr, abool(self.ar.toubool() != self.cr.toubool()))
        distincts(self.br, self.cr, abool(self.br.toubool() != self.cr.toubool()))

if __name__ == '__main__':
    unittest.main()