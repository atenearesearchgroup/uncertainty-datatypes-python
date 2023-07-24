from __future__ import annotations

import math

from uncertainty.utypes import uint
from uncertainty.utypes import ufloat
from uncertainty.ubool import ubool

THRESHOLD = 0.95

class ustr:
	
    # Instance attributes:
    # str: str 
    # c: float 

    def __init__(self, string: str, c: float|int = 1.0) -> ustr:
        if isinstance(string, (str, int, uint, float, ufloat, ubool)):
            if c < 0 or c > 1:
                raise ValueError('Invalid parameter: c is c < 0 or c > 1. c=' + c)
        else:
            raise ValueError('Invalid parameter: string is not str')
        
        self.string = string
        self._c = c

    @property
    def value(self):
        return self._string

    @property
    def confidence(self):
        return self._c

    ''' Auxiliary operations '''
    def __confToDist(self):
        return len(self.string) * (1 - self._c)

    def __confToDist(self, conf: float = None, size: int = None):
        if conf is None:
            conf = self._c
        if size is None:
            size = len(self.string)

        if conf < 0.0 or conf > 1.0:
            raise ValueError('Invalid parameter: c is c < 0 or c > 1. conf=' + conf)
        return size * (1 - conf)

    def __distToConf(self, dist: float, size: int) -> float:
        return max(1 - dist / size, 0.0)  

    def __str__(self) -> str:
        return 'ustr({:s}, {:5.3f})'.format(self.string, self._c)

    def __repr__(self) -> str:
        return self.__str__()

    def __levenshteinDist(a: str, b: str) -> int:
        a = a.lower()
        b = b.lower()
        costs : list[int] = [j for j in range(len(b) + 1)]
        
        for i in range(len(a)):
            costs[0] = i
            nw: int = i - 1
            for j in range(len(b)):
                cj: int = min(1 + min(costs[j], costs[j - 1]), nw if a[i - 1] == b[j - 1] else nw + 1)
                nw = costs[j]
                costs[j] = cj

        return costs[len(b)]
    
    ''' ustr operations '''
    def concat(self, u: ustr|str) -> ustr:
        if not isinstance(u, ustr):
            u = ustr(u)

        s: str = self.string + u.string
        auxDist: float = self.__confToDist() + u.__confToDist()
        c: float = self.__distToConf(auxDist, len(self.string) + len(u.string))
        return ustr(s, c)

    def __add__(self, other) -> ustr:
        return self.concat(other)

    def __radd__(self, left) -> ustr:
        if not isinstance(left, ustr):
            left = ustr(left)
        return left.concat(self)

    def uSubstring(self, lower: int = 0, upper: int = None, step: int = 1) -> ustr:
        if upper is None:
            upper = len(self.string)
       
        return ustr(self.string[lower: upper: step], self._c)
    
    def __getitem__(self, idx) -> ustr:
        if isinstance(idx, int):
            return self.uAt(idx)
        elif isinstance(idx, slice):
            return self.uSubstring(idx.start, idx.stop, idx.step)

    def uEquals(self, u: ustr) -> ubool:
        if id(self) == id(u):
            return ubool(1.0)
        
        c = self.calculateConf(u)
        if self.string == u.string:
            return ubool(c)
        else:
            return ubool(1 - c)
        
    def eq(self, r: ustr) -> ubool:
        return self.uEquals(r)
    
    def __eq__(self, r: ustr) -> ubool:
        return self.uEquals(r)

    def uDistinct(self, u: ustr) -> ubool:
        return self.uEquals(u).NOT()
    
    def ne(self, r: ustr) -> ubool:
        return self.uDistinct(r)
    
    def __ne__(self, r: ustr) -> ubool:
        return self.uDistinct(r)
        
    def uEqualsIgnoreCase(self, u: ustr) -> ubool:
        return self.upper().uEquals(u.upper())
    
    def equals(self, other) -> bool:
        if (id(self) == id(other)): 
            return True
        elif other is None or not isinstance(other, self.__class__): 
            return False
        elif not math.isclose(self._c, other.confidence, rel_tol = 0.001, abs_tol = 0.001): 
            return False
        return self.string == other.string
    
    def lt(self, u: ustr) -> ubool:
        c = self.calculateConf(u)
        return ubool(c if self.string < u.string else 1 - c)

    def __lt__(self, u: ustr) -> ubool:
        return self.lt(u)

    def gt(self, u: ustr) -> ubool:
        c = self.calculateConf(u)
        return ubool(c if self.string > u.string else 1 - c)

    def __gt__(self, u: ustr) -> ubool:
        return self.gt(u)

    def le(self, u: ustr) -> ubool:
        c = self.calculateConf(u)
        return ubool(c if self.string <= u.string else 1 - c)

    def __le__(self, u: ustr) -> ubool:
        return self.le(u)

    def ge(self, u: ustr) -> ubool:
        c = self.calculateConf(u)
        return ubool(c if self.string >= u.string else 1 - c)

    def __ge__(self, u: ustr) -> ubool:
        return self.ge(u)
    
    def __len__(self) -> int:
        return len(self.string)
    
    def ulen(self) -> uint:
        return uint(len(self.string), self.__confToDist())
    
    def uUpper(self) -> ustr:
        return ustr(self.string.upper(), self._c)

    def uLower(self) -> ustr:
        return ustr(self.string.lower(), self._c)
    
    def uCapitalize(self) -> ustr:
        return ustr(self.string.capitalize(), self._c)

    def uFirstLower(self) -> ustr:
        return ustr(self.string[0].lower() + self.string[1:], self._c)

    def index(self, s: str) -> uint:
        return self.string.index(s)
    
    def at(self, idx: int) -> str:
        if idx < 0 or idx > len(self.string):
            raise IndexError('idx = ' + idx)
        return self.string[idx: idx + 1]

    def uAt(self, idx: int) -> ustr:
        return self.uSubstring(idx, idx + 1)

    def uCharacters(self) -> list[str]:
        return [self.uAt(i) for i in range(len(self.string))]
    
    ''' Conversion operations '''
    def toString(self) -> str:
        return self.string
    
    def tofloat(self) -> float:
        return float(self.string)
    
    def __float__(self) -> int:
        return self.tofloat()
    
    def toufloat(self) -> float:
        return ufloat(float(self.string), self._c)

    def toint(self) -> int:
        return int(self.string) 
    
    def __int__(self) -> int:
        return self.toint()
    
    def touint(self) -> float:
        return uint(int(self.string), self._c)

    def tobool(self) -> bool:
        if self.string.lower() == 'true' or self.string.lower() == 'false':
            return bool(self.string.lower() == 'true')
    
        raise ValueError('String is not True/False. string=' + str(self.string))
    
    def __bool__(self) -> int:
        return self.toint()

    def toubool(self) -> ubool:
        rTrue: ubool = self.uLower().uEquals(ustr('true', 1.0))
        rFalse: ubool = self.uLower().uEquals(ustr('false', 1.0))
    
        if rTrue.confidence >= 0.5:
            return ubool(rTrue.confidence)
        elif rFalse.confidence >= 0.5:
            return ubool(rFalse.confidence)
        
        raise ValueError('String is not True/False. string=' + str(self.string))

    '''
      La confianza es el producto de las confianzas del string
      Aparecen problemas para confianzas inferiores a 0.7 porque para resultados de confianza menor a 0.5
      'conmuta' de True a False y viceversa
    '''
    def calculateConf(self, u: ustr) -> float:
        return self._c * u.confidence 	# conf producto de las confianzas de cada string
    
    '''
        Posible implementacion alternativa, limitando para los casos peores a conf = 0.5
        No se usa en la ultima version
     '''
    def calculateConf_05(self, u: ustr) -> float:
        conf : float = self._c * u.confidence 	# conf producto de las confianzas de cada string
        return conf if conf > 0.5 else 0.5 

    def copy(self) -> ustr:
        return ustr(self.string, self._c)