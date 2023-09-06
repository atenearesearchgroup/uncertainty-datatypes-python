from __future__ import annotations

from enum import Enum

import random
import math
import numpy as np

from collections.abc import Iterable
from uncertainty.utypes import *

MAX_LENGTH: int = 100000
BOOL_SAMPLE_SIZE: int = 10000
#BOOL_SAMPLE_SIZE: int = 10000000

class Distribution(Enum):
    UNIFORM = 1; TRIANGULAR = 2; TRUNCATED = 3; NORMAL = 4; USHAPED = 5

def nextTruncated(x: float, u: float, beta: float) -> float:
    b: float = x + u * math.sqrt(6 / (1 - beta * beta))
    a: float = 2 * x - b
    r1: float = random.random()
    r2: float = random.random()
    return a + (b-a) * ((1 + beta) * r1 + (1 - beta) * r2)/2

def nextTriangular(x: float, u: float) -> float:
    b: float = x + u * math.sqrt(6)
    a: float = 2 * x - b
    r1: float = random.random()
    r2: float = random.random()
    return a + (b-a) * (r1 + r2)/2

def nextUShaped(x: float, u: float) -> float:
    r: float = random.random()
    return x + u * math.sqrt(2) * math.sin(2 * math.PI * r)

def createSample(s: Iterable[float|int], x1: float, u1: float, dist: Distribution, toInt: bool = False, length: int = MAX_LENGTH):
    # fills the sample with values from the given distribution
    d: float = u1 * math.sqrt(3)
    match dist:
        case Distribution.UNIFORM:
            for i in range(length):
                value = (x1 - d) + 2 * d * random.random()
                s[i] = math.trunc(value) if toInt else value
        case Distribution.NORMAL:
            for i in range(length):
                value = x1 + random.gauss() * u1
                s[i] = math.trunc(value) if toInt else value
        case Distribution.TRIANGULAR:
            for i in range(length):
                value = nextTriangular(x1, u1)
                s[i] = math.trunc(value) if toInt else value
        case Distribution.TRUNCATED:
            beta: float = 2/3 # ratio between the lengths of the top of the trapezoid and of the base
            for i in range(length):
                value = nextTruncated(x1, u1, beta)
                s[i] = math.trunc(value) if toInt else value
        case Distribution.USHAPED:
            for i in range(length):
                value = nextUShaped(x1, u1)
                s[i] = math.trunc(value) if toInt else value
        #  Uniform distribution by deafult
        case _:
            for i in range(length):
                value = (x1 - d) + 2 * d * random.random()
    return s

def createfloatSample(x1: float, u1: float, dist: Distribution = Distribution.UNIFORM):
    s: Iterable[float] = np.empty(MAX_LENGTH, dtype = float)
    createSample(s, x1, u1, dist)
    return s

def createintSample(x1: float, u1: float, dist: Distribution = Distribution.UNIFORM):
    s: Iterable[int] = np.empty(MAX_LENGTH, dtype = int)
    createSample(s, x1, u1, dist, True)
    return s

def createZeroSample(dtype):
    return np.zero(MAX_LENGTH, dtype = dtype)

def createfloatZeroSample():
    return createZeroSample(dtype = float)

def createintZeroSample():
    return createZeroSample(dtype = int)

def createboolSample(s: Iterable[bool], c: float):
    if c < 0.0 or c > 1.0:
        raise ValueError('Invalid parameters')
    
    for i in range(BOOL_SAMPLE_SIZE):
        s[i] = (random.random() - c) <= 0
    return s