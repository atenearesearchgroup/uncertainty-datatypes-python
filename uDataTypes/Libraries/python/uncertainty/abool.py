from __future__ import annotations

from collections.abc import Iterable

from uncertainty.afuncs import *

class abool:

    # Instance attributes:
    # c: float
    # sample : Iterable[bool]

    def __init__(self, c: int|float|Iterable = 0.0) -> abool:
        if isinstance(c, (int, float)):
            if c < 0.0 or c > 1.0: 
                raise ValueError('Invalid parameter: c < 0.0 or c > 1.0. c=' + c)
            self._c = float(c)
            self._sample = createboolSample(np.empty(shape=BOOL_SAMPLE_SIZE, dtype=bool), self._c)
        elif isinstance(c, str):
            c = float(c)
            if c < 0.0 or c > 1.0: 
                raise ValueError('Invalid parameter: c < 0.0 or c > 1.0. c=' + c)
            self._c = c
            self._sample = createboolSample(np.empty(shape=BOOL_SAMPLE_SIZE, dtype=bool), self._c)
        elif isinstance(c, bool):
            self._c = 1.0 if c else 0.0
            self._sample = createboolSample(np.empty(shape=BOOL_SAMPLE_SIZE, dtype=bool), self._c)
        elif isinstance(c, ubool):
            self._c = c.uncertainty
            self._sample = createboolSample(np.empty(shape=BOOL_SAMPLE_SIZE, dtype=bool), self._c)
        elif isinstance(c, Iterable):
            c_temp = self.__extractConfidence(c)
            self._sample = createboolSample(np.empty(shape=BOOL_SAMPLE_SIZE, dtype=bool), c_temp)
            for i in range(len(c)):
                self._sample[i] = c[i]
            self._c = self.__extractConfidence()
        else:
            raise ValueError('Invalid parameter c: not [bool], bool, ubool or number[0.0, 1.0]. C=' + c)
        

    ''' Auxiliary operations '''
    def __extractConfidence(self, data: Iterable[bool] = None) -> float:
        if data is None:
            return self.__extractConfidence(self._sample)
    
        numTrue: int = 0
        for b in data:
            if b:
                numTrue += 1
        
        return numTrue / len(data)     

    @property
    def c(self) -> float:
        return self._c

    ''' Type operations '''    
    def getMaxLength(self, r: abool):
        if self._sample.size == r.size:
            return self._sample.size
        elif self._sample.size != r.size:
            raise ValueError('Different array size: ' + str(self._sample.size) + ' - ' + str(len(r)))

    def AND(self, o: abool) -> abool:
        length: int = self.getMaxLength(o._sample)
        andSample: list[bool] = np.empty(shape=self._sample.size, dtype=bool)
        for i in range(length):
            andSample[i] = self._sample[i] & o._sample[i]
        
        return abool(andSample)

    def __and__(self, other) -> abool:
        return self.AND(other)
    
    def __rand__(self, left) -> abool:
        return abool(left).AND(self)
    
    def OR(self, o: abool) -> abool:
        length: int = self.getMaxLength(o._sample)
        orSample: list[bool] = np.empty(shape=self._sample.size, dtype=bool)
        for i in range(length):
            orSample[i] = self._sample[i] | o._sample[i]
        
        return abool(orSample)

    def __or__(self, other) -> abool:
        if callable(other):
            return NotImplemented
        return self.OR(other)

    def __ror__(self, left) -> abool:
        return abool(left).OR(self)
    
    def IMPLIES(self, o: abool) -> abool:
        length: int = self.getMaxLength(o._sample)
        impliesSample: list[bool] = np.empty(shape=self._sample.size, dtype=bool)
        for i in range(length):
            impliesSample[i] = (not self._sample[i]) | o._sample[i]
        
        return abool(impliesSample)
    
    def XOR(self, other: abool) -> abool:
        return self.EQUIVALENT3(other).NOT()

    #  XOR	(X AND NOT Y) OR (NOT X AND Y)
    def XOR2(self, other: abool) -> abool:
        u1: abool = self.AND(other.NOT())
        u2: abool = self.NOT().AND(other)

        return u1.OR(u2)
    
    def __xor__(self, other) -> abool:
        return self.XOR(other)
    
    def __rxor__(self, left) -> abool:
        return abool(left).XOR(self)
    
    def NOT(self) -> abool:
        notSample: list[bool] = np.empty(shape=self._sample.size, dtype=bool)
        for i in range(len(notSample)):
            notSample[i] = not self._sample[i]

        return abool(notSample)
    
    def __invert__(self) -> abool:
        return self.NOT()
    
    def __rshift__(self, other) -> abool:
        return self.IMPLIES(other)

    def __rrshift__(self, left) -> abool:
        return abool(left).IMPLIES(self)
    
    #  equivalent
    def EQUIVALENT(self, other: abool) -> abool:
        return self.IMPLIES(other).AND(other.IMPLIES(self))
    
    #  equivalent	(X AND Y) OR (NOT X AND NOT Y)
    def EQUIVALENT2(self, other: abool) -> abool:
        u1: abool = self.AND(other)
        u2: abool = self.NOT().AND(other.NOT())
        
        return u1.OR(u2)
    
    def EQUIVALENT3(self, other: abool) -> abool:
        return self.XOR2(other).NOT()
    
    def equals(self, o) -> abool:
        return self.EQUIVALENT(o)

    def __eq__(self, other) -> abool:
        return self.equals(other)
    
    def DISTINCT(self, o) -> abool: 
        return self.EQUIVALENT(o).NOT()
    
    def distinct(self, o) -> abool: 
        return self.DISTINCT(o)
    
    def __ne__(self, other) -> abool:
        return self.distinct(other)
    
    '''Conversions'''
    def __str__(self) -> str:
        return 'abool({:5.3f}, {:s})'.format(self._c, str(self._sample))
    
    def __repr__(self) -> str:
        return self.__str__()

    def toubool(self) -> ubool:
        return ubool(self._c)
    
    def tobool(self) -> bool:
        return self._c > ubool.CERTAINTY

    '''Other Methods '''
    def __hash__(self):
        return 1 if self.tobool() else 0 
    
    def copy(self) -> abool:
        return abool(self._sample)