from __future__ import annotations

import math

from uncertainty.utypes import ubool
from uncertainty.utypes import Result

import math

class uint:
	
    # Instance attributes:
    # x: int 
    # u: float 

	def __init__(self, x: int|str|tuple = 0, u: int|float|str = 0.0) -> uint:
		if isinstance(x, tuple) and len(x) == 2:
			x, u = x
		elif isinstance(x, (uint, ufloat)):
			u = x.u
			x = x.x

		if not isinstance(x, (int, str)):
			raise ValueError("Invalid parameter: x is not int or int as string")
		if not isinstance(u, (int, float, str)):
			raise ValueError("Invalid parameter: u is not int, float or float/int as string")
		
		self.x = int(x)
		self.u = abs(float(u))

	@property
	def u(self):
		return self._u

	@u.setter
	def u(self, u: float|str):
		if not isinstance(u, (float, str)):
			raise ValueError("Invalid parameter: u not float or float as string")
		
		self._u = abs(float(u))
		
	''' Type Operations '''

	def add(self, r: int|uint|float|ufloat, covariance: float = 0.0) -> uint:
		if isinstance(r, float):
			return self.toufloat() + ufloat(r)
		elif isinstance(r, ufloat):
			return self.toufloat() + r
		elif isinstance(r, int):
			r = uint(r)
			
		return uint(self.x + r.x, math.sqrt((self.u * self.u) + (r.u**2) + 2 * covariance))
	
	def __add__(self, r: int|uint) -> uint:
		return self.add(r)
	
	def __radd__(self, left) -> uint:
		if isinstance(left, int):
			left = uint(left)
		elif isinstance(left, float):
			left = ufloat(left)

		return left + self
	
	def sub(self, r: int|uint, covariance: float = 0.0) -> uint|ufloat:
		if isinstance(r, float):
			return self.toufloat() - ufloat(r)
		elif isinstance(r, ufloat):
			return self.toufloat() - r
		elif isinstance(r, int):
			r = uint(r)

		if id(r) == id(self): 
			return uint(self.x - r.x, 0.0) 		# pathological case, x-x
		else: 
			return uint(self.x - r.x, math.sqrt((self.u*self.u) + (r.u**2)  - 2 * covariance))
	
	def __sub__(self, r: int|uint|float|ufloat):
		return self.sub(r)
	
	def __rsub__(self, left) -> uint:
		if isinstance(left, int):
			left = uint(left)
		elif isinstance(left, float):
			left = ufloat(left)
			
		return left - self

	def mul(self, r: int|uint, covariance: float = 0.0) -> uint:
		if isinstance(r, float):
			return self.toufloat() * ufloat(r)
		elif isinstance(r, ufloat):
			return self.toufloat() * r
		elif isinstance(r, int):
			r = uint(r)

		a = r.x**2 * self.u**2
		b = self.x**2 * r.u**2
		c = 2 * self.x * r.x * covariance

		return uint(self.x * r.x, math.sqrt(a + b + c))

	def __mul__(self, r) -> uint:
		return self.mul(r)
	
	def __rmul__(self, left) -> uint:
		if isinstance(left, int):
			left = uint(left)
		elif isinstance(left, float):
			left = ufloat(left)
			
		return left * self

	''' self operation returns a ufloat '''
	def __div(self, r: ufloat, covariance:float = 0.0) -> ufloat:
		if r == self:    		# pathological cases x/x
			return 1, 0.0
		elif r.u == 0.0:  		# r is a scalar
			return self.x / r.x, self.u / r.x 		# "self" may be a scalar, too
		elif self.u == 0.0:  		# "self is a scalar, r is not
			return self.x / r.x, r.u / (r.x**2)
		
		# both variables have associated uncertainty
		a: float = self.x / r.x		
		c: float = abs(((self.u**2) / r.x))
		d: float = (self.x**2 * r.u**2) / (r.x**4)
		e: float = abs((self.x * covariance)/(r.x**3))
		
		return a, math.sqrt(c + d - e)
	
	def div(self, r: uint|ufloat|int|float, covariance: float = 0.0) -> ufloat:
		return self.toufloat() / (ufloat(r) if isinstance(r, (int,float)) else r.toufloat())

	def __truediv__(self, r) -> uint:
		return self.div(r, 0.0)
	
	def __rtruediv__(self, left) -> uint:
		if isinstance(left, int):
			left = uint(left)
		elif isinstance(left, float):
			left = ufloat(left)
			
		return left / self
		
	def floordiv(self, r: uint|ufloat|int|float, covariance: float = 0.0) -> uint|ufloat:
		if isinstance(r, (int, uint)):
			x, u = self.__div(uint(r) if isinstance(r, int) else r , covariance)
			return uint(math.floor(x), u)
		elif isinstance(r, (float, ufloat)):
			return self.toufloat().floordiv(ufloat(r) if isinstance(r, float) else r, covariance)
		else:
			raise RuntimeError("Invalid divisor")
		
	def __floordiv__(self, r):
		return self.floordiv(r, 0.0)
	
	def __rfloordiv__(self, left):
		if isinstance(left, int):
			left = uint(left)
		elif isinstance(left, float):
			left = ufloat(left)
			
		return left // self

	def mod(self, r: int|uint, covariance: float = 0.0) -> uint|ufloat:
		if isinstance(r, int):
			r = uint(r)
	
		if id(r) == id(self):  		# pathological cases x/x
			return uint(0, 0.0)
		
		if isinstance(r, (float, ufloat)):
			return self.toufloat() % r
		elif isinstance(r, int):  		# r is a scalar
			return uint(self.x % r, self.u / r) 		# "self" may be a scalar, too
		elif r.u == 0.0:  		# r is a scalar
			return uint(self.x % r.x, self.u / r.x) 		# "self" may be a scalar, too
		elif self.u == 0.0: 		# "self is a scalar, r is not
			return uint(self.x % r.x, r.u / (r.x**2))
		
		# both variables have associated uncertainty
		a = self.x % r.x
		
		c = abs(((self.u**2) / r.x))
		d = (self.x**2 * r.u**2) / (r.x**4)
		e = abs((self.x * covariance) / (r.x**3))
		
		return uint(math.floor(a), math.sqrt(c + d - e))
		
	def __mod__(self, r: uint|int):
		if isinstance(r, int):
			return self.mod(uint(r))
		
		return self.mod(r)

	''' Rest of the type operations '''
	def abs(self) -> uint:
		return uint(abs(self.x), self.u)
	
	def __abs__(self) -> ufloat:
		return self.abs()
	
	def neg(self) -> uint:
		return uint(-self.x, self.u)
	
	def __neg__(self) -> uint:
		return self.neg()
	
	def power(self, s: float|int) -> uint:
		return (self.toufloat()**s).touint()
	
	def __pow__(self, s: float|int) -> uint:
		return self.power(s)
		
	def sqrt(self) -> uint:
		return self.toufloat().sqrt()

	def inverse(self) -> uint:
		return uint(1, 0.0).div(self, 0.0)
		
	def equals(self, r: uint) -> ubool:
		return self.toufloat() == r.toufloat()
	
	def distinct(self, r: uint) -> bool:
		return not self.equals(r)
	
	''' FuZZY COMPARISON OPERATIONS
		Assume ufloat values (x,u) represent standard uncertainty values, i.e., they follow a Normal distribution
	 	of mean x and standard deviation \sigma = u
	 '''
	def uEquals(self, r: uint|ufloat) -> ubool:
		if isinstance(r, (int, float)):
			r = ufloat(r)
		return self.toufloat() == r.toufloat()
	
	def eq(self, other) -> ubool:
		return self.uEquals(other)
	
	def __eq__(self, r: uint|ufloat) -> ubool:
		return self.uEquals(r)

	def uDistinct(self, r: uint|ufloat) -> ubool:
		if isinstance(r, (int, float)):
			r = ufloat(r)
		return ~self.uEquals(r)
	
	def ne(self, other) -> ubool:
		return self.uDistinct(other)
	
	def __ne__(self, r: uint|ufloat) -> ubool:
		return self.uDistinct(r)

	def lt(self, r: uint|ufloat) -> ubool:
		if isinstance(r, (int, float)):
			r = ufloat(r)
		return self.toufloat() < r.toufloat()
	
	def __lt__(self, r: uint|ufloat) -> ubool:
		return self.lt(r)

	def le(self, r: uint|ufloat) -> ubool:
		if isinstance(r, (int, float)):
			r = ufloat(r)
		return self.toufloat() <= r.toufloat()

	def __le__(self, r: uint|ufloat) -> ubool:
		return self.le(r)

	def gt(self, r: uint|ufloat) -> ubool:
		if isinstance(r, (int, float)):
			r = ufloat(r)
		return self.toufloat() > r.toufloat()
	
	def __gt__(self, r: uint|ufloat) -> ubool:
		return self.gt(r)
	
	def ge(self, r: uint|ufloat) -> ubool:
		if isinstance(r, (int, float)):
			r = ufloat(r)
		return self.toufloat() >= r.toufloat()
	
	def __ge__(self, r: uint|ufloat) -> ubool:
		return self.ge(r)

	''' END OF FuZZY COMPARISON OPERATIONS '''

	''' Conversions '''
	def __str__(self) -> str:
		return "uint({:d}, {:5.3f})".format(self.x, self.u)
    
	def __repr__(self) -> str:
		return self.__str__()

	def toint(self) -> int:
		return self.x
	
	def touint(self) -> uint:
		return self
	
	def tofloat(self) -> float: 
		return self.x
	
	def toufloat(self) -> ufloat:
		return ufloat(self.x, self.u)
	
	''' Other Methods '''
	def __hash__(self) -> int:
		return round(float(self.x))

	def copy(self) -> uint:
		return uint(self.x,self.u)

class ufloat:
	
    # Instance attributes:
    # x: float 
    # u: float 

	''' Initializer '''
	def __init__(self, x: float|int|str|tuple = 0.0, u: float|int|str = 0.0) -> ufloat:
		if isinstance(x, tuple) and len(x) == 2:
			x, u = x
		elif isinstance(x, (uint, ufloat)):
			u = x.u
			x = x.x
	
		if not isinstance(x, (float, int, str)):
			raise ValueError("Invalid parameter: x is not float, not int or float/int as string")
		elif not isinstance(u, (float, int, str)):
			raise ValueError("Invalid parameter: u is not float, not int or float/int as string")
		
		self.x = float(x)
		self.u = abs(float(u))

	@property
	def u(self):
		return self._u

	@u.setter
	def u(self, u: float):
		if not isinstance(u, float):
			raise ValueError("Invalid parameter: u not float")
		self._u = abs(u)

	def add(self, r: int|uint|float|ufloat, covariance: float = 0.0) -> ufloat:
		if isinstance(r, (int, uint, float)):
			r = ufloat(r)

		return ufloat(self.x + r.x, math.sqrt(self.u**2 + r.u**2  + 2 * covariance))

	def __add__(self, r) -> ufloat:
		return self.add(r)
	
	def __radd__(self, left) -> ufloat:
		return ufloat(left).add(self)

	def sub(self, r: int|uint|float|ufloat, covariance: float = 0.0) -> ufloat:
		if isinstance(r, (int, uint, float)):
			r = ufloat(r)

		if id(r) == id(self):
			return ufloat(self.x - r.x, 0.0)
		else:
			return ufloat(self.x - r.x, math.sqrt(self.u**2 + r.u**2 - 2 * covariance))

	def __sub__(self, other) -> ufloat:
		return self.sub(other)
	
	def __rsub__(self, left) -> ufloat:
		return ufloat(left).__sub__(self)

	def mul(self, r: int|uint|float|ufloat, covariance: float = 0.0) -> ufloat:
		if isinstance(r, (int, uint, float)):
			r = ufloat(r)
			
		x = self.x * r.x

		a = r.x**2 * self.u**2
		b = self.x**2 * r.u**2
		c = 2 * self.x * r.x * covariance

		return ufloat(x, math.sqrt(a + b + c))
	
	def __mul__(self, other) -> ufloat:
		return self.mul(other)
	
	def __rmul__(self, left) -> ufloat:
		return ufloat(left).__mul__(self)

	def __div(self, r: ufloat, covariance: float = 0.0) -> ufloat:
		if id(r) == id(self): # pathological cases: x/x
			return 1.0, 0.0
		elif r.u == 0.0: # r is a scalar
			return self.x / r.x, self.u / r.x # "self" may be a scalar, too
		elif self.u == 0.0: # "this is a scalar, r is not
			return self.x / r.x, r.u / (r.x**2)
		
		# both variables have associated uncertainty	
		
		a: float = self.x / r.x
		c: float = (self.u**2) / abs(r.x)
		d: float = (self.x**2 * r.u**2) / (r.x**4)
		if covariance == 0.0:	
			return a, math.sqrt(c + d)
		else:
			b: float = (self.x * r.u**2) / (r.x**3)
			e: float = (self.x * covariance) / abs(r.x**3)			
			return a + b, math.sqrt(c + d - e)
	
	def div(self, r: uint|ufloat|int|float, covariance: float = 0.0) -> ufloat:
		if isinstance(r, (int, uint)):
			return ufloat(self.__div(uint(r) if isinstance(r, int) else r.toufloat() , covariance))
		elif isinstance(r, (float, ufloat)):
			return ufloat(self.__div(ufloat(r) if isinstance(r, float) else r, covariance))
		else:
			raise RuntimeError("Invalid divisor")

	def __truediv__(self, other) -> ufloat:
		return self.div(other, 0.0)
	
	def __rtruediv__(self, left) -> ufloat:
		return ufloat(left).__truediv__(self)
	
	def floordiv(self, r: uint|ufloat|int|float, covariance: float = 0.0) -> ufloat:
		if isinstance(r, (int, uint)):
			x, u = self.__div(uint(r) if isinstance(r, int) else r.toufloat() , covariance)
			return ufloat(math.floor(x), u)
		elif isinstance(r, (float, ufloat)):
			x, u = self.__div(ufloat(r) if isinstance(r, float) else r, covariance)
			return ufloat(math.floor(x), u)
		else:
			raise RuntimeError("Invalid divisor")

	def __floordiv__(self, r):
		return self.floordiv(r, 0.0)
	
	def __rfloordiv__(self, left):
		return ufloat(left).__floordiv__(self)

	def abs(self) -> ufloat:
		return ufloat(abs(self.x), self.u)
	
	def __abs__(self) -> ufloat:
		return self.abs()

	def neg(self) -> ufloat:
		return ufloat(-self.x, self.u)

	def __neg__(self) -> ufloat:
		return self.neg()
	
	def power(self, s: float|int) -> ufloat:
		a = self.x**s
		c = s * self.u * (self.x**(s-1))

		return ufloat(a, c)
	
	def __pow__(self, s: float|int) -> ufloat:
		return self.power(s)
	
	def sqrt(self) -> ufloat:
		if self.x == 0.0 and self.u == 0.0:
			return ufloat(0.0, 0.0)
		elif self.x < 0.0:
			raise ValueError('math domain error: negative number')
		
		x = math.sqrt(self.x)
		u = (self.u) / (2 * math.sqrt(self.x))
		
		return ufloat(x, u)

	def sin(self) -> ufloat:
		return ufloat(math.sin(self.x), self.u * math.cos(self.x))

	def cos(self) -> ufloat:
		return ufloat(math.cos(self.x), self.u * math.sin(self.x))
	
	def tan(self) -> ufloat:
		return self.sin().div(self.cos()) 
	
	def atan(self) -> ufloat:
		return ufloat(math.atan(self.x), self.u / (1 + self.x**2))
	
	''' Type Operations '''

	def acos(self) -> ufloat:
		if abs(self.x) == 1.0:
			return ufloat(math.acos(self.x), self.u)
		else:
			return ufloat(math.acos(self.x), self.u / math.sqrt(1 - self.x**2))

	def asin(self) -> ufloat:
		if abs(self.x) == 1.0:
			return ufloat(math.asin(self.x), self.u)
		else:
			return ufloat(math.asin(self.x), self.u/math.sqrt((1 - self.x**2)))

	def inverse(self) -> ufloat: #inverse (reciprocal)
		return ufloat(1.0, 0.0) / self

	def floor(self) -> ufloat: #returns (i,u) with i the largest int such that (i,u)<=(x,u)
		return ufloat(math.floor(self.x),self.u)

	def round(self) -> ufloat: #returns (i,u) with i the closest int to x
		return ufloat(round(self.x), self.u)

	''' Comparison operations '''
	def equals(self, other) -> bool:
		''' we compute the separation factor of the two distributions considered as a mixture
		 	see http:#faculty.washington.edu/tamre/IsHumanHeightBimodal.pdf '''
		if id(self) == id(other): return True
		
		s1 = self.u
		s2 = other.u
		# non-ufloat cases first
		if s1 == 0 or s2 == 0:
			return self.x == other.x
		# if both numbers have some uncertainty
		r = (s1 * s1) / (s2 * s2)

		S = math.sqrt(-2.0 + 3*r + 3*r*r - 2*r*r*r + 2 * math.pow(1 - r + r*r, 1.5) ) / (math.sqrt(r) * (1 + math.sqrt(r)))
		if math.isnan(S): # similar to s1==0 or s2==0. No way to compute the separation test
			return (self.x == other.x)
		
		separation = S * (s1 + s2)
		return abs(other.x - self.x) <= separation # they are indistinguishable

	def distinct(self, other) -> bool:
		return not self.equals(other)
	
	''' FUZZY COMPARISON OPERATIONS
	    Assume ufloat values (x,u) represent standard uncertainty values, i.e., they follow a Normal distribution
	    of mean x and standard deviation \sigma = u
	'''
	
	''' Let's start by some Gaussian operations
		returns the cumulative normal distribution function (CNDF) for a standard normal: N(0,1)
   	'''	   
	def CNDF(self, x: float, mu: float = None, sigma: float = None) -> float:
		# See http:#stackoverflow.com/questions/442758/which-java-library-computes-the-cumulative-standard-normal-distribution-function
		# and https:#lyle.smu.edu/~aleskovs/emis/sqc2/accuratecumnorm.pdf
		if mu is not None and sigma is not None:
			return self.CNDF((x - mu) / sigma)
		
		neg = 1 if x < 0.0 else 0
		if neg == 1:
			x *= -1.0
		k = 1 / ( 1 + 0.2316419 * x)
		y = (((( 1.330274429 * k - 1.821255978) * k + 1.781477937) * k - 0.356563782) * k + 0.319381530) * k
		y = 1.0 - 0.398942280401 * math.exp(-0.5 * x**2) * y
		return (1 - neg) * y + neg * (1 - y)

	''' alternative implementation -- they both work equally well '''
	def CNDF2(self, z: float, mu: float = None, sigma: float = None) -> float:
		if mu is None and sigma is None:
			return self.CNDF((z - mu) / sigma)
		
		if z < -8.0: return 0.0
		if z >  8.0: return 1.0
		sum = 0.0
		term = z
		i = 3
		while sum + term != sum:
			sum  = sum + term
			term = term * z * z / i
			i+=2

		return 0.5 + sum * self.pdf(z)
	
	# returns pdf(x) = standard Gaussian pd
	def pdf(self, x: float, mu: float = None, sigma: float = None) -> float:
		if mu is None and sigma is None:
			return math.exp(-x**2 / 2) / math.sqrt(2 * math.PI)
		else:
			return self.pdf((x - mu) / sigma) / sigma
	     
	# Compute z such that cdf(z) = y via bisection search
	# taken from http:#introcs.cs.princeton.edu/java/22library/Gaussian.java.html
	def inverseCNDF(self, y: float, delta: float = None, lo: float = None, hi: float = None) -> float:
		if delta is None and lo is None and hi is None:
			return self.inverseCNDF(y, 0.00000001, -8, 8)
		mid = lo + (hi - lo) / 2
		if hi - lo < delta:
			return mid
		elif self.CNDF(mid) > y:
			return self.inverseCNDF(y, delta, lo, mid)
		else:
			return self.inverseCNDF(y, delta, mid, hi)  
    
	'''Now we start with the fuzzy functions	'''
    

	''' This method returns three numbers (lt, eq, gt) with the probabilities that 
	 	lt: this < number, 
     	eq: this = number
     	gt: this > number
	'''
	def calculate(self, number: ufloat|uint) -> Result:
		r = Result()
		m1 = 0.0; m2 = 0.0; s1 = 0.0; s2 = 0.0; swap = False

		if self.x <= number.x: # m1 is less or equal than m2
			m1 = self.x; m2 = float(number.x); s1 = self.u; s2 = number.u
		else:
			m2 = self.x; m1 = float(number.x); s2 = self.u; s1 = number.u
			swap = True # to return values in the correct order

		if s1 == 0.0 and s2 == 0.0: #comparison between Real numbers
			if m1 == m2:
				r.lt = 0.0; r.eq = 1.0; r.gt = 0.0 
				return r.check(swap) 
	
			if m1 < m2:
				r.lt = 1.0; r.eq = 0.0; r.gt = 0.0 
				return r.check(swap) 
	
			r.lt = 0.0; r.eq = 0.0; r.gt = 1.0 
			return r.check(swap) 

		if s1 == 0.0: # s1 is degenerated, s2 is not
			r.lt = 1 - self.CNDF(m1,m2,s2) 
			r.eq = 0.0
			r.gt = self.CNDF(m1,m2,s2) 
			return r.check(swap) 

		if s2 == 0.0: # s2 is degenerated, s1 is not
			r.lt = self.CNDF(m2,m1,s1)
			r.eq = 0.0
			r.gt = 1-self.CNDF(m2,m1,s1) 
			return r.check(swap) 

		# here none of the numbers are degenerated
		if s1 == s2: 
			crossing = (m1 + m2)/2
			r.lt = self.CNDF(crossing, m1, s1) - self.CNDF(crossing, m2, s2)
			r.gt = 0.0 
			r.eq = 1.0 - (r.gt + r.lt) 
			return r.check(swap) 
		else:
			crossing1 = -(-m2*s1**2 + m1*s2*s2 +
					s1 * s2 * math.sqrt( (m1-m2) * (m1-m2) - 2.0 * (s1**2 - s2**2) * math.log(s2 / s1))
				 ) / (s1**2 - s2**2)	
			crossing2 = (m2*s1**2 - m1*s2**2 +
					s1 * s2 * math.sqrt( (m1-m2) * (m1-m2) - 2.0 * (s1**2 - s2**2) * math.log(s2 / s1))
				) / (s1**2 - s2**2)
			
			c1 = min(crossing1, crossing2)
			c2 = max(crossing1, crossing2)
			if s1 < s2:
				r.gt = self.CNDF(c1, m2, s2) - self.CNDF(c1, m1, s1)
				r.lt = 1.0 - self.CNDF(c2, m2, s2) - (1.0-self.CNDF(c2, m1, s1))
				r.eq = self.CNDF(c1, m1, s1) + (1.0 - self.CNDF(c2, m1, s1)) + self.CNDF(c2,m2,s2) - self.CNDF(c1,m2,s2)
			else:
				r.lt = self.CNDF(c1, m1, s1)-self.CNDF(c1, m2, s2)
				r.gt = 1.0 - self.CNDF(c2, m1, s1) - (1.0 - self.CNDF(c2, m2, s2))
				r.eq = self.CNDF(c1, m2, s2) + (1.0 - self.CNDF(c2, m2, s2)) + self.CNDF(c2,m1,s1) - self.CNDF(c1,m1,s1)
	
			return r.check(swap) 
		
	def uEquals(self, other: uint|ufloat) -> ubool:
		if isinstance(other, (int, float)):
			other = ufloat(other)
		r = self.calculate(other.toufloat())
		return ubool(r.eq)

	def eq(self, other) -> ubool:
		return self.uEquals(other)

	def __eq__(self, other) -> ubool:
		return self.eq(other)

	def uDistinct(self, other: uint|ufloat) -> ubool:
		if isinstance(other, (int, float)):
			other = ufloat(other)
		return ~self.uEquals(other)
	
	def ne(self, other) -> ubool:
		if isinstance(other, (int, float)):
			other = ufloat(other)
		return self.uDistinct(other)

	def __ne__(self, other) -> ubool:
		return self.uDistinct(other)

	def lt(self, number: uint|ufloat) -> ubool:
		r = self.calculate(ufloat(number) if isinstance(number, (int, float)) else number.toufloat())
		return ubool(r.lt)
	
	def __lt__(self, number: uint|ufloat) -> ubool:
		return self.lt(number)
	
	def le(self, number: uint|ufloat) -> ubool:
		r = self.calculate(ufloat(number) if isinstance(number, (int, float)) else number.toufloat())
		return ubool(r.lt + r.eq)

	def __le__(self, number: uint|ufloat) -> ubool:
		return self.le(number)

	def gt(self, number: uint|ufloat) -> ubool:
		r = self.calculate(ufloat(number) if isinstance(number, (int, float)) else number.toufloat())
		return ubool(r.gt)
	
	def __gt__(self, number: uint|ufloat) -> ubool:
		return self.gt(number)
	
	def ge(self, number: uint|ufloat) -> ubool:
		r = self.calculate(ufloat(number) if isinstance(number, (int, float)) else number.toufloat())
		return ubool(r.gt + r.eq)
	
	def __ge__(self, number: uint|ufloat) -> ubool:
		return self.ge(number)

	''' END OF FUZZY COMPARISON OPERATIONS '''

	''' Conversions '''
	def toint(self) -> int:
		return int(math.floor(self.x))

	def touint(self) -> uint:
		x = int(math.floor(self.x))
		u = math.sqrt((self.u * self.u) + (self.x - x) * (self.x - x))
		return uint(x, u)
	
	def tofloat(self) -> float: 
		return self.x
	
	def toufloat(self) -> ufloat: 
		return self

	def toBestuint(self) -> uint:
		x = int(round(self.x))
		u = math.sqrt((self.u * self.u) + (self.x - x) * (self.x - x))
		return uint(x, u)

	''' Other Methods '''
	def __hash__(self):
		return round(self.x)
	
	def copy(self) -> ufloat:
		return ufloat(self.x, self.u)

	''' Conversions '''
	def __str__(self) -> str:
		return "ufloat({:5.3f}, {:5.3f})".format(self.x, self.u)
    
	def __repr__(self) -> str:
		return self.__str__()