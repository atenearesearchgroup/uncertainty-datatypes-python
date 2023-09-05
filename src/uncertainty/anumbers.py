from __future__ import annotations

from collections.abc import Iterable

from uncertainty.utypes import *
from uncertainty.afuncs import *

import math

class aint:

    # Instance attributes:
    # x: int 
    # u: float 
    # sample : Iterable[int]
    
    def __init__(self, x: Iterable|int|str = 0.0, u: float|int|str = 0.0, array: Iterable[int] = None, dist: Distribution = Distribution.UNIFORM) -> aint:
        if array is not None: 
            self.__setArray(x, u, np.array(array, dtype=int))
        elif isinstance(x, Iterable):
            self.__initFromArray(x)
        else:
            self.__initFromValues(x, u, dist)

    def __setValues(self, x: int|str, u: float|int|str):
        if not isinstance(x, (int, str)):
            raise ValueError('Invalid parameter: x is not int or float as string')
        elif not isinstance(u, (float, int, str)):
            raise ValueError('Invalid parameter: u is not float, not int or float as string')

        self._x = int(x)
        self._u = float(u)

    def __initFromValues(self, x: int|str, u: float|int|str, dist: Distribution):
        self.__setValues(x, u)

        if self._u == 0.0:
            self._sample = createintSample(self._x, self._u)
        else:
            self._sample = createintSample(self._x, self._u, dist)

    def __initFromArray(self, array: Iterable[int]):
        self._sample = np.array(array, dtype=int)
        sum: int = 0.0 
        dev: float = 0.0
        
        length: float = self._sample.size
        for i in range(length):
            sum += self._sample[i]
            dev += self._sample[i] * self._sample[i]
        
        #  average
        self._x = math.trunc(sum/length)
        # standard deviation
        self._u = math.sqrt(abs(dev - ( sum * sum / length)) / (length - 1))

    def __setArray(self, x: int|str, u: float|int|str, array: Iterable[float]):
        self.__setValues(x, u)
        self._sample = array

    @property
    def value(self) -> int:
        return self._x
    
    @property
    def uncertainty(self) -> float:
        return self._u
    
    def getSample(self) -> Iterable[int]: #gets a copy of the sample
        return self._sample.copy()
    
    def getLength(self, r: aint = None):
        if r is None:
            return self._sample.size
        elif self._sample.size == r._sample.size:
            return self._sample.size
        elif self._sample.size != r._sample.size:
            raise ValueError('Different array size: ' + str(self._sample.size) + ' - ' + str(r._sample.size))
    
    ''' Type Operations '''

    def __operation(self, r: aint|int|float, operation) -> aint:
        if isinstance(r, int):
            return self.execute_operation(operation, None, r)
        elif isinstance(r, float):
            return self.toafloat().execute_operation(operation, None, r)
        elif isinstance(r, afloat):
            return self.toafloat().execute_operation(operation, r)
        else:
            return self.execute_operation(operation, r)
    
    def __create_aint(self, sum: int, dev: float, length: int, result: Iterable) -> aint:
        # average, standard deviation, result
        return aint(int(round(sum / length)), math.sqrt(abs(dev - (sum * sum / length)) / (length - 1)), result)
    
    def execute_operation(self, operation, r: aint = None, n: int = None) -> aint:        
        length: int = self.getLength()

        sum: int =  0 
        dev: float =  0.0

        result = np.empty(shape=length, dtype=int)
        for i in range(length):
            if n is not None:
                result[i] = operation(self._sample[i], n)
            elif r is not None:
                result[i] = operation(self._sample[i], r._sample[i])
            else:
                result[i] = operation(self._sample[i])
            sum += result[i]
            dev += result[i] * result[i]

        return self.__create_aint(sum, dev, length, result)
    
    def add(self, r: aint|int|float) -> aint:
        return self.__operation(r, lambda x, y : x + y)
    
    def __add__(self, r) -> aint:
        return self.add(r)
    
    def __radd__(self, left) -> aint:
        if isinstance(left, int):
            return self.execute_operation(lambda y : left + y)
        elif isinstance(left, float):
            return self.toafloat().execute_operation(lambda y : left + y)

        return left.__add__(self)

    def sub(self, r: aint) -> aint:
        return self.__operation(r, lambda x, y : x - y)

    def __sub__(self, r: aint):
        return self.sub(r)
    
    def __rsub__(self, left) -> aint:
        if isinstance(left, int):
            return self.execute_operation(lambda y : left - y)
        elif isinstance(left, float):
            return self.toafloat().execute_operation(lambda y : left - y)

        return left.__sub__(self)
    
    def mul(self, r: aint) -> aint:
        return self.__operation(r, lambda x, y : x * y)
    
    def __mul__(self, r) -> aint:
        return self.mul(r)
    
    def __rmul__(self, left) -> aint:
        if isinstance(left, int):
            return self.execute_operation(lambda y : left * y)
        elif isinstance(left, float):
            return self.toafloat().execute_operation(lambda y : left * y)
        
        return left.__mul__(self)

    ''' self operation returns a ufloat '''
    def div(self, r: aint) -> ufloat:
        return self.toafloat() / r

    def __truediv__(self, r):
        return self.div(r)
    
    def __rtruediv__(self, left) -> aint:
        if isinstance(left, (int, float)):
            return self.toafloat().execute_operation(lambda y : left / y if y != 0 else 0)
        
        return left.__truediv__(self)

    def floordiv(self, r: aint) -> aint:        
        if isinstance(r, int):
            return self.execute_operation(lambda x : x // r if r != 0 else 0)
        elif isinstance(r, float):
            return self.toafloat().floordiv(r)
        
        return self.__operation(r, lambda x, y : x // y if y != 0 else 0)
    
    def __floordiv__(self, r):
        return self.floordiv(r)

    def __rfloordiv__(self, left):
        if isinstance(left, int):
            return self.execute_operation(lambda y : left // y if y != 0 else 0)
        elif isinstance(left, float):
            return self.toafloat().floordiv(left, True)

        return left.__floordiv__(self)

    def power(self, s: int| float) -> aint:
        length: int = self.getLength()
        sum: int =  0 
        dev: float =  0.0

        result = np.empty(shape=length, dtype=int)
        for i in range(length):
            result[i] = np.trunc(self._sample[i] ** s)
            sum += result[i]
            dev += result[i] * result[i]   

        # average, standard deviation, result
        return self.__create_aint(sum, dev, length, result)
    
    def __pow__(self, s: float|int) -> aint:
        if isinstance(s, float):
            return self.toafloat().execute_operation(lambda x : x**s)
        
        return self.power(s)
    
    def neg(self) -> aint:
        length: int = self.getLength()
        result = np.empty(shape=length, dtype=int)
        for i in range(length):
            result[i] = -self._sample[i]

        return aint(-self._x, self._u, result)
    
    def __neg__(self) -> aint:
        return self.neg()

    ''' 
       FUZZY COMPARISON OPERATIONS
       using 1-to-1 comparisons is not fair, due to possible reorderings
    '''
    def equals(self, number: aint) -> ubool:
        return self.toufloat().uEquals(number.toufloat())
    
    def eq(self, r: uint|ufloat) -> ubool:
        return self.equals(r)
    
    def __eq__(self, r: uint|ufloat) -> ubool:
        return self.equals(r)

    def distinct(self, r: aint) -> ubool:
        return self.equals(r).NOT()
    
    def ne(self, r: uint|ufloat) -> ubool:
        return self.distinct(r)
    
    def __ne__(self, r: uint|ufloat) -> ubool:
        return self.distinct(r)

    def lt(self, number: aint) -> ubool:
        return self.toufloat().lt(number.toufloat())
    
    def __lt__(self, r: uint|ufloat) -> ubool:
        return self.lt(r)
    
    def le(self, number: aint) -> ubool:
        return self.toufloat().le(number.toufloat())

    def __le__(self, r: uint|ufloat) -> ubool:
        return self.le(r)

    def gt(self, number: aint) -> ubool:
        return self.toufloat().gt(number.toufloat())
    
    def __gt__(self, r: uint|ufloat) -> ubool:
        return self.gt(r)

    def ge(self, number: aint) -> ubool:
        return self.toufloat().ge(number.toufloat())
    
    def __ge__(self, r: uint|ufloat) -> ubool:
        return self.ge(r)
   
    '''END OF FUZZY COMPARISON OPERATIONS'''
    
    def abs(self) -> aint:
        length: int = self.getLength()
        sum: int = 0 
        dev: float = 0.0

        result = np.empty(shape=length, dtype=int)
        for i in range(length):
            result[i] = abs(self._sample[i])
            sum += result[i]
            dev += result[i] * result[i]

        # average, standard deviation, result
        return self.__create_aint(sum, dev, length, result)
    
    def __abs__(self) -> aint:
        return self.abs()
    
    def sqrt(self) -> aint:
        length: int = self.getLength()
        sum: int =  0 
        dev: float =  0.0

        result = np.empty(shape=length, dtype=int)
        for i in range(length):
            result[i] = int(math.sqrt(self._sample[i]))
            sum += result[i]
            dev += result[i] * result[i]

        # average, standard deviation, result
        return self.__create_aint(sum, dev, length, result)

    def inverse(self) -> aint: #inverse (reciprocal)
        return aint(1, 0.0).div(self)
    
    ''' Conversions '''
    def __str__(self) -> str:
        return 'aint({:5.3f}, {:5.3f}, {:s})'.format(self._x, self._u, str(self._sample))

    def __repr__(self) -> str:
        return self.__str__()
    
    def toint(self) -> int: #
        return int(self._x)
        
    def toint(self) -> ufloat:
        return uint(self._x, self._u)
    
    def tofloat(self) -> ufloat:
        return float(self._x)
    
    def toufloat(self) -> ufloat:
        return ufloat(self._x, self._u)
    
    def toaint(self) -> aint:
        return self

    def toafloat(self) -> afloat:
        return afloat(self._x, self._u, self._sample)
    
    ''' Other Methods '''
    def __hash__(self):
        return math.round(self._x)

    def copy(self) -> aint:
        return aint(self._x, self._u, self._sample)

class afloat:

    # Instance attributes:
    # x: float 
    # u: float 
    # sample : Iterable[float]
    
    # Instance attributes:
    # x: int 
    # u: float 
    # sample : Iterable[int]
    
    def __init__(self, x: Iterable|int|float|str = 0.0, u: float|int|str = 0.0, array: Iterable[int] = None, dist: Distribution = Distribution.UNIFORM) -> aint:
        if array is not None: 
            self.__setArray(x, u, np.array(array, dtype=float))
        elif isinstance(x, Iterable):
            self.__initFromArray(x)
        else:
            self.__initFromValues(x, u, dist)

    def __setValues(self, x: int|str, u: float|int|str):
        if not isinstance(x, (int, float, str)):
            raise ValueError('Invalid parameter: x is not int or float as string')
        elif not isinstance(u, (int, float, str)):
            raise ValueError('Invalid parameter: u is not float, not int or float as string')

        self._x = float(x)
        self._u = float(u)

    def __initFromValues(self, x: int|str, u: float|int|str, dist: Distribution):
        self.__setValues(x, u)

        if self._u == 0.0:
            self._sample = createintSample(self._x, self._u)
        else:
            self._sample = createintSample(self._x, self._u, dist)

    def __initFromArray(self, array: Iterable[int]):
        self._sample = np.array(array, dtype=float)
        sum: int = 0.0 
        dev: float = 0.0
        
        length: float = self._sample.size
        for i in range(length):
            sum += self._sample[i]
            dev += self._sample[i] * self._sample[i]
        
        #  average
        self._x = sum/length
        # standard deviation
        self._u = math.sqrt(abs(dev - ( sum * sum / length)) / (length - 1))

    def __setArray(self, x: int|str, u: float|int|str, array: Iterable[float]):
        self.__setValues(x, u)
        self._sample = array

    @property
    def value(self) -> int:
        return self._x
    
    @property
    def uncertainty(self) -> float:
        return self._u
    
    def getSample(self) -> Iterable[float]: # gets a copy of the sample
        return self._sample.copy()
    
    def copy(self) -> afloat:
        return afloat(self._x, self._u, self._sample)

    def getLength(self, r: afloat = None):
        if r is None:
            return self._sample.size
        elif self._sample.size == r._sample.size:
            return self._sample.size
        elif self._sample.size != r._sample.size:
            raise ValueError('Different array size: ' + str(self._sample.size) + ' - ' + str(r._sample.size))
        
    ''' Type Operations '''
    def __operation(self, r: int|float|aint, operation) -> afloat:
        if isinstance(r, (int, float)):
            return self.execute_operation(operation, None, r)
        else:
            return self.execute_operation(operation, r)
    
    def __create_afloat(self, sum: int, dev: float, length: int, result: Iterable) -> afloat:
        # average, standard deviation, result
        return afloat(sum / length, math.sqrt(abs(dev - (sum * sum / length)) / (length - 1)), result)
    
    def execute_operation(self, operation, r: aint|afloat = None, n: int|float = None) -> afloat:        
        length: int = self.getLength()

        sum: int =  0 
        dev: float =  0.0

        result = np.empty(shape=length, dtype=float)
        for i in range(length):
            if n is not None:
                result[i] = operation(self._sample[i], n)
            elif r is not None:
                result[i] = operation(self._sample[i], r._sample[i])
            else:
                result[i] = operation(self._sample[i])
            sum += result[i]
            dev += result[i] * result[i]

        return self.__create_afloat(sum, dev, length, result)
    
    def add(self, r: afloat) -> afloat:
        return self.__operation(r, lambda x, y : x + y)
    
    def __add__(self, other) -> afloat:
        return self.add(other)
    
    def __radd__(self, left) -> afloat:
        if isinstance(left, (int, float)):
            return self.execute_operation(lambda y : left + y)
        
        return afloat(left).add(self)

    def sub(self, r: afloat) -> afloat:
        return self.__operation(r, lambda x, y : x - y)

    def __sub__(self, other) -> afloat:
        return self.sub(other)
    
    def __rsub__(self, left) -> afloat:
        if isinstance(left, (int, float)):
            return self.execute_operation(lambda y : left - y)
        
        return afloat(left).__sub__(self)
    
    def mul(self, r: afloat) -> afloat:
        return self.__operation(r, lambda x, y : x * y)
    
    def __mul__(self, other) -> afloat:
        return self.mul(other)
    
    def __rmul__(self, left) -> afloat:
        if isinstance(left, (int, float)):
            return self.execute_operation(lambda y : left * y)
        
        return afloat(left).__mul__(self)
    
    def div(self, r: afloat) -> afloat:
        return self.__operation(r, lambda x, y : x / y if y != 0 else 0)

    def __truediv__(self, other) -> afloat:
        return self.div(other)
    
    def __rtruediv__(self, left) -> ufloat:
        if isinstance(left, (int, float)):
            return self.execute_operation(lambda y : left / y if y != 0 else 0)
        
        return afloat(left).__truediv__(self)

    def floordiv(self, r: afloat, reverse: bool = False) -> afloat:
        length: int = self.getLength()

        sum: int =  0 
        dev: float =  0.0

        result = np.empty(shape=length, dtype=float)
        for i in range(length):
            if isinstance(r, (int, float)):
                if reverse:
                    result[i] = r // self._sample[i] if self._sample[i] != 0 else 0
                else:
                    result[i] = self._sample[i] // r if r != 0 else 0
            elif isinstance(r, (aint, afloat)):
                result[i] = self._sample[i] // r._sample[i] if r._sample[i] != 0 else 0
            sum += result[i]
            dev += result[i] * result[i]

        return afloat(round(sum / length), math.sqrt(abs(dev - (sum * sum / length)) / (length - 1)), result)

    def __floordiv__(self, r):
        return self.floordiv(r)

    def __rfloordiv__(self, left):
        if isinstance(left, (int, float)):
            return self.floordiv(left, True)
        
        return afloat(left).__floordiv__(self)

    def abs(self) -> afloat:
        return self.execute_operation(abs)

    def __abs__(self) -> afloat:
        return self.abs()
    
    def neg(self) -> afloat:
        length: int = self.getLength()
        result = np.empty(shape=length, dtype=float)
        for i in range(length):
            result[i] = -self._sample[i]
    
        return afloat(-self._x, self._u, result)

    def __neg__(self) -> afloat:
        return self.neg()

    def power(self, s: float) -> afloat:
        return self.execute_operation(lambda x: x**s)
    
    def __pow__(self, s: float|int) -> afloat:
        return self.power(s)
    
    def sqrt(self) -> afloat:
        return self.execute_operation(lambda x: math.sqrt(x))
    
    def sin(self) -> afloat:
        return self.execute_operation(lambda x: math.sin(x))
        
    def cos(self) -> afloat:
        return self.execute_operation(lambda x: math.cos(x))
    
    def tan(self) -> afloat:
        return self.execute_operation(lambda x: math.tan(x))
    
    def asin(self) -> afloat:
        return self.execute_operation(lambda x: math.asin(x))
    
    def acos(self) -> afloat:
        return self.execute_operation(lambda x: math.acos(x))
    
    def atan(self) -> afloat:
        return self.execute_operation(lambda x: math.atan(x))

    def inverse(self) -> afloat: # inverse (reciprocal)
        return afloat(1.0).div(self)
    
    def floor(self) -> afloat: # returns (i,u) with i the largest int such that (i,u)<=(x,u)
        s: Iterable[float] = self.getSample()
        newX: float = math.floor(self._x)
        for i in len(s):
            s[i] = newX + (s[i] - self._x) 
        
        return afloat(newX, self._u, s)
    
    def round(self) -> afloat: # returns (i,u) with i the closest int to x
        s: Iterable[float] = self.getSample()
        newX: float = math.round(self._x)
        for i in len(s):
            s[i] = newX + (s[i] - self._x) 
        
        return afloat(newX, self._u, s)
    
    ''' FUZZY COMPARISON OPERATIONS '''

    '''
    self method returns three numbers (lt, eq, gt) with the probabilities that 
        lt: self < number, 
        eq: self = number
        gt: self > number
    '''
    def calculate(self, number: afloat) -> Result:
        length = self.getLength(number)
        res: Result = Result(0.0,0.0,0.0)
    
        for i in len(length):
            if self._sample[i] < number.sample[i]: 
                res.lt += 1
            elif self._sample[i] > number.sample[i]: 
                res.gt += 1
            else: 
                res.eq += 1
        
        res.lt = res.lt/length
        res.gt = res.gt/length
        res.eq = 1.0 - (res.lt + res.gt)
        return res
    
    def equals(self, r: uint|ufloat) -> ubool:
        return self.toufloat().uEquals(r.toufloat())
    
    def eq(self, r: uint|ufloat) -> ubool:
        return self.equals(r)

    def __eq__(self, other) -> ubool:
        return self.equals(other)

    def distinct(self, r: aint) -> ubool:
        return self.equals(r).NOT()
    
    def ne(self, r: uint|ufloat) -> ubool:
        return self.distinct(r)
    
    def __ne__(self, r: uint|ufloat) -> ubool:
        return self.distinct(r)

    def lt(self, number: afloat) -> ubool:
        return self.toufloat().lt(number.toufloat())
    
    def __lt__(self, number: uint|ufloat) -> ubool:
        return self.lt(number)
    
    def le(self, number: afloat) -> ubool:
        return self.toufloat().le(number.toufloat())

    def __le__(self, number: uint|ufloat) -> ubool:
        return self.le(number)

    def gt(self, number: afloat) -> ubool:
        return self.toufloat().gt(number.toufloat())
    
    def __gt__(self, number: uint|ufloat) -> ubool:
        return self.gt(number)
    
    def ge(self, number: afloat) -> ubool:
        return self.toufloat().ge(number.toufloat())
    
    def __ge__(self, number: uint|ufloat) -> ubool:
        return self.ge(number)
    
    ''' Conversions '''
    def __str__(self) -> str:
        return 'afloat({:5.3f}, {:5.3f}, {:s})'.format(self._x, self._u, str(self._sample))

    def __repr__(self) -> str:
        return self.__str__()
    
    def toint(self) -> int:
        return math.floor(self._x)
    
    def tofloat(self) -> float:
        return self._x

    def toufloat(self) -> float:
        return ufloat(self._x, self._u)

    def toaint(self) -> aint:
        return aint(self._x, self._i, round(self._sample))

    def toafloat(self) -> afloat:
        return self
    
    '''Other Methods'''
    def __hash__(self) -> int: # required for equals()
        return math.round(float(self._x))
    
    def copy(self) -> afloat:
        return afloat(self._x, self._u, self._sample)
