from __future__ import annotations
    
class ubool:

    CERTAINTY: float = 0.9

    # Instance attributes:
    # c: float 

    '''	Initializer '''	       
    def __init__(self, c: int|float|bool|str|ubool = 0.0) -> ubool:
        if isinstance(c, str):
            if 'True' == c.capitalize():
                c = True
            elif 'False' == c.capitalize():
                c = False

        if isinstance(c, (int, float, str)):
            c = float(c)
            if c < 0.0 or c > 1.0: 
                raise ValueError('Invalid parameter: c < 0.0 or c > 1.0. c=' + c)
            self.c = float(c)
        elif isinstance(c, bool):
            self.c = 1.0 if c else 0.0
        elif isinstance(c, ubool):
            self.c = c.c
        else:
            raise ValueError('Invalid parameter c: not bool, ubool, str or number[0.0, 1.0]. C=' + c)
     
    @property   
    def u(self, u: int|float|str = None):
        if u is None:
            return self._c
        
        if not isinstance(u, (int, float, str)):
            raise ValueError('Invalid parameter c: not a number[0.0, 1.0]. c=' + u)
        self._c = float(u)
    
    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, c: int|float|str):
        if not isinstance(c, (int, float, str)):
            raise ValueError('Invalid parameter c: not a number[0.0, 1.0]. c=' + c)
        self._c = float(c)
            
    def setCertainty(certainty: float|int):
        if not isinstance(certainty, (int, float)):
            raise ValueError('Invalid parameter: certainty is not an integer or float [0.0, 1.0].')
        
        if certainty < 0.0 or certainty > 1.0:
            raise ValueError('Invalid parameter: certainty is an integer and c < 0 or c > 1. C=')
        
        ubool.CERTAINTY = float(certainty)

    def certainty() -> float:
        return ubool.CERTAINTY

    ''' Type Operations '''
    ''' Not (c) = (1-c)'''
    def NOT(self) -> ubool:
        return ubool(1 - self.c)
    
    def __invert__(self) -> ubool:
        return self.NOT()
    
    def __neg__(self) -> ubool:
        return self.NOT()
           
    def AND(self, o) -> ubool:
        if (id(self) == id(o)):
            return ubool(self.c) # x and x
        
        if not isinstance(o, ubool):
            o = ubool(o)

        return ubool(self.c * o.c)

    def __and__(self, other) -> ubool:
        return self.AND(other)
    
    def __rand__(self, left) -> ubool:
        return ubool(left).AND(self)

    def OR(self, o: ubool|bool|int|float) -> ubool:
        if (id(self) == id(o)):
            return ubool(self.c) # x or x
        
        if not isinstance(o, ubool):
            o = ubool(o)

        return ubool(self.c + o.c - (self.c * o.c))

    def __or__(self, other) -> ubool:
        if callable(other):
            return NotImplemented
        return self.OR(other)

    def __ror__(self, left) -> ubool:
        return ubool(left).OR(self)
    
    def IMPLIES(self, o) -> ubool:
        if (id(self) == id(o)):
            return ubool(self.c) # x implies x

        return ubool((1-self.c) + o.c - ((1 - self.c) * o.c))
    
    def __rshift__(self, other) -> ubool:
        return self.IMPLIES(other)

    def __rrshift__(self, left) -> ubool:
        return ubool(left).IMPLIES(self)

    def EQUIVALENT(self, o) -> ubool:
        return self.XOR(o).NOT()

    def XOR(self, o) -> ubool:
        if not isinstance(o, ubool):
            o = ubool(o)

        return ubool(abs(self.c - o.c))

    def __xor__(self, other) -> ubool:
        return self.XOR(other)
    
    def __rxor__(self, left) -> ubool:
        return ubool(left).XOR(self)

    def EQUALS(self, o) -> ubool:
        return self.EQUIVALENT(o)
    
    def equals(self, o) -> ubool:
        return self.EQUALS(o)

    def __eq__(self, other) -> ubool:
        return self.EQUALS(other)
    
    def DISTINCT(self, o) -> ubool: 
        return self.EQUALS(o).NOT()
    
    def distinct(self, o) -> ubool: 
        return self.DISTINCT(o)
    
    def __ne__(self, other) -> ubool:
        return self.DISTINCT(other)

    ''' Comparison operations '''

    def equalsC(self, o, conf) -> bool:
        return abs(self.c - o.c) <= (1 - conf)

    ''' Other Methods  '''
    def compareTo(self, o) -> int:
        x = self.c - o.c
        if (abs(x) < 0.001): return 0
        if (x < 0): return -1
        
        return 1    

    def copy(self) -> ubool:
        return ubool(self.c)

    ''' Conversions '''
    def __str__(self) -> str:
        return 'ubool({:5.3f})'.format(self.c)
    
    def __repr__(self) -> str:
        return self.__str__()

    def tobool(self, c: float = None) -> bool:
        if c is None:
            c = self.__class__.CERTAINTY
        return self.c >= c
    
    def __bool__(self) -> bool:
        return self.tobool()