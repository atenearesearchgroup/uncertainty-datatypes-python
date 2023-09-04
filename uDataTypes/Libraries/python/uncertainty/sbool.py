from __future__ import annotations

import math

from enum import Enum
from functools import reduce
from collections.abc import Iterable

from uncertainty.utypes import ubool

class Domain(Enum): 
    NIL = 1; TRUE = 2; FALSE = 3; DOMAIN = 4

    def intersect(self, d: Domain) -> Domain:
        match self:
            case Domain.NIL: return Domain.NIL
            case Domain.TRUE:
                match d:
                    case Domain.NIL: return Domain.NIL
                    case Domain.FALSE: return Domain.NIL
                    case Domain.TRUE: return Domain.TRUE
                    case Domain.DOMAIN: return Domain.TRUE
                    case _: raise RuntimeError('unidentified domain')
            case Domain.FALSE:
                match d:
                    case Domain.NIL: return Domain.NIL
                    case Domain.TRUE: return Domain.NIL
                    case Domain.FALSE: return Domain.FALSE
                    case Domain.DOMAIN: return Domain.FALSE
                    case _: raise RuntimeError('unidentified domain')
            case Domain.DOMAIN: return d
            case _: raise RuntimeError('unidentified domain')
           
    def union(self, d: Domain) -> Domain:
        match self:
            case Domain.DOMAIN: return Domain.DOMAIN
            case Domain.TRUE:
                match d:
                    case Domain.TRUE: return Domain.TRUE
                    case Domain.NIL: return Domain.TRUE
                    case Domain.FALSE: return Domain.DOMAIN
                    case Domain.DOMAIN: return Domain.DOMAIN
                    case _: raise RuntimeError('unidentified domain')
            case Domain.FALSE:
                match d:
                    case Domain.FALSE: return Domain.FALSE
                    case Domain.NIL: return Domain.FALSE
                    case Domain.TRUE: return Domain.DOMAIN
                    case Domain.DOMAIN: return Domain.DOMAIN
                    case _: raise RuntimeError('unidentified domain')
            case Domain.NIL: return d
            case _: raise RuntimeError('unidentified domain')


class sbool:

    #b belief mass: degree of belief that self is True
    #d disbelief mass: degree of belief that self is False
    #u uncertainty mass: amount of uncommitted belief  
    #a base rate: prior probability of self being True
    #relative_weight For fusion operations

    def __init__(self, b: bool|ubool|float|str = 1.0, d: float|str = 0.0, u: float|str = 0.0, 
                 a: float|str = 1.0, relative_weight: float|str = 1.0) -> sbool:
        if isinstance(b, bool):
            self._createFromBool(b, relative_weight)
        elif isinstance(b, ubool):
            self._createFromubool(b, relative_weight)
        elif isinstance(b, sbool):
            self._createFromsbool(b)
        else:
            self._createFromFloats(b, d, u, a, relative_weight)

    @property
    def belief(self) -> float:
        return self._b
    
    @property
    def disbelief(self) -> float:
        return self._d 
    
    @property
    def uncertainty(self) -> float:
        return self._u
    
    @property
    def base_rate(self) -> float:
        return self._a

    @property
    def relative_weight(self) -> float:
        return self._relative_weight if self.isDogmatic() else 0.0
    
    @relative_weight.setter
    def relative_weight(self, relative_weight: float):
        self._relative_weight = self.adjust(relative_weight)

    def adjust(self, value: float) -> float:
        return float(round(value * 1000000.0) / 1000000.0)

    def _createFromFloats(self, b: float|str = 1.0, d: float|str = 0.0, u: float|str = 0.0, 
                 a: float|str = 1.0, relative_weight: float|str = 1.0) -> sbool:
        if abs(b + d + u - 1.0) > 0.001 or b < 0.0 or \
            d < 0.0 or u < 0.0 or a < 0.0 or b > 1.0 or \
            d > 1.0 or u > 1.0 or a > 1.0:
            raise ValueError('sbool constructor with relative weight: Invalid parameters. b: ' + str(b) + \
                             ' ,d: ' + str(d) + ' ,u: ' + str(u) + ' ,a: ' + str(a))

        self._b = self.adjust(float(b))
        self._d = self.adjust(float(d))
        self._u = self.adjust(float(u))
        self._a = self.adjust(float(a))
        self._relative_weight = float(self.adjust(relative_weight))

    def _createFromBool(self, b: bool, relative_weight: float):
        if b: self._b = 1.0; self._d = 0.0; self._u = 0.0; self._a = 1.0 # Dogmatic True
        else: self._b = 0.0; self._d = 1.0; self._u = 0.0; self._a = 0.0 # Dogmatic False
        self._relative_weight = relative_weight

    def _createFromubool(self, o: ubool, relative_weight: float): # type embedding -- without uncertainty
        self._b = self.adjust(o.confidence) 
        self._d = 1.0 - self._b 
        self._u = 0.0 
        self._a = self._b
        self._relative_weight = relative_weight

    def _createFromsbool(self, o: sbool): # type embedding -- without uncertainty
        self._b = o._b
        self._d = o._d
        self._u = o._u
        self._a = o._a

    ''' Dogmatic opinions are opinions with complete certainty (i.e., uncertainty = 0). '''
    def createDogmaticOpinion(projection: float, base_rate: float) -> sbool:
        if projection < 0.0 or projection > 1.0 or base_rate < 0.0 or base_rate > 1.0:
            raise ValueError('Create Dogmatic Opinion: Projections and baseRates should be between 0 and 1')
        
        return sbool(projection, 1.0 - projection, 0.0, base_rate)
	
    ''' Vacuous opinions have an uncertainty of 1. '''
    def createVacuousOpinion(projection: float) -> sbool:
        if projection < 0.0 or projection > 1.0:
            raise ValueError('CreateVacuousOpinion: Projection must be between 0 and 1. p=' + projection)
        return sbool(0.0, 0.0, 1.0, projection)	
    
    def getRelativeWeight(self, opinion: sbool = None) -> float:
        if opinion is None:
            return self._relative_weight if self.isDogmatic() else 0.0
        else:
            return self.adjust(self._relative_weight / opinion.relative_weight)

    '''  Auxiliary operationn '''
    def projection(self) -> float: # projected probability
        return self.adjust(self._b + self._a * self._u)
            
    def projectiveDistance(self, s: sbool) -> float: # projectiveDistance
        return self.adjust(abs(self.projection() - s.projection())) # /2

    def conjunctiveCertainty(self, s: sbool) -> float:
        return self.adjust((1.0 - self._u) * (1.0 - s._u))

    def degreeOfConflict(self, s: sbool) -> float:
        return self.adjust(self.projectiveDistance(s) * self.conjunctiveCertainty(s))
    
    def increasedUncertainty(self) -> sbool:
        if self.isVacuous():
            return self.copy()
        
        sqrt_u: float = math.sqrt(self._u)
        k: float = 1.0 - (sqrt_u - self._u) / (self._b + self._d)
        brBelief: float = self._b * k
        brUncertainty: float = sqrt_u
        brDisbelief: float = self._d * k
        return sbool(brBelief, brDisbelief, brUncertainty, self._a)

    def isAbsolute(self) -> bool:
        return (self._b == 1.0) or (self._d == 1.0)

    def isVacuous(self) -> bool:
        return self._u == 1.0

    def isCertain(self, threshold: float) -> bool:
        return not self.isUncertain(threshold)

    def isDogmatic(self) -> bool:
        return self._u == 0.0

    def isMaximizedUncertainty(self) -> bool:
        return (self._d == 0.0) or (self._b == 0.0)

    def isUncertain(self, threshold: float) -> bool:
        return 1.0 - self._u < threshold

    def uncertainOpinion(self) -> sbool:
        return self.uncertaintyMaximized()

    def certainty(self) -> float:
        if self._u == 0.0:
            return 0.0
        return 1.0 - self._u
    
    '''
	   Returns the subjective opinion that results from adjusting the base rate to be the one given in the
	   parameter. self operation is useful when we need to apply an opinion on a ubool value, whose
	   confidence will become the base rate of the resulting opinion. 
	   @param x ubool, whose confidence specifies the base_rate
	   @return A sbool value whose base rate is the one given in the parameter, the uncertainty is 
	   maintained, and the degree of belief is adjusted proportionally to the ratio (b/a) of the 
	   original sbool. If the base rate is the same, the sbool does not change. If the 
	   base_rate is 0 (False), the degree of belief of the sbool is 0 too, and the previous belief is 
	   transferred to the degree of disbelief.
    '''
    def applyOn(self, x: ubool) -> sbool:
        base_rate: float = x.c
        if base_rate < 0.0 or base_rate > 1.0:
            raise ValueError('applyOn(): base_rate must be between 0 and 1')
        
        if self._a == base_rate:
            return self.copy()
        
        uT: float = self._u
        if uT==1.0:
            return sbool(0.0, 0.0, 1.0, base_rate) # we only change the base rate...
        
        bT: float = 0.0
        if self._a == 0.0: #then base_rate != 0.0
            bT  = self._b + self._d * base_rate #OK
        else:  #self._a != 0.0
            bT  = min(base_rate * self._b / self._a, (1.0 - uT))
        
        return sbool(bT, 1.0 - bT - uT, uT, base_rate)
		
    '''Type Operations '''
    def NOT(self) -> sbool:
        return sbool(self._d, self._b, self._u, 1.0-self._a, self._relative_weight)
    
    def __invert__(self) -> sbool:
        return self.NOT()
    
    def __invert__(self) -> sbool:
        return self.NOT()
    
    def AND(self, s: sbool) -> sbool: # assumes independent variables
        if id(self) == id(s):
            return self.copy() # x and x = x

        if not isinstance(s, sbool):
            s = sbool(s)
        
        b: float = self._b * s._b + (0.0 if self._a * s._a == 1.0 else
            ((1.0 - self._a) * s._a * self._b * s._u + self._a * (1.0 - s._a) * self._u * s._b)
            / (1.0 - self._a * s._a))
        d: float = self._d + s._d - self._d * s._d
        return  sbool(b, 
                      d,
                      0 if abs(1 - d - b) < 0.0001 else 1 - d - b, 
                      self._a * s._a, 
                      self.getRelativeWeight() + s.getRelativeWeight()
        )

    def __and__(self, other) -> sbool:
        return self.AND(other)
    
    def __rand__(self, left) -> sbool:
        return sbool(left).AND(self)

    def OR(self, s: sbool) -> sbool:# assumes independent variables
        if id(self) == id(s):
            return self.copy() # x and x = x

        if not isinstance(s, sbool):
            s = sbool(s)
        
        b: float = self._b + s._b - self._b * s._b
        d: float = self._d * s._d + (0.0 if self._a + s._a == self._a*s._a else 
            (self._a*(1-s._a)*self._d*s._u+s._a*(1-self._a)*self._u*s._d)/(self._a + s._a - self._a*s._a))
        return sbool(
            b, 
            d, 
            0 if abs(1 - d - b) < 0.0001 else 1 - d - b, 
            self._a + s._a - self._a*s._a, 
            self.getRelativeWeight() + s.getRelativeWeight()
        )

    def __or__(self, other) -> sbool:
        if callable(other):
            return NotImplemented
        return self.OR(other)

    def __ror__(self, left) -> sbool:
        return sbool(left).OR(self)
	
    def IMPLIES(self, s: sbool) -> sbool:
        return self.NOT().OR(s) # self is to be consistent with ubool, because in Subjective Logic self is not the case...
	
    def __rshift__(self, other) -> ubool:
        return self.IMPLIES(other)

    def __rrshift__(self, left) -> ubool:
        return ubool(left).IMPLIES(self)
    
    def EQUIVALENT(self, s: sbool) -> sbool:
		# return self.IMPLIES(b).and(b.IMPLIES(self))
        return self.XOR(s).NOT() 	
	
    def XOR(self, s: sbool) -> sbool:
        if not isinstance(s, sbool):
            s = sbool(s)

        return sbool(
                abs(self._b - s._b), 
                1.0 - abs(self._b - s._b) - self._u*s._u,
                self._u*s._u,
                abs(self._a - s._a), 
                self.getRelativeWeight() + s.getRelativeWeight()
        )

    def __xor__(self, other) -> sbool:
        return self.XOR(other)
    
    def __rxor__(self, left) -> sbool:
        return sbool(left).XOR(self)
	
    def uncertaintyMaximized(self) -> sbool: # Returns the equivalent sbool with maximum uncertainty. 
            # The dual operation is toubool, which returns the equivalent sbool, with u==0
        #return self.increaseduncertainty
        # Replaced by another version
        
        p: float = self.projection()
        # Extreme cases
        if self._a == 1.0 and p == 1.0:
            return sbool(0.0,0.0,1.0,self._a,self.getRelativeWeight())
        if self._a == 1.0 and self._u == 1.0:
            return sbool(0.0,0.0,1.0,self._a,self.getRelativeWeight())
        if self._a == 0.0 and self._b==0.0:
            return sbool(0.0,0.0,1.0,self._a,self.getRelativeWeight())
        # Normal cases
        if p < self._a:
            return sbool(0.0, 1.0 - (p/self._a), p/self._a, self._a,self.getRelativeWeight())
        return sbool((p - self._a) / (1.0 - self._a), 0.0, (1.0 - p)/ (1.0 - self._a), self._a,self.getRelativeWeight())	
		
    def deduceY(self, yGivenX: sbool, yGivenNotX: sbool) -> sbool: # DEDUCTION: returns Y, acting 'self' as X
        y: sbool = sbool()
        px: float = self.projection()
        K: float = 0.0
        y._a: float = yGivenX._a if yGivenX._u+yGivenNotX._u >= 2.0 else (self._a*yGivenX._b+(1.0-self._a)*yGivenNotX._b)/(1.0-self._a*yGivenX._u-(1.0-self._a)*yGivenNotX._u)
        pyxhat: float = yGivenX._b*self._a + yGivenNotX._b*(1-self._a)+ y._a*(yGivenX._u*self._a+yGivenNotX._u*(1-self._a))
        bIy: float = self._b*yGivenX._b+self._d*yGivenNotX._b+self._u*(yGivenX._b*self._a+yGivenNotX._b*(1.0-self._a))
        dIy: float = self._b*yGivenX._d+self._d*yGivenNotX._d+self._u*(yGivenX._d*self._a+yGivenNotX._d*(1.0-self._a))
        uIy: float = self._b*yGivenX._u+self._d*yGivenNotX._u+self._u*(yGivenX._u*self._a+yGivenNotX._u*(1.0-self._a))
        # case I
        #if (((yGivenX._b>yGivenNotX._b)and(yGivenX._d>yGivenNotX._d))or((yGivenX._b<=yGivenNotX._b)and(yGivenX._d<=yGivenNotX._d))) 
        K = 0.0

        # case II.A.1
        if (yGivenX._b>yGivenNotX._b)and(yGivenX._d<=yGivenNotX._d) and \
                (pyxhat <= (yGivenNotX._b+y._a*(1.0-yGivenNotX._b-yGivenX._d))) and \
                (px<=self._a):
            K=(self._a*self._u*(bIy-yGivenNotX._b))/((self._b+self._a*self._u)*y._a)
        # case II.A.2
        if (yGivenX._b>yGivenNotX._b)and(yGivenX._d<=yGivenNotX._d) and \
                (pyxhat <= (yGivenNotX._b+y._a*(1.0-yGivenNotX._b-yGivenX._d))) and \
                (px>self._a):
            K=(self._a*self._u*(dIy-yGivenX._d)*(yGivenX._b-yGivenNotX._b))/((self._d+(1.0-self._a)*self._u)*y._a*(yGivenNotX._d-yGivenX._d))
        # case II.B.1
        if (yGivenX._b>yGivenNotX._b)and(yGivenX._d<=yGivenNotX._d) and \
                (pyxhat > (yGivenNotX._b+y._a*(1.0-yGivenNotX._b-yGivenX._d))) and \
                (px<=self._a):
            K=((1.0-self._a)*self._u*(bIy-yGivenNotX._b)*(yGivenNotX._d-yGivenX._d))/((self._b+self._a*self._u)*(1.0-y._a)*(yGivenX._b-yGivenNotX._b))
        # case II.B.2
        if (yGivenX._b>yGivenNotX._b)and(yGivenX._d<=yGivenNotX._d) and \
                (pyxhat > (yGivenNotX._b+y._a*(1.0-yGivenNotX._b-yGivenX._d))) and \
                (px>self._a):
            K=((1.0-self._a)*self._u*(dIy-yGivenX._d))/((self._d+(1.0-self._a)*self._u)*(1.0-y._a))

        # case III.A.1
        if (yGivenX._b<=yGivenNotX._b)and(yGivenX._d>yGivenNotX._d) and \
                (pyxhat <= (yGivenX._b+y._a*(1.0-yGivenNotX._b-yGivenX._d))) and \
                (px<=self._a):
            K=((1.0-self._a)*self._u*(dIy-yGivenNotX._d)*(yGivenNotX._b-yGivenX._b))/((self._b+self._a*self._u)*y._a*(yGivenX._d-yGivenNotX._d))
        
        # case III.A.2
        if (yGivenX._b<=yGivenNotX._b)and(yGivenX._d>yGivenNotX._d) and \
                (pyxhat <= (yGivenX._b+y._a*(1.0-yGivenX._b-yGivenNotX._d))) and \
                (px>self._a):
            K=((1.0-self._a)*self._u*(bIy-yGivenX._d))/((self._d+(1.0-self._a)*self._u)*y._a)

        # case III.B.1
        if (yGivenX._b<=yGivenNotX._b)and(yGivenX._d>yGivenNotX._d) and \
                (pyxhat > (yGivenX._b+y._a*(1.0-yGivenX._b-yGivenNotX._d))) and \
                (px<=self._a):
            K=(self._a*self._u*(dIy-yGivenNotX._b))/((self._b+self._a*self._u)*(1.0-y._a))

        # case III.B.2
        if (yGivenX._b<=yGivenNotX._b)and(yGivenX._d>yGivenNotX._d) and \
                (pyxhat > (yGivenX._b+y._a*(1.0-yGivenX._b-yGivenNotX._d))) and \
                (px>self._a):
            K=(self._a*self._u*(bIy-yGivenX._b)*(yGivenX._d-yGivenNotX._d))/((self._d+(1.0-self._a)*self._u)*(1.0-y._a)*(yGivenNotX._b-yGivenX._b))
        
        y._b = self.adjust(bIy - y._a*K)
        y._d = self.adjust(dIy - (1.0-y._a)*K)
        y._u = self.adjust(uIy + K)
        y.relative_weight = yGivenX.getRelativeWeight() + yGivenNotX.getRelativeWeight()

        return y
	

    ''' UNION AND WEIGHTED UNION OPERATIONS '''
    '''
        This method implements Union of two opinions, according to Josang's book (Section 6.1)
        return a sbool that represents the union of the two opinions (self + s).
    '''
    def union(self, s: sbool) -> sbool:
        if s is None or self._a + s._a >1.0 or self._b+s._b > 1.0:
            raise ValueError('union: invalid argument')

        if not isinstance(s, sbool):
            s = sbool(s)

        return sbool(
            self._b + s._b, 
            (self._a * (self._d - s._b) + s._a * (s._d - self._b)) / (self._a + s._a),
            self._a * self._u + s._a * s._u,
            self._a + s._a, 
            self.getRelativeWeight() + s.getRelativeWeight()
		)
	
    '''
        This method implements the Weighted Union of a collection of opinions. 
        Note that the weighted union of two operations is different from their union. 
        return a sbool that represents the weigthed union, assuming the same weight for all opinions.
    '''    
    def weightedUnion(opinions: Iterable[sbool]) -> sbool:
        if None in opinions or len(opinions) < 2:
            raise ValueError('weightedUnion: Cannot make the union of None opinions, or only one opinion was passed')
        b: float = 0.0
        a: float = 0.0
        u: float = 0.0
        n: int = len(opinions)
        for so in opinions:
            b+=so._b
            a+=so._a
            u+=so._a*so._u
        
        return sbool(b/n,1-b/n-u/a,u/a,a/n)
    
 
    ''' Binary ver ''' 
    def weightedUnion2(self, opinion: sbool) -> sbool: #consensus and compromise fusion
       return sbool.ccOpinionsFusion([self, opinion])

	
    '''
	    FUSION OPERATIONS 
	        These implementations are based in those given in https:#github.com/vs-uulm/subjective-logic-java
    '''
    '''
	    This method implements constraint belief fusion (CBF). It uses the binary operation and iterates 
	    over the collection of opinions. self operation is associative if the base rate is the same for all 
        opinions, otherwise the fused base rate distribution could be the confidence-weighted
	    average base rate (see Josang's book). The neutral element is the vacuous opinion.
        return a sbool that represents the fused evidence.
    '''
    def cbOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        if None in opinions or len(opinions) < 2:
            raise ValueError('BCF: Cannot fuse None opinions, or only one opinion was passed')
        bcf: sbool = None
        
        for so in opinions:
            if bcf is None:
                bcf = so # first time
            else:
                bcf = bcf.cbFusion(so)
        
        return bcf
    
    '''
        This method implements MIN fusion. self takes the minimum, i.e., returns the opinion with 
        the lowest probability of being True, meaning the lowest projected probability P(X=x).
        return a sbool that represents the fused evidence.
    '''
    def minimumOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        if None in opinions or len(opinions) < 2:
            raise ValueError('MBF: Cannot fuse None opinions, or only one opinion was passed')

        min: sbool = None
        for so in opinions:
            if min is None:
                min = so
            min = min.min(so)
        
        return min.copy()

    '''
        This method implements MAJORITY fusion. self returns a dogmatic opinion that specifies the 
        decision of the majority.
        If the majority is tied, a vacuous opinion is returned.
        It is assumed that the base rates of all opinions are equal.
        For self operation, opinions that are undecided (projections equals base rate) are ignored.
        return a sbool that represents the fused evidence.
    '''

    def majorityOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        if None in opinions or len(opinions) < 2:
            raise ValueError('MajBF: Cannot fuse None opinions, or only one opinion was passed')
        pos: int = 0
        neg: int = 0

        for so in opinions:
            if so.projection() < so._a:
                neg+= 1
            elif so.projection() > so._a:
                pos+= 1
        
        if pos > neg: return sbool(1.0, 0, 0, 0.5) 		# True
        elif pos < neg: return sbool(0, 1.0, 0, 0.5) 	# False
        else: return sbool(0, 0, 1.0, 0.5) 				# uncertain
    
    
    ''' This method implements AVERAGE fusion.
        return a sbool that represents the fused evidence.
    '''
    def averagingOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
	   
        #implemented using equation (32) of https:#folk.uio.no/josang/papers/JWZ2017-FUSION.pdf 
        # because the Josang's book has a problem.

        if opinions is None or None in opinions or not opinions:
            raise ValueError('AVF: Cannot average None opinions')

        b: float = 0.0; u: float=0.0; a: float = 0.0
        PU: float = 1.0 #product of all uncertainties
        count: int = 0

        oBelief: float; oAtomicity: float; oUncertainty: float; oDisbelief: float

        for o in opinions:
            PU *= o.uncertainty # product of all uncertainties

        # case I: all opinions with uncertainty > 0:
        if PU != 0.0:
            for o in opinions:
                u += PU/o.uncertainty
                b += o.belief * PU/o.uncertainty
                a += o.base_rate
            oBelief = b / u
            oAtomicity = a / len(opinions)
            oUncertainty = len(opinions) * PU / u
            oDisbelief = 1.0 - oBelief - oUncertainty
            return sbool(oBelief, oDisbelief, oUncertainty, oAtomicity)

        else: # there is at least one opinion with uncertainty = 0. Then we only consider these opinions
            for o in opinions:
                if o.uncertainty == 0.0:
                    b += o.belief
                    a += o.base_rate
                    count+= 1  
            oBelief = b / count
            oAtomicity = a / count
            oUncertainty = 0.0
            oDisbelief = 1.0 - oBelief - oUncertainty
            return sbool(oBelief, oDisbelief, oUncertainty, oAtomicity)

    def productOfUncertainties(opinions: Iterable[sbool]) -> float:
        return reduce(lambda acc, u : acc * u, map(lambda x : x.uncertainty, opinions), 1.0)

    '''
     This method implements cumulative belief fusion (CBF) for multiple sources, as discussed in the corrected
     version of <a href='https:#folk.uio.no/josang/papers/JWZ2017-FUSION.pdf'>a FUSION 2017 paper by Josang et al.</a>
    
     As discussed in the book, cumulative fusion is useful in scenarios where opinions from multiple sources 
     are combined, where each source is relying on independent (in the statistical sense) evidence.
     
     
       return a sbool that represents the fused evidence based on evidence accumulation.
    '''
    def aleatoryCumulativeOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        #handle edge cases
        if opinions is None or None in opinions or not opinions:
            raise ValueError('aCBF: Cannot average None opinions')

        if len(opinions) == 1:
            return opinions.iterator().next().copy()
        
        #fusion as defined by Josang
        resultBelief: float; resultDisbelief: float; resultUncertainty: float; resultRelativeWeight: float = 0.0; resultAtomicity: float = -1.0

        dogmatic: list[sbool] = []
        first: bool = True

        for o in opinions:
            if first:
                resultAtomicity = o.base_rate
                first = False
            #dogmatic iff uncertainty is zero.
            if o.uncertainty == 0.0:
                dogmatic.append(o)

        if not dogmatic:
            #there are no dogmatic opinions -- case I/Eq16 of 10.23919/ICIF.2017.8009820
            productOfUncertainties: float = sbool.productOfUncertainties(opinions)
            numerator: float = 0.0
            beliefAccumulator: float = 0.0
            disbeliefAccumulator: float = 0.0

            #self computes the top and bottom sums in Eq16, but ignores the - (N-1) * productOfUncertainties in the numerator (see below)
            for o in opinions:
                #productWithoutO = product of uncertainties without o's uncertainty
                #self can be rewritten:
                #prod {C_j != C  u^{C_j = (u^C)^-1 * prod{C_j u^{C_j = 1/(u^C) * prod{C_j u^{C_j
                #so instead of n-1 multiplications, we only need a division
                productWithoutO: float = productOfUncertainties / o.uncertainty
                beliefAccumulator = beliefAccumulator + productWithoutO * o.belief
                disbeliefAccumulator = disbeliefAccumulator + productWithoutO * o.disbelief
                numerator = numerator + productWithoutO

            #self completes the numerator:
            numerator = numerator - (len(opinions) - 1) * productOfUncertainties
            resultBelief = beliefAccumulator / numerator
            resultDisbelief = disbeliefAccumulator / numerator
            resultUncertainty = productOfUncertainties / numerator
            resultRelativeWeight = 0.0
        else:
            #at least 1 dogmatic opinion
            #note: self computation assumes that the relative weight represents how many opinions have been fused into that opinion.
            #for a normal multi-source fusion operation, self should be 1, in which case the gamma's in Eq17 are 1/N as noted in the text (i.e., all opinions count equally)
            #however, self formulation also allows partial fusion beforehand, by 'remembering' the amount of dogmatic (!) opinions in o.relative_weight.
            totalWeight: float = math.fsum(map(lambda o : o.getRelativeWeight(), dogmatic))
            resultBelief: float =  math.fsum(map(lambda o : o.getRelativeWeight()/totalWeight * (o).belief, dogmatic))
            resultDisbelief: float = math.fsum(map(lambda o : o.getRelativeWeight()/totalWeight * (o).disbelief, dogmatic))
            resultUncertainty: float = 0.0
            resultRelativeWeight: float = totalWeight

        return sbool(resultBelief, resultDisbelief, resultUncertainty, resultAtomicity,resultRelativeWeight)

    '''
        This method implements epistemic cumulative belief fusion (eCBF) for multiple sources, 
        as discussed in the corrected
        version of <a href='https:#folk.uio.no/josang/papers/JWZ2017-FUSION.pdf'>a FUSION 2017 paper by Josang et al.</a>

        eCBF is useful when the opinions represent knowledge, and not observations, and therefore they are
        uncertainty maximized. As in the CBF, each source is supposed to be relying on independent 
        (in the statistical sense) evidence (in self case, knowledge).
        return a sbool that represents the fused evidence based on evidence accumulation.
    '''
    def epistemicCumulativeOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        #handle edge cases
        if opinions is None or None in opinions or not opinions:
            raise ValueError('eCBF: Cannot average None opinions')

        if len(opinions) == 1:
            return opinions.iterator().next().copy()

        #fusion as defined by Josang
        resultBelief: float; resultDisbelief: float; resultUncertainty: float; resultRelativeWeight: float = 0.0; resultAtomicity: float = -1.0

        dogmatic: list[sbool] = []
        first: bool = True
        for o in opinions:
            if first:
                resultAtomicity = o.base_rate
                first = False
            
            #dogmatic iff uncertainty is zero.
            if o.uncertainty == 0.0:
                dogmatic.append(o)
        
        if not dogmatic:
            #there are no dogmatic opinions -- case I/Eq16 of 10.23919/ICIF.2017.8009820
            uncertainties: float = map(lambda o : o.uncertainty, opinions)
            productOfUncertainties: float = sbool.productOfUncertainties(opinions)
            numerator: float = 0.0
            beliefAccumulator: float = 0.0
            disbeliefAccumulator: float = 0.0

            #self computes the top and bottom sums in Eq16, but ignores the - (N-1) * productOfUncertainties in the numerator (see below)
            for o in opinions:
                #productWithoutO = product of uncertainties without o's uncertainty
                #self can be rewritten:
                #prod {C_j != C  u^{C_j = (u^C)^-1 * prod{C_j u^{C_j = 1/(u^C) * prod{C_j u^{C_j
                #so instead of n-1 multiplications, we only need a division
                productWithoutO: float = productOfUncertainties / o.uncertainty
                beliefAccumulator = beliefAccumulator + productWithoutO * o.belief
                disbeliefAccumulator = disbeliefAccumulator + productWithoutO * o.disbelief
                numerator = numerator + productWithoutO
            
            #self completes the numerator:
            numerator = numerator - (len(opinions) - 1) * productOfUncertainties
            resultBelief = beliefAccumulator / numerator
            resultDisbelief = disbeliefAccumulator / numerator
            resultUncertainty = productOfUncertainties / numerator
            resultRelativeWeight = 0.0
        else:
            #at least 1 dogmatic opinion
            #note: self computation assumes that the relative weight represents how many opinions have been fused into that opinion.
            #for a normal multi-source fusion operation, self should be 1, in which case the gamma's in Eq17 are 1/N as noted in the text (i.e., all opinions count equally)
            #however, self formulation also allows partial fusion beforehand, by 'remembering' the amount of dogmatic (!) opinions in o.relative_weight.
            totalWeight: float = math.fsum(map(lambda o : o.getRelativeWeight(), dogmatic))
            resultBelief: float =  math.fsum(map(lambda o : o.getRelativeWeight()/totalWeight * (o).belief, dogmatic))
            resultDisbelief: float = math.fsum(map(lambda o : o.getRelativeWeight()/totalWeight * (o).disbelief, dogmatic))
            resultUncertainty = 0.0
            resultRelativeWeight = totalWeight

        result: sbool = sbool(resultBelief, resultDisbelief, resultUncertainty, resultAtomicity,resultRelativeWeight)
        return result.uncertaintyMaximized()


    '''
        This method implements weighted belief fusion (WBF) for multiple sources, as discussed in a FUSION 2018 paper by van der Heijden et al.
        
        As discussed in the book, WBF is intended to represent the confidence-weighted averaging of evidence.
        Similar to AverageBF, it is useful when dependence between sources is assumed. However, WBF introduces 
        additional weights to increase the significance of sources that possess high certainty. 
        
        return a SubjectiveOpinion that represents the fused evidence based on confidence-weighted averaging of evidence.
    '''
    def weightedOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        if opinions is None or None in opinions or not opinions:
            raise ValueError('WBF: Cannot average None opinions')

        if len(opinions) == 1:
            return opinions[0].copy()

        resultBelief: float = 0.0
        resultDisbelief: float = 0.0
        resultUncertainty: float = 0.0
        resultRelativeWeight: float = 0.0
        resultAtomicity: float = 0.0

        dogmatic: list[sbool] = []
        for o in opinions:
            #dogmatic iff uncertainty is zero.
            if o.uncertainty == 0:
                dogmatic.append(o)

        if not dogmatic and any([o.certainty() > 0 for o in opinions]):
            #Case 1: no dogmatic opinions, at least one non-vacuous opinion
            productOfUncertainties: float = sbool.productOfUncertainties(opinions)
            sumOfUncertainties: float = math.fsum(map(lambda o : o.uncertainty, opinions))

            numerator: float = 0.0
            beliefAccumulator: float = 0.0
            disbeliefAccumulator: float = 0.0
            atomicityAccumulator: float = 0.0

            for o in opinions:
                #prod = product of uncertainties without o's uncertainty
                prod: float = productOfUncertainties / o.uncertainty

                #recall certainty = 1 - uncertainty
                beliefAccumulator = beliefAccumulator + prod * o.belief * o.certainty()
                disbeliefAccumulator = disbeliefAccumulator + prod * o.disbelief * o.certainty()
                atomicityAccumulator = atomicityAccumulator + o.base_rate * o.certainty()
                numerator = numerator + prod
            

            numerator = numerator - len(opinions) * productOfUncertainties

            resultBelief = beliefAccumulator / numerator
            resultDisbelief = disbeliefAccumulator / numerator
            resultUncertainty = (len(opinions) - sumOfUncertainties) * productOfUncertainties / numerator
            resultAtomicity = atomicityAccumulator / (len(opinions) - sumOfUncertainties)
        elif all([o.uncertainty == 1 for o in opinions]):
            #Case 3 -- everything is vacuous
            resultBelief = 0.0
            resultDisbelief = 0.0
            resultUncertainty = 1.0

            #all confidences are zero, so the weight for each opinion is the same -> use a plain average for the resultAtomicity
            resultAtomicity: float = 0.0
            first: bool = True
            for o in opinions:
                if first:
                    resultAtomicity = resultAtomicity + o.base_rate
                    first = False
                
            resultAtomicity = resultAtomicity / float(len(opinions))

        else:
            #Case 2 -- dogmatic opinions are involved
            totalWeight: float = math.fsum(map(lambda o : o.getRelativeWeight(), dogmatic))
            resultBelief: float =  math.fsum(map(lambda o : o.getRelativeWeight()/totalWeight * (o).belief, dogmatic))
            resultDisbelief: float = math.fsum(map(lambda o : o.getRelativeWeight()/totalWeight * (o).disbelief, dogmatic))
            resultUncertainty = 0.0
            resultRelativeWeight = totalWeight

            #note: the for loop below will always set resultAtomicity correctly.
            resultAtomicity = -1
            first: bool = True
            for o in opinions:
                if first:
                    resultAtomicity = o.base_rate
                    first = False

        return sbool(resultBelief, resultDisbelief, resultUncertainty, resultAtomicity,resultRelativeWeight)
   
    '''
        This method implements consensus & compromise fusion (CCF) for multiple sources, as discussed in a FUSION 2018 paper by van der Heijden et al.
        For more details, refer to Chapter 12 of the Subjective Logic book by Josang, specifically Section 12.6, which defines CC fusion for the case of two sources.
    
        return a sbool that represents the fused evidence.
    '''
    def ccOpinionsFusion(opinions: Iterable[sbool]) -> sbool:
        if opinions is None or None in opinions or len(opinions) < 2:
            raise ValueError('CCF: Cannot fuse None opinions, or only one opinion was passed')

        base_rate: float = -1
        first: bool = True
        for so in opinions:
            if first:
                base_rate = so.base_rate
                first = False
            elif base_rate != so.base_rate:
                raise ValueError('CCF: Base rates for CC Fusion must be the same')
    
        #Step 1: consensus phase
        consensusBelief: float = float(min(map(lambda o : o.belief, opinions)))
        consensusDisbelief: float = float(min(map(lambda o : o.disbelief, opinions)))
        consensusMass: float = consensusBelief + consensusDisbelief

        residueBeliefs: list[float] = []
        residueDisbeliefs: list[float] = []
        uncertainties: list[float] = []
        for so in opinions:
            #note: self max should not be necessary..
            residueBeliefs.append(max(so.belief - consensusBelief, 0))
            residueDisbeliefs.append(max(so.disbelief - consensusDisbelief, 0))
            uncertainties.append(so.uncertainty)

        #Step 2: Compromise phase
        productOfUncertainties: float = sbool.productOfUncertainties(opinions)

        compromiseBeliefAccumulator: float = 0
        compromiseDisbeliefAccumulator: float = 0
        compromiseXAccumulator: float = 0 #self is what will later become uncertainty

        #self computation consists of 4 sub-sums that will be added independently.
        for i in range(len(opinions)):
            bResI: float = residueBeliefs[i]
            dResI: float = residueDisbeliefs[i]
            uI: float = uncertainties[i]
            # uWithoutI: float = productOfUncertainties / uI
            uWithoutI: float = productOfUncertainties / uI if uI != 0.0 else 0.0 

            #sub-sum 1:
            compromiseBeliefAccumulator = compromiseBeliefAccumulator + bResI * uWithoutI
            compromiseDisbeliefAccumulator = compromiseDisbeliefAccumulator + dResI * uWithoutI
            #note: compromiseXAccumulator is unchanged, since b^{ResI_X() of the entire domain is 0

        #sub-sums 2,3,4 are all related to different permutations of possible values
        domains = sbool.tabulateOptions(len(opinions))
        for permutation in domains:
            intersection: Domain = reduce(lambda acc, p : acc.intersect(p), permutation, Domain.DOMAIN)
            union: Domain = reduce(lambda acc, p : acc.union(p), permutation, Domain.NIL)

            #sub-sum 2: intersection of elements in permutation is x
            if intersection is Domain.TRUE:
                # --> add to belief
                prod: float = 1
                if Domain.DOMAIN in permutation:
                    prod = 0.0
                else:
                    for j in range(len(permutation)):
                        match permutation[j]:
                            case Domain.DOMAIN:
                                prod = 0.0 # multiplication by 0
                            case Domain.TRUE:
                                prod = prod * residueBeliefs[j]
                compromiseBeliefAccumulator += prod
            elif intersection is Domain.FALSE:
                # --> add to disbelief
                prod: float = 1.0
                if Domain.DOMAIN in permutation:
                    prod = 0.0
                else:
                    for j in range(len(permutation)):
                        match permutation[j]:
                            case Domain.DOMAIN:
                                prod = 0.0 # multiplication by 0
                            case Domain.FALSE:
                                prod *= residueDisbeliefs[j]
                        
                compromiseDisbeliefAccumulator += prod
            

            match union:
                case Domain.DOMAIN:
                    if intersection is not Domain.NIL:
                        pass
                        #sub-sum 3: union of elements in permutation is x, and intersection of elements in permutation is not NIL

                        #Note: self is always zero for binary domains, as explained by the following:
                        #prod: float = 1
                        #for (j: int=0 j<len(permutation) j++) {
                        #    switch (permutation[j]) {
                        #        case Domain.NIL:
                        #        case Domain.DOMAIN:
                        #            prod = 0 #because residue belief over NIL/DOMAIN is zero here
                        #        case Domain.TRUE:
                        #        case Domain.FALSE:
                        #            prod = 0 #because 1-a(y|x) is zero here, since a(y|x)=1 when x=y, and self must occur, since a(x|!x) occurring implies the intersection is NIL
                        #    
                        #            
                    else:
                        #sub-sum 4: union of elements in permutation is x, and intersection of elements in permutation is NIL
                        prod: float = 1.0
                        for j in range(len(permutation)):
                            match permutation[j]:
                                case Domain.NIL:
                                    prod = 0.0
                                case Domain.DOMAIN:
                                    prod = 0.0 #because residue belief over NIL/DOMAIN is zero here
                                case Domain.TRUE:
                                    prod *= residueBeliefs[j]
                                case Domain.FALSE:
                                    prod *= residueDisbeliefs[j]                          
                        compromiseXAccumulator += prod
                case Domain.NIL:
                    #union of NIL means we have nothing to add
                    #sub-sum 3: union of elements in permutation is x, and intersection of elements in permutation is not NIL
                    #sub-sum 4: union of elements in permutation is x, and intersection of elements in permutation is NIL
                    pass
                case Domain.TRUE:
                    #sub-sum 3: self is always zero for True and False, since 1-a(y_i|y_j)=0 in binary domains, where the relative base rate is either 1 if the union is x

                    #sub-sum 4: union of elements in permutation is x, and intersection of elements in permutation is NIL
                    if intersection is Domain.NIL:
                        #union is True, intersection is nil --> compute the product
                        prod: float = 1.0
                        for j in range(len(permutation)):
                            match permutation[j]: #other cases will not occur
                                case Domain.TRUE:
                                    prod *= residueBeliefs[j]
                                case Domain.FALSE:
                                    prod *= residueDisbeliefs[j]
                                case Domain.NIL:
                                    prod = 0.0
                                case _:
                                    raise RuntimeError()
                        compromiseBeliefAccumulator += prod
                case Domain.FALSE:
                    #sub-sum 3: self is always zero for True and False, since 1-a(y_i|y_j)=0 in binary domains, where the relative base rate is either 1 if the union is x
                    #sub-sum 4: union of elements in permutation is x, and intersection of elements in permutation is NIL
                    if intersection is Domain.NIL:
                        #union is True, intersection is nil --> compute the product
                        prod: float = 1.0
                        for j in range(len(permutation)):
                            match permutation[j]: #other cases will not occur
                                case Domain.TRUE:
                                    prod *= residueBeliefs[j]
                                case Domain.FALSE:
                                    prod *= residueDisbeliefs[j]
                                case Domain.NIL:
                                    prod = 0.0
                                case _:
                                    raise RuntimeError()
                        compromiseDisbeliefAccumulator += prod

        compromiseBelief: float = compromiseBeliefAccumulator
        compromiseDisbelief: float = compromiseDisbeliefAccumulator
        compromiseUncertainty: float = compromiseXAccumulator
        preliminaryUncertainty: float = productOfUncertainties
        compromiseMass: float = compromiseBelief + compromiseDisbelief + compromiseUncertainty

        #Step 3: Normalization phase
        normalizationFactor: float = (1 - consensusMass - preliminaryUncertainty) / (compromiseMass) if compromiseMass != 0.0 else 1.0
        fusedBelief: float = consensusBelief + normalizationFactor * compromiseBelief
        fusedDisbelief: float = consensusDisbelief + normalizationFactor * compromiseDisbelief
        fusedUncertainty: float = 1.0 - fusedBelief - fusedDisbelief

        return sbool(fusedBelief, fusedDisbelief, fusedUncertainty, base_rate)

    def tabulateOptions(size: int) -> set[Domain]:
        result = []

        if size == 1:
            for d in Domain:
                result.append([d])
        else:
            for size_less_one_list in sbool.tabulateOptions(size - 1):
                for d in Domain:
                    new_list = size_less_one_list.copy()
                    new_list.append(d)
                    result.append(new_list)

        return result
   
    ''' BINARY VERSIONS OF FUSING OPERATIONS '''

    def cbFusion(self, opinion: sbool) -> sbool: #belief constraint fusion
        #implemented using equation 12.2 of Josang's book
        harmony: float = self._b * opinion.uncertainty + self._u * opinion.belief + self._b *opinion.belief
        conflict: float = self._b * opinion.disbelief + self._d * opinion.belief
        if conflict == 1.0:
            raise ValueError('BCF: Cannot fuse totally conflicting opinions')
        
        b: float = harmony/(1.0-conflict)
        u: float = (self._u * opinion.uncertainty) / (1.0-conflict) 
        a: float = (self._a + opinion.base_rate) / 2.0 if (self._u + opinion.uncertainty == 2.0) \
                    else (self._a * (1.0 - self._u) + opinion.base_rate * (1.0-opinion.uncertainty)) \
                        / (2-self._u-opinion.uncertainty)
        return sbool(b, 1.0 - b - u, u, a)
        
    def ccFusion(self, opinion: sbool) -> sbool: #consensus and compromise fusion
        return sbool.ccOpinionsFusion([self, opinion])

    def aleatoryCumulativeFusion(self, opinion: sbool) -> sbool:
        return sbool.aleatoryCumulativeOpinionsFusion([self, opinion])

    def epistemicCumulativeFusion(self, opinion: sbool) -> sbool:
        return sbool.epistemicCumulativeOpinionsFusion([self, opinion])

    def weightedFusion(self, opinion: sbool) -> sbool:
        return sbool.weightedOpinionsFusion([self, opinion])

    def minimumFusion(self, opinion: sbool) -> sbool:
        return sbool.minimumOpinionsFusion([self, opinion])

    def majorityFusion(self, opinion: sbool) -> sbool:
        return sbool.majorityOpinionsFusion([self, opinion])

    def averagingFusion(self, opinion: sbool) -> sbool:
        return sbool.averagingOpinionsFusion([self, opinion])
   
   
    ''' DISCOUNTING OPERATIONS '''
   
    def discount(self, x):
        if isinstance(x, sbool):
            return self.discount_sbool(x)
        elif isinstance(x, list):
            return self.discount_list(x)

    ''' Binary versions '''
    '''
        This method implements the 'probability-sensitive trust discounting operator', 
        which causes the uncertainty in A's derived opinion about X to increase as a 
        function of the projected distrust in the source/advisor B. 
    
        For more details, refer to Chapter 14 of the Subjective Logic book by Josang, 
        specifically Section 14.3.2 that defines Trust Discounting with Two-Edge Paths.
    
        we assume that 'self' represents the opinion (functional trust) of an agent B 
        on statement X, i.e., [B:X]
        
        return a sbool that represents the opinion of A about X, [A:X]=[AB]x[B:X]
    '''
    def discount_sbool(self, atrustOnB: sbool) -> sbool:
        if atrustOnB is None:
            raise ValueError('Discountion operator parameter cannot be None')

        # self IS THE DISCOUNT OPERATOR DEFINED IN THE JOSANG 2016 BOOK 
        p: float = atrustOnB.projection()
        b: float = p * self._b
        d: float = p * self._d
        u: float = 1 - p * (self._d + self._b)
        a: float = self._a
        return sbool(b,d,u,a)


    '''
        This method implements the discounting operator from the Trustyfeer 2018 
        paper bu Kurdi et al., which uses the belief of the trust of A on B, instead of 
        the projection() of the trust of A on B, that was originally used by Josang. 
     
        Heba Kurdi, Bushra Alshayban, Lina Altoaimy, and Shada Alsalamah
        'TrustyFeer: A Subjective Logic Trust Model for Smart City Peer-to-Peer Federated Clouds'
        Wireless Communications and Mobile Computing, Volume 2018, Article ID 1073216, 13 pages
        https:#doi.org/10.1155/2018/1073216
     
        We assume that 'self' represents the opinion (functional trust) of an agent B 
        on statement X, i.e., [B:X]
    
        return a sbool that represents the opinion of A about X, [A:X]=[AB]x[B:X]
    '''
    def discountB(self, atrustOnB: sbool) -> sbool:
        if atrustOnB is None:
            raise ValueError('Discountion operator parameter cannot be None')

        p: float = atrustOnB.belief # instead of atrustOnB.projection()
        b: float = p * self._b
        d: float = p * self._d
        u: float = 1 - b - d # = atrustOnB.disbelief + atrustOnB.uncertainty + atrustOnB.belief*self._u
        a: float = self._a

        return sbool(b,d,u,a)


    ''' Multi-edge path versions '''
    '''
        This method implements the discounting operator on multi-edge paths, 
        using the 'probability-sensitive trust discounting operator'
        which causes the uncertainty in A�s derived opinion about X to increase as a 
        function of the projected distrust in the source/advisor B. 
     
        For more details, refer to Chapter 14 of the Subjective Logic book by Josang, 
        specifically Section 14.3.4 that defines Trust Discounting with Multi-Edge Paths.
     
        we assume that 'self' represents the opinion (functional trust) of an agent An 
        on statement X, i.e., [An:X]
    
        @param agentsTrusts A collection of trust referrals that Agent (Ai) has on (Ai+1). [AiAi+1]
        return a sbool that represents the resulting opinion of A1 on X. 
        [A1:X]=[A1A2...An]x[An:X]
    '''
    
    def discount_list(self, agentsTrusts: Iterable[sbool]) -> sbool:
        if agentsTrusts is None:
            raise ValueError('Discountion operator parameter cannot be None')

        # self IS THE DISCOUNT OPERATOR DEFINED IN THE JOSANG 2016 BOOK 
        p: float = reduce(lambda acc, value : acc * value, map(lambda o : o.projection(), agentsTrusts), 1.0)
        b: float = p * self._b
        d: float = p * self._d
        u: float = 1 - p * (self._d + self._b)
        a: float = self._a

        return sbool(b,d,u,a)

    '''
        This method implements the discounting operator on multi-edge paths, 
        using the 'discounting operator' discountB() defined by Kurdi et al in 
        their 2018 paper 
         
        Heba Kurdi, Bushra Alshayban, Lina Altoaimy, and Shada Alsalamah
        'TrustyFeer: A Subjective Logic Trust Model for Smart City Peer-to-Peer Federated Clouds'
        Wireless Communications and Mobile Computing, Volume 2018, Article ID 1073216, 13 pages
        https:#doi.org/10.1155/2018/1073216
         
        we assume that 'self' represents the opinion (functional trust) of an agent An 
        on statement X, i.e., [An:X]
        
        return a sbool that represents the resulting opinion of A1 on X. 
        [A1:X]=[A1A2...An]x[An:X]
    '''
    def discountB(self, agentsTrusts: Iterable[sbool]) -> sbool:
        if agentsTrusts is None:
            raise ValueError('Discountion operator parameter cannot be None')
        
        # self IS THE DISCOUNT OPERATOR DEFINED IN THE JOSANG 2016 BOOK 
        p: float = reduce(lambda acc,value : acc * value, map(lambda o : o.belief, agentsTrusts), 1.0)
        b: float = p * self._b
        d: float = p * self._d
        u: float = 1 - p * (self._d + self._b)
        a: float = self._a

        return sbool(b,d,u,a)
    
    ''' comparison operations '''
    def EQUALS(self, o: sbool) -> bool:
        if id(self) == id(o):
            return True
        if o is None or self.__class__ != o.__class__:
            return False

        return 	abs(self.belief - o.belief) < 0.001 and \
                abs(self.disbelief - o.disbelief) < 0.001 and \
                abs(self.uncertainty - o.uncertainty) < 0.001 and \
                abs(self.base_rate - o.base_rate) < 0.001

    def equals(self, o: sbool) -> bool:
        return self.EQUALS(o)

    def __eq__(self, other) -> ubool:
        return self.EQUALS(other)

    def DISTINCT(self, b: sbool) -> bool:
        return not self.EQUALS(b)

    def distinct(self, b: sbool) -> bool:
        return not self.DISTINCT(b)
    
    def __ne__(self, other) -> ubool:
        return self.DISTINCT(other)

    def min(self, opinion: sbool) -> sbool: # minimum based on projections
        return self if self.projection() <= opinion.projection() else opinion

    def max(self, opinion: sbool) -> sbool: # maximum based on projections
        return self if self.projection() >= opinion.projection() else opinion

    def __hash__(self) -> int:
        return round(float(self._b*100)) \
                + 10 * round(float(self._d * 100)) \
                + 100 * round(float(self._u*100)) \
                + 1000 * round(float(self._a*100))

    '''Conversions'''
    def __str__(self) -> str:
        return 'sbool({:5.3f}, {:5.3f}, {:5.3f}, {:5.3f})'.format(self._b, self._d, self._u, self._a)
        
    def __repr__(self) -> str:
        return self.__str__()

    def toubool(self) -> ubool: # returns the projected probability
        return ubool(self.projection()) 

    def tobool(self) -> bool:
        return ubool(self.projection()).tobool()

    def __bool__(self) -> bool:
        return self.tobool()

    ''' Other Methods '''
    def compareTo(self, other: sbool) -> int:
        x: float = abs(self._b - other.belief) \
                    + abs(self._d - other.disbelief) \
                    + abs(self._u - other.uncertainty) \
                    + abs(self._a - other.base_rate)
        if x < 0.001:
            return 0
        elif self.projection()-other.projection() < 0:
            return -1
        return 1

    def copy(self) -> sbool:
        return sbool(self._b,self._d,self._u,self._a,self._relative_weight)