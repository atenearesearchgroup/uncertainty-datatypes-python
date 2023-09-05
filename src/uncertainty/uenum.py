from __future__ import annotations

from collections.abc import Iterable

from uncertainty.utypes import ubool
from uncertainty.utypes import ustr

import math

class uenum:
    
    # Instance attributes:
    # elements: Dict[str, float] = {}

    def __init__(self, literals: Iterable[str], c: Iterable[float] = None):
        if c is None:
            if isinstance(literals, dict):
                self._elements = literals.copy()
            elif isinstance(literals, list):
                self._elements = {}
                for i in range(len(literals)):
                    self._elements[literals[i].string] = literals[i].confidence
        else:
            if len(literals) != len(c):
                raise ValueError('Sizes of the parameters \'literals\' and \'conf\' are not the same.')

            self._elements = {}
            for i in range(len(literals)):
                self._elements[literals[i]] = c[i]
    
    @property
    def elements(self) -> Iterable[str]:
        return self._elements
    
    @property
    def literals(self):
        return [i for i in self._elements.keys()]
    
    @property
    def ustrs(self):
        return [ustr(k, v) for k, v in self._elements.items()]

    def __str__(self) -> str:
        result = 'uenum{' 
        for k in self._elements:
            result += '{}={:5.3f}, '.format(k, self._elements[k])
        
        result += '}'
        return result
    
    def __repr__(self) -> str:
        return self.__str__()

    def equals(self, other: uenum) -> ubool:
        if other is None or self.__class__ != other.__class__:
            return False
        
        return self._elements == other.elements

    def uEquals(self, other: uenum) -> ubool:
        if other is None or self.__class__ != other.__class__:
            return ubool(1.0)

        error = 0.0
        for k in self._elements.keys():
            c1 = self._elements[k]
            c2 = other.elements[k]
            error += (c1-c2) * (c1-c2)  # suma de diferencias al cuadrado
        
        error = math.sqrt(error / 2)

        return ubool(1.0 - error)
    
    def __eq__(self, other: uenum) -> ubool:
        return self.uEquals(other)

    def uDistinct(self, other: uenum):
        return ubool(1 - self.uDistinct(other))
    
    def __ne__(self, other: uenum) -> ubool:
        return self.uDistinct(other)
