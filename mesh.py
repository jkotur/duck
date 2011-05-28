import sys

import math as m
import numpy as np

from OpenGL.GL import *

import shaders as sh

class Mesh :
	def __init__( self , path , img , shad ) :
		self._from_path( path )
		self.img = img
		self.shad_path = shad
		self.tex = 0
		self.prog = 0

	def gfx_init( self ) :
		self._load_img( self.img )
		self._load_shader( self.shad_path )

	def _load_shader( self , path ) :
		try : 
			self.prog = sh.compile_program(path)

			self.loc_mmv   = sh.get_loc(self.prog,'modelview' )
			self.loc_mp    = sh.get_loc(self.prog,'projection')
			self.loc_tex   = sh.get_loc(self.prog,'texture'   )
			self.loc_light = sh.get_loc(self.prog,'light'     )
			self.loc_anix  = sh.get_loc(self.prog,'xdir'      )
		except ValueError as ve :
			print "Shader compilation failed: " + str(ve)
			sys.exit(0)    

	def draw( self , pos , dir , lpos ) :
		glEnableClientState( GL_VERTEX_ARRAY )
		glEnableClientState( GL_NORMAL_ARRAY )
		glEnableClientState( GL_TEXTURE_COORD_ARRAY )

		glVertexPointer  ( 3 , GL_FLOAT , 0 , self.verts )
		glNormalPointer  (     GL_FLOAT , 0 , self.norms )
		glTexCoordPointer( 2 , GL_FLOAT , 0 , self.coord )

		mmv = glGetFloatv(GL_MODELVIEW_MATRIX)
		lpos = np.resize(lpos,4)
		lpos[3] = 1.0;
		lpos = np.dot( lpos , mmv )
						 
		glPushMatrix()
		glTranslatef( pos[0] , 0 , pos[1] )
		glRotatef( m.atan2( dir[0] , dir[1] )*180.0/m.pi + 90.0 , 0 , 1 , 0 )
		glScalef(.001,.001,.001)

		glUseProgram( self.prog )

		mmv = glGetFloatv(GL_MODELVIEW_MATRIX)
		mp  = glGetFloatv(GL_PROJECTION_MATRIX)

		xdir = np.dot( np.array((1,0,0,0)),mmv )

		glUniformMatrix4fv(self.loc_mmv,1,GL_FALSE,mmv)
		glUniformMatrix4fv(self.loc_mp ,1,GL_FALSE,mp )
		glUniform1i(self.loc_tex,0)
		glUniform3f(self.loc_light,lpos[0],lpos[1],lpos[2])
		glUniform3f(self.loc_anix ,xdir[0],xdir[1],xdir[2])

		glBindTexture( GL_TEXTURE_2D , self.tex )

		glDrawElements( GL_TRIANGLES , len(self.ind) , GL_UNSIGNED_INT , self.ind )

		glUseProgram( 0 )

		glPopMatrix()

		glDisableClientState( GL_VERTEX_ARRAY )
		glDisableClientState( GL_NORMAL_ARRAY )
		glDisableClientState( GL_TEXTURE_COORD_ARRAY )

	def _from_path( self , path ) :
		with open(path,"r+") as f :
			self._from_file(f)

	def _from_file( self , f ) :
		V = int(f.readline())
		self.verts = np.empty( (V,3) , np.float32 )
		self.norms = np.empty( (V,3) , np.float32 )
		self.coord = np.empty( (V,2) , np.float32 )
		for v in range(V) :
			vx , vy , vz , nx , ny , nz , ts , tt = map( float , f.readline().split(' ') )
			self.verts[v] = vx , vy , vz
			self.norms[v] = nx , ny , nz
			self.coord[v] = ts , tt

		T = int(f.readline())
		self.ind = np.empty( T*3 , np.uint )
		for t in range(0,T*3,3) :
			self.ind[t  ] , self.ind[t+1] , self.ind[t+2] = map( int , f.readline().split(' ') )

	def _load_img( self , img ) :
		self.tex = glGenTextures( 1 )
		glBindTexture(GL_TEXTURE_2D, self.tex )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S    , GL_CLAMP  )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T    , GL_CLAMP  )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,img.w,img.h,0,GL_RGB,GL_UNSIGNED_BYTE,img.data)
		glBindTexture(GL_TEXTURE_2D, 0)
