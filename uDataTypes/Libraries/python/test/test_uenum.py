import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class uenumTest(unittest.TestCase):

    def setUp(self):
        self.ar = uenum(["water", "what"], [0.8, 0.923])
        self.br = uenum(["good", "bad"], [0.3, 0.453])
        self.cr = uenum({"red": 0.8, "green": 0.771})
        self.dr = uenum({"yellow": 0.3, "blue": 0.852})
        self.er = uenum([ustr("black", 0.83), ustr("white", 0.7)])

    def test_elements(self):
        ''' elements '''
        t(self.ar.elements, {"water": 0.8, "what": 0.923})
        t(self.br.elements, {"good": 0.3, "bad": 0.453})
        t(self.cr.elements, {"red": 0.8, "green": 0.771})
        t(self.dr.elements, {"yellow": 0.3, "blue": 0.852})
        t(self.er.elements, {"black": 0.83, "white": 0.7})

    def test_literals(self):
        ''' literals '''
        t(self.ar.literals, ["water", "what"])
        t(self.br.literals, ["good", "bad"])
        t(self.cr.literals, ["red", "green"])
        t(self.dr.literals, ["yellow", "blue"])
        t(self.er.literals, ["black", "white"])

if __name__ == '__main__':
    unittest.main()