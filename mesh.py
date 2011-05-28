
import math as m
import numpy as np

from OpenGL.GL import *

class Mesh :
	def __init__( self , path , img ) :
		self._from_path( path )
		self.img = img
		self.tex = 0

	def gfx_init( self ) :
		self._load_img( self.img )

	def draw( self , pos , dir ) :
		glEnableClientState( GL_VERTEX_ARRAY )
		glEnableClientState( GL_NORMAL_ARRAY )
		glEnableClientState( GL_TEXTURE_COORD_ARRAY )

		glVertexPointer  ( 3 , GL_FLOAT , 0 , self.verts )
		glNormalPointer  (     GL_FLOAT , 0 , self.norms )
		glTexCoordPointer( 2 , GL_FLOAT , 0 , self.coord )

		glEnable( GL_TEXTURE_2D )
		glBindTexture( GL_TEXTURE_2D , self.tex )

		glPushMatrix()
		glTranslatef( pos[0] , 0 , pos[1] )
		glRotatef( m.atan2( dir[0] , dir[1] )*180.0/m.pi + 90.0 , 0 , 1 , 0 )
		glScalef(.001,.001,.001)

		glDrawElements( GL_TRIANGLES , len(self.ind) , GL_UNSIGNED_INT , self.ind )

		glPopMatrix()

		glDisable( GL_TEXTURE_2D )
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
