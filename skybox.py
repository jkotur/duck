
import numpy as np

from OpenGL.GL import *

cube_tex = [
		GL_TEXTURE_CUBE_MAP_POSITIVE_X , 
		GL_TEXTURE_CUBE_MAP_NEGATIVE_X ,
		GL_TEXTURE_CUBE_MAP_POSITIVE_Y ,
		GL_TEXTURE_CUBE_MAP_NEGATIVE_Y ,
		GL_TEXTURE_CUBE_MAP_POSITIVE_Z ,
		GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
		]

class Skybox :
	def __init__( self , img ) :
		self.img = img
		self.tex = 0

	@property
	def texture( self ) :
		return self.tex

	def gfx_init( self ) :
		self._mk_texture() 
		self._mk_box()

	def _mk_texture( self ) :
		self.tex = glGenTextures( 1 )
		glBindTexture(GL_TEXTURE_CUBE_MAP, self.tex )
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S    , GL_CLAMP  )
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T    , GL_CLAMP  )
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		for i in range(6) :
			glTexImage2D(cube_tex[i],0,GL_RGBA,self.img.width,self.img.height,0,GL_RGBA,GL_UNSIGNED_BYTE,self.img.datas[i])
		glBindTexture(GL_TEXTURE_CUBE_MAP,0)

	def _mk_box( self ) :
		self.verts = np.array( ((-1,-1,-1),(-1,-1,1),(-1,1,1),(1,1,1),(1,-1,1),(1,-1,-1),(1,1,-1),(-1,1,-1)) , np.float32 )
		self.ind   = np.array( (7,2,1,0, 6,5,4,3, 0,1,4,5, 7,6,3,2, 0,5,6,7, 1,2,3,4) , np.uint32 )

	def draw( self ):
		glEnable(GL_CULL_FACE)
		glEnable(GL_AUTO_NORMAL)
		glEnable(GL_DEPTH_TEST)

		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_TEXTURE_COORD_ARRAY)

		glEnable(GL_TEXTURE_CUBE_MAP)
		glBindTexture(GL_TEXTURE_CUBE_MAP , self.tex )

		glVertexPointer( 3, GL_FLOAT , 0 , self.verts )
		glTexCoordPointer( 3 ,GL_FLOAT , 0 , self.verts )
		glDrawElements( GL_QUADS , len(self.ind) , GL_UNSIGNED_INT , self.ind )

		glDisable(GL_TEXTURE_CUBE_MAP)

		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_TEXTURE_COORD_ARRAY)

