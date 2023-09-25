from __future__ import annotations
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import unittest

from uncertainty.utypes import *
from .funcs_testing import *


TEST_FOLDER = 'test'
TEST_FILES_FOLDER = 'test-files'

ARROW = '->'
LINE_COMMENT = '#'

class TestExpression:

    def __init__(self, expression: str = None, expectedResult: str = None) -> TestExpression:
        self.expression = expression
        self.expectedResult = expectedResult

    def test(self):
        t(exec(self.expression), exec(self.expectedResult))

    def isEmpty(self):
        return self.expression is None or self.expectedResult is None

    def __truth__(self):
        return self.isEmpty()

def isLine(pattern):
    return lambda l : l.startswith(pattern)

isCommentLine = isLine(LINE_COMMENT)
isExpectedResultLine = isLine(ARROW)

def readExpresionLine(f):
    testExpr = TestExpression()
    line = f.readline()

    while line and testExpr.isEmpty():    
        line = line.strip()

        if line and not isCommentLine(line):
            if testExpr.expression is None:
                if isExpectedResultLine(line):
                    raise ValueError('Missing expression.')
                
                testExpr.expression = line
            else:
                if not isExpectedResultLine(line):
                    raise ValueError('Missing expected result line.')

                testExpr.expectedResult = line[line.index(ARROW) + 2:]

        if testExpr.expectedResult is None:
            line = f.readline()

    if testExpr.isEmpty():
        return # End of file

    return testExpr

DEBUG = False
class uenumTest(unittest.TestCase):

    def test_files(self):
        dir = os.path.join(os.getcwd(), TEST_FOLDER, TEST_FILES_FOLDER)
        for filename in os.listdir(dir):
            with open(os.path.join(dir, filename), 'r') as f:
                testExpr = readExpresionLine(f)
                while testExpr:
                    with self.subTest():
                        self.checkLine(testExpr)
                    testExpr = readExpresionLine(f)

    def checkLine(self, testExpr):
        res = ''; exp = ''
        exec('res = ' + testExpr.expression + ';' + 'exp = ' + testExpr.expectedResult)

        if res != exp:
            print('Test failed.')
            print('Result:' + '\t' + testExpr.expression + ' == Expected: ' + testExpr.expectedResult + ' ? ' + res == exp + '\n')
        
        testExpr.test()

if __name__ == '__main__':
    unittest.main()
                        