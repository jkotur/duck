
import numpy as np
import random as rnd

from OpenGL.GL import *

import membrane

class Water :
	def __init__( self , n = 256 ) :
		self.n = n
		self.h = 2.0 / (self.n-1)
		self.c = 1.0
		self.maxdt = 1.0 / self.n
		self.w1 = np.zeros( self.n*self.n , np.float32 )
		self.w2 = np.zeros( self.n*self.n , np.float32 )

		self.drop_time = 0.0
		self.next_drop = rnd.uniform(0.0,2.0)

	def get( self , x , y ) :
		return self.w1[ x + y * self.n ]

	def set( self , x , y , v ) :
		self.w1[ x + y * self.n ] = v

	def add( self , x , y , v ) :
		self.w1[ x + y * self.n ]+= v

	def drop( self , x , y ) :
		self.add( x , y , rnd.gauss(-0.25,0.5) )

	def drop_rnd( self ) :
		self.drop( rnd.uniform(0.0,2.0) , rnd.uniform(0.0,2.0) )

	def step( self , dt ) :
		self._up_drop(dt)
		self._up_water(dt)

	def _up_drop( self , dt ) :
		self.drop_time += dt
		while self.drop_time >= self.next_drop :
			self.drop_time -= self.next_drop
			self.drop_time += rnd.uniform(0.0,2.0)
			self.drop_rnd()

	def _up_water( self , dt ) :
		t = 0.0
		while t < dt :
#            print dt , self.maxdt
			membrane.step( self.w1 , self.w2 , self.n , self.h , self.c , min(dt,self.maxdt) )
			self.w1 , self.w2 = self.w2 , self.w1
			t += self.maxdt

	def draw( self ) :
		glBegin(GL_LINES)
		glVertex3f(0,self.get(0,0),0)
		for i in range(1,self.n-1) :
			for j in range(1,self.n-1) :
				glColor3f(self.get(i,j),.5,0)
				glVertex3f(.1*i,self.get(i,j),.1*j)
				glVertex3f(.1*i,self.get(i,j),.1*j)
		glVertex3f(.1*(self.n-1),self.get(self.n-1,self.n-1),.1*(self.n-1))
		glVertex3f(0,self.get(0,0),0)
		for j in range(1,self.n-1) :
			for i in range(1,self.n-1) :
				glColor3f(self.get(i,j),.5,0)
				glVertex3f(.1*i,self.get(i,j),.1*j)
				glVertex3f(.1*i,self.get(i,j),.1*j)
		glVertex3f(.1*(self.n-1),self.get(self.n-1,self.n-1),.1*(self.n-1))
		glEnd()

