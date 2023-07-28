import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class ustrTest(unittest.TestCase):

    def setUp(self):
        self.ustr1 = ustr('What is Lorem Ipsum?', 0.97)
        self.ustr2 = ustr('Lorem Ipsum is simply dummy', 0.75)
        self.ustr3 = ustr('text of the printing and typesetting industry.', 0.85)

    def test_init(self):
        ''' inint '''
        ustr('My string', 0.97)
        ustr('My string', 1)
        ustr('My string')

    def test_add(self):
        ''' concat '''
        adds(self.ustr1, self.ustr2, ustr('What is Lorem Ipsum?Lorem Ipsum is simply dummy', 0.844))
        adds(self.ustr1, self.ustr3, ustr('What is Lorem Ipsum?text of the printing and typesetting industry.', 0.886))
        adds(self.ustr2, self.ustr3, ustr('Lorem Ipsum is simply dummytext of the printing and typesetting industry.', 0.813))
        adds(self.ustr1, 'What is Lorem Ipsum?', ustr('What is Lorem Ipsum?What is Lorem Ipsum?', 0.985))
        adds('What is Lorem Ipsum?', self.ustr1, ustr('What is Lorem Ipsum?What is Lorem Ipsum?', 0.985))

    def test_substring(self):
        ''' substring '''
        t(self.ustr1.uSubstring(0, 4), ustr('What', 0.993))
        t(self.ustr1[0: 4], ustr('What', 0.993))

        t(self.ustr1.uSubstring(0, 4, 2), ustr('Wa', 0.996))
        t(self.ustr1[0: 4: 2], ustr('Wa', 0.996))

        t(self.ustr1.uSubstring(5, 7), ustr('is', 0.996))
        t(self.ustr1[5: 7], ustr('is', 0.996))

        t(self.ustr2.uSubstring(-5), ustr('dummy', 0.796))
        t(self.ustr2[-5:], ustr('dummy', 0.796))
        
        t(self.ustr2.uSubstring(12), ustr('is simply dummy', 0.861))
        t(self.ustr2[12:], ustr('is simply dummy', 0.861))

        t(self.ustr3.uSubstring(-9, -1), ustr('industry', 0.973))
        t(self.ustr3[-9: -1], ustr('industry', 0.973))

        t(self.ustr3.uSubstring(5, 7), ustr('of', 0.993))
        t(self.ustr3[5: 7], ustr('of', 0.993))

    def test_at(self):
        ''' at '''
        t(self.ustr1.at(0), 'W')
        t(self.ustr1[0], 'W')

        t(self.ustr2.at(3), 'e')
        t(self.ustr2[3], 'e')

        t(self.ustr3.at(3), 't')
        t(self.ustr3[3], 't')

    def test_usize(self):
        ''' uSize '''
        t(self.ustr2.ulen(), uint(len(self.ustr2.string), 6.750))
        t(self.ustr3.ulen(), uint(len(self.ustr3.string), 6.900))

        t(len(self.ustr2), len(self.ustr2.string))
        t(len(self.ustr3), len(self.ustr3.string))

    def test_uUpper(self):
        ''' uUpper '''
        t(self.ustr1.uUpper(), ustr('WHAT IS LOREM IPSUM?', 0.97))
        t(self.ustr2.uUpper(), ustr('LOREM IPSUM IS SIMPLY DUMMY', 0.75))
        t(self.ustr3.uUpper(), ustr('TEXT OF THE PRINTING AND TYPESETTING INDUSTRY.', 0.85))

    def test_uLower(self):
        ''' uLower '''
        t(self.ustr1.uLower(), ustr('what is lorem ipsum?', 0.97))
        t(self.ustr2.uLower(), ustr('lorem ipsum is simply dummy', 0.75))
        t(self.ustr3.uLower(), ustr('text of the printing and typesetting industry.', 0.85))

    def test_uCapitalize(self):
        ''' uCapitalize '''
        t(self.ustr1.uCapitalize(), ustr('What is lorem ipsum?', 0.97))
        t(self.ustr2.uCapitalize(), ustr('Lorem ipsum is simply dummy', 0.75))
        t(self.ustr3.uCapitalize(), ustr('Text of the printing and typesetting industry.', 0.85))

    def test_uFirstLower(self):
        ''' uFirstLower '''
        t(self.ustr1.uFirstLower(), ustr('what is Lorem Ipsum?', 0.97))
        t(self.ustr2.uFirstLower(), ustr('lorem Ipsum is simply dummy', 0.75))
        t(self.ustr3.uFirstLower(), ustr('text of the printing and typesetting industry.', 0.85))

    def test_index(self):
        ''' index '''
        t(self.ustr1.index('a'), 2)
        t(self.ustr2.index('m'), 4)
        t(self.ustr3.index('x'), 2)

    def test_toint(self):
        ''' toint '''
        t(ustr('2', 0.8).toint(), 2)
        t(ustr(2, 0.8).toint(), 2)
        t(int(ustr('2', 0.8)), 2)
        t(int(ustr(2, 0.8)), 2)

        t(ustr('20', 0.8).toint(), 20)
        t(ustr(20, 0.8).toint(), 20)
        t(int(ustr('20', 0.8)), 20)
        t(int(ustr(20, 0.8)), 20)
        
        t(ustr('-52', 0.8).toint(), -52)
        t(ustr(-52, 0.8).toint(), -52)
        t(int(ustr('-52', 0.8)), -52)
        t(int(ustr(-52, 0.8)), -52)

    def test_toint(self):
        ''' touint '''
        t(ustr('2', 0.8).touint(), uint(2, 0.8))
        t(ustr(2, 0.8).touint(), uint(2, 0.8))
        t(ustr('20', 0.58).touint(), uint(20, 0.58))
        t(ustr(20, 0.58).touint(), uint(20, 0.58))
        t(ustr('-52', 0.7).touint(), uint(-52, 0.7))
        t(ustr(-52, 0.7).touint(), uint(-52, 0.7))

    def test_tofloat(self):
        ''' tofloat '''
        t(ustr('2.34', 0.8).tofloat(), 2.34)
        t(ustr(2.34, 0.8).tofloat(), 2.34)
        t(float(ustr('2.34', 0.8)), 2.34)
        t(float(ustr(2.34, 0.8)), 2.34)

        t(ustr('20.765', 0.58).tofloat(), 20.765)
        t(ustr(20.765, 0.58).tofloat(), 20.765)
        t(float(ustr('20.765', 0.58)), 20.765)
        t(float(ustr(20.765, 0.58)), 20.765)
        
        t(ustr('-52.3568', 0.7).tofloat(), -52.3568)
        t(ustr(-52.3568, 0.7).tofloat(), -52.3568)
        t(float(ustr('-52.3568', 0.7)), -52.3568)
        t(float(ustr(-52.3568, 0.7)), -52.3568)

    def test_toufloat(self):
        ''' toufloat '''
        t(ustr('2.34', 0.8).toufloat(), ufloat(2.34, 0.8))
        t(ustr(2.34, 0.8).toufloat(), ufloat(2.34, 0.8))
        t(ustr('20.765', 0.58).toufloat(), ufloat(20.765, 0.58))
        t(ustr(20.765, 0.58).toufloat(), ufloat(20.765, 0.58))
        t(ustr('-52.3568', 0.7).toufloat(), ufloat(-52.3568, 0.7))
        t(ustr(-52.3568, 0.7).toufloat(), ufloat(-52.3568, 0.7))

    def test_tobool(self):
        ''' toufloat '''
        t(ustr('True', 0.8).tobool(), True)
        t(ustr('False', 0.8).tobool(), False)

    def test_toubool(self):
        ''' toufloat '''
        t(ustr('True', 0.8).toubool(), ubool(0.8))
        t(ustr('False', 0.8).toubool(), ubool(0.8))

        t(ustr('true', 0.96).toubool(), ubool(0.96))
        t(ustr('false', 0.96).toubool(), ubool(0.96))
        
    def test_lt(self):
        ''' lt < '''
        lts(ustr('T', 0.8), ustr('True', 0.8), ubool(0.640))
        lts(ustr('True', 0.8), ustr('T', 0.8), ubool(0.360))

    def test_lt(self):
        ''' le <= '''
        les(ustr('T', 0.8), ustr('True', 0.8), ubool(0.640))
        les(ustr('True', 0.8), ustr('T', 0.8), ubool(0.360))

    def test_gt(self):
        ''' gt > '''
        gts(ustr('T', 0.8), ustr('True', 0.8), ubool(0.360))
        gts(ustr('True', 0.8), ustr('T', 0.8), ubool(0.640))

    def test_ge(self):
        ''' ge >= '''
        ges(ustr('T', 0.8), ustr('True', 0.8), ubool(0.360))
        ges(ustr('True', 0.8), ustr('T', 0.8), ubool(0.640))

    def test_eq(self):
        ''' eq == '''
        eqs(ustr('True', 0.8), ustr('True', 0.8), ubool(0.640))
        eqs(ustr('False', 0.8), ustr('T', 0.8), ubool(0.360))

    def test_ne(self):
        ''' ne != '''
        nes(ustr('True', 0.8), ustr('True', 0.8), ubool(0.360))
        nes(ustr('False', 0.8), ustr('True', 0.8), ubool(0.640))

if __name__ == '__main__':
    unittest.main()