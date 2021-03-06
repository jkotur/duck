
import sys , time 

import math as m
import numpy as np
import numpy.linalg as la

import random as rnd

import operator as op

from OpenGL.GL import *
from OpenGL.GLU import *

from water import Water
from skybox import Skybox
from camera import Camera
from mesh import Mesh
from bspline import BSpline

if sys.platform.startswith('win') :
	timer = time.clock
else:
	timer = time.time

class Scene :
	def __init__( self , fov , ratio , near , far  , skybox_img , duck_img ) :
		self.fov = fov
		self.far = far
		self.near = near 
		self.ratio = ratio

		self.last_time = timer()

		self.water = Water( 128 )
		self.box   = Skybox( skybox_img )
		self.duck  = Mesh( 'data/duck.gpt' , duck_img , 'shad/anisotropic' )
		self.path  = BSpline( (-1,1) , (-1,1) )

		self.light = np.array( (0,2,0) )

		self.water.drop_rnd()

	def gfx_init( self ) :
		self.camera = Camera( ( 0 , 5 ,  0 ) , ( 1 , 1 , 0 ) , ( 1 , 0 , 0 ) )
		self._update_proj()

		self.water.gfx_init()
		self.box  .gfx_init()
		self.duck .gfx_init()

	def draw( self ) :
		self.time = timer()
		dt = self.time - self.last_time

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
			   
		self.camera.look()

		self.box.draw()

		self.path.next( dt )
		self.water.drop( *((self.path.value+1.0)*self.water.n/2.0) ,
				force = np.linalg.norm(self.path.tangent)*25 )
		self.water.step( dt * .5 )
		self.water.draw( self.box.texture , self.camera.matrix )

		self.duck.draw( self.path.value , self.path.tangent , self.light )

		self.last_time = self.time

	def set_fov( self , fov ) :
		self.fov = fov
		self._update_proj()

	def set_near( self , near ) :
		self.near = near
		self._update_proj()

	def set_ratio( self , ratio ) :
		self.ratio = ratio
		self._update_proj()

	def set_screen_size( self , w , h ) :
		self.width  = w 
		self.height = h
		self.set_ratio( float(w)/float(h) )

	def set_fov( self , fov ) :
		self.fov = fov
		self._update_proj()

	def set_near( self , near ) :
		self.near = near
		self._update_proj()

	def set_ratio( self , ratio ) :
		self.ratio = ratio
		self._update_proj()

	def set_screen_size( self , w , h ) :
		self.width  = w
		self.height = h
		self.set_ratio( float(w)/float(h) )

	def mouse_move( self , df ) :
		self.camera.rot( *map( lambda x : -x*.2 , df ) )

	def key_pressed( self , mv ) :
		self.camera.move( *map( lambda x : x*.05 , mv ) )

	def _update_proj( self ) :                                         
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective( self.fov , self.ratio , self.near , self.far )
		glMatrixMode(GL_MODELVIEW)

