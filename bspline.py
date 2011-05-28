
import random as rnd

import numpy as np

def rekN( n , i ,  t ) :
	if n == 0 : return 1 if t >= i and t < i + 1 else 0
	n1 = rekN(n - 1, i, t)
	n2 = rekN(n - 1, i + 1, t)
	return n1 * float(t - i) / float(n) + n2 * float(i + n + 1 - t) / float(n)

class BSpline :
	def __init__( self , xbounds , ybounds ) :
		self.nums = 512
		self.xb = xbounds
		self.yb = ybounds
		self._init_bspline()
		self.pts  = [ self._rand() for i in range(4) ]
		self.futr = None
		self.curr = None
		self.prev = None
		self.next(1)
		self.next(1)

	def _init_bspline( self ) :
		self.ncache = {}
		self.t = 3.0
		i = 0
		for t in np.linspace(3,4,self.nums) :
			for j in range(4) :
				self.ncache[ (j,i) ] = rekN( 3 , j , t )
			i+=1

	def _new( self , p ) :
		self.pts.append(p)
		self.pts.pop(0)

	def _rand( self ) :
		return np.array( (rnd.uniform(*self.xb),rnd.uniform(*self.yb)) )

	def rand( self ) :
		self._new( self._rand() )

	def calc( self , t ) :
		p = np.zeros(2)
		for j in range(4) :          
			p += self.pts[j] * self.ncache[ (j,t) ]       
		return p

	def next( self , dt ) :
		self.t += 1
		if self.t >= self.nums :
			self.t -= self.nums
			self.rand()
		self.prev = self.curr
		self.curr = self.futr
		self.futr = self.calc( self.t )
		return self.curr

	@property
	def value( self ) :
		return self.curr

	@property
	def tangent( self ) :
		return self.futr - self.prev

