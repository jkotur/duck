
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

if sys.platform.startswith('win') :
	timer = time.clock
else:
	timer = time.time

class Scene :
	def __init__( self , fov , ratio , near , far  , skybox_img ) :
		self.fov = fov
		self.far = far
		self.near = near 
		self.ratio = ratio

		self.last_time = timer()

		self.water = Water( 256 )
		self.box   = Skybox( skybox_img )

		self.water.drop_rnd()

	def gfx_init( self ) :
		self.camera = Camera( ( 0 , 5 ,  0 ) , ( 1 , 1 , 0 ) , ( 1 , 0 , 0 ) )
		self._update_proj()

		self.water.gfx_init()
		self.box.gfx_init()

	def draw( self ) :
		self.time = timer()
		dt = self.time - self.last_time

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
			   
		self.camera.look()

		self.box.draw()

		self.water.step( dt )
		self.water.draw()

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
		self.camera.move( *map( lambda x : x*.25 , mv ) )

	def _update_proj( self ) :                                         
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective( self.fov , self.ratio , self.near , self.far )
		glMatrixMode(GL_MODELVIEW)

