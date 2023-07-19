from __future__ import annotations

# Aux classes
class Result:
	def __init__(self, lt: float = 0.0, eq: float = 1.0, gt: float = 0.0):
		self.lt = lt
		self.eq = eq
		self.gt = gt
	#swap the values if swap == true
	def check(self, swap: bool) -> Result: 
		if not swap:
			return self
		return Result(self.gt, self.eq, self.lt)