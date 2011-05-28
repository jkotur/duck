
import sys

import numpy as np
import random as rnd

from OpenGL.GL import *

import shaders as sh

import membrane

class Water :
	def __init__( self , n = 256 ) :
		self.n = n
		self.h = 2.0 / (self.n-1)
		self.c = 1.0
		self.maxdt = 1.0 / self.n
		self.w1 = np.zeros( (self.n,self.n) , np.float32 )
		self.w2 = np.zeros( (self.n,self.n) , np.float32 )

		self.norm= np.zeros( (self.n,self.n,3) , np.float32 )

		self.drop_time = 0.0
		self.next_drop = rnd.uniform(0.0,2.0)

		self.prog = self.loc_mmv = self.loc_mp = self.loc_norms = 0

	def gfx_init( self ) :
		self._mk_texture()
		self._mk_shaders()

	def get( self , x , y ) :
		return self.w1[x][y]

	def set( self , x , y , v ) :
		self.w1[x][y] = v

	def add( self , x , y , v ) :
		self.w1[x][y]+= v

	def drop( self , x , y ) :
		self.add( x , y , rnd.gauss(-0.5,0.25) )

	def drop_rnd( self ) :
		self.drop( rnd.uniform(0.0,self.n) , rnd.uniform(0.0,self.n) )

	def step( self , dt ) :
		self._up_drop(dt)
		self._up_water(dt)

	def _up_drop( self , dt ) :
		self.drop_time += dt
		while self.drop_time >= self.next_drop :
			self.drop_time -= self.next_drop
			self.next_drop  = rnd.uniform(0.0,2.0)
			self.drop_rnd()
			print self.drop_time , self.next_drop

	def _up_water( self , dt ) :
		t = 0.0
		while t < dt :
#            print dt , self.maxdt
			membrane.step( self.w1 , self.w2 , self.n , self.h , self.c , min(dt,self.maxdt) )
			self.w1 , self.w2 = self.w2 , self.w1
			t += self.maxdt

		self._up_texture( self.w1 )

	def _mk_texture( self ) :
		self.ntex = glGenTextures( 1 )
		glBindTexture(GL_TEXTURE_2D, self.ntex )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S    , GL_CLAMP  )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T    , GL_CLAMP  )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		glTexImage2D(GL_TEXTURE_2D,0,GL_RGB16F,self.n,self.n,0,GL_RGB,GL_FLOAT,self.norm)
		glBindTexture(GL_TEXTURE_2D, 0)

	def _mk_shaders( self ) :
		try : 
			self.prog = sh.compile_program('shad/water')

			self.loc_mmv   = sh.get_loc(self.prog,'modelview' )
			self.loc_mp    = sh.get_loc(self.prog,'projection')
			self.loc_norms = sh.get_loc(self.prog,'normalmap' )
			self.loc_cube  = sh.get_loc(self.prog,'cubemap'   )
			self.loc_cam   = sh.get_loc(self.prog,'campos'    )
		except ValueError as ve :
			print "Shader compilation failed: " + str(ve)
			sys.exit(0)    

	def _up_texture( self , w ) :
		membrane.to_normals( w , self.norm , self.n )
		glBindTexture(GL_TEXTURE_2D, self.ntex )
		glTexImage2D(GL_TEXTURE_2D,0,GL_RGB16F,self.n,self.n,0,GL_RGB,GL_FLOAT,self.norm)
		glBindTexture(GL_TEXTURE_2D, 0)

	def draw( self , cube_tex , cam_mat ) :
		glUseProgram( self.prog )
                 
		mmv = glGetFloatv(GL_MODELVIEW_MATRIX)
		mp  = glGetFloatv(GL_PROJECTION_MATRIX)
		cam_pos = np.dot(np.array((0,0,0,1)),np.linalg.inv(cam_mat))
						 
		glUniformMatrix4fv(self.loc_mmv,1,GL_FALSE,mmv)
		glUniformMatrix4fv(self.loc_mp ,1,GL_FALSE,mp )
		glUniform1i(self.loc_norms,0)
		glUniform1i(self.loc_cube ,1)
		glUniform3f(self.loc_cam,cam_pos[0],cam_pos[1],cam_pos[2])

		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.ntex )
		glActiveTexture(GL_TEXTURE1)
		glBindTexture(GL_TEXTURE_CUBE_MAP, cube_tex )

		glBegin(GL_QUADS)
		glNormal3f( 0,1, 0)
		glTexCoord2d(0,0)
		glVertex3f(-1,0,-1)
		glTexCoord2d(0,1)
		glVertex3f(-1,0, 1)
		glTexCoord2d(1,1)
		glVertex3f( 1,0, 1)
		glTexCoord2d(1,0)
		glVertex3f( 1,0,-1)
		glEnd()

		glBindTexture(GL_TEXTURE_CUBE_MAP, 0 )
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, 0)

		glUseProgram( 0 )

