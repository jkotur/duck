import sys

import pygtk
pygtk.require('2.0')
import gtk

import operator as op

from OpenGL.GL import *

from glwidget import GLDrawingArea

from scene import Scene
from image import Image , CubeImage

ui_file = "duck.ui"
skybox_files = [ "data/cube{0}.png".format(i) for i in range(6) ]
duck_file = 'data/ducktex.jpg'

class App(object):
	"""Application main class"""

	def __init__(self):

		self._init_keyboard()

		self.near = 1
		self.far  = 1000
		self.fov  = 60

		builder = gtk.Builder()
		builder.add_from_file(ui_file)

		glconfig = self.init_glext()

		self.drawing_area = GLDrawingArea(glconfig)
		self.drawing_area.set_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON3_MOTION_MASK )
		self.drawing_area.set_size_request(800, 800)

		builder.get_object("vbox1").pack_start(self.drawing_area)

		self.scene = Scene( self.fov , 1 , self.near , self.far , self._load_cube_img(skybox_files) , self._load_img(duck_file) )
		self.drawing_area.add( self.scene )

		win_main = builder.get_object("win_main")

		win_main.connect('key-press-event'  , self._on_key_pressed  )
		win_main.connect('key-release-event', self._on_key_released )

		win_main.show_all()

		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height
		ratio = float(width)/float(height)

		self.scene.set_ratio( ratio )

		builder.connect_signals(self)

		self.statbar = builder.get_object('statbar')

		self.drawing_area.connect('motion_notify_event',self._on_mouse_motion)
		self.drawing_area.connect('button_press_event',self._on_button_pressed)
		self.drawing_area.connect('configure_event',self._on_reshape)
		self.drawing_area.connect_after('expose_event',self._after_draw)

		gtk.timeout_add( 1 , self._refresh )

	def _init_keyboard( self ) :
		self.move = [0,0,0]
		self.dirskeys = ( ( ['w'] , ['s'] ) , ( ['a'] , ['d'] ) , ( ['e'] , ['q'] ) )

		for d in self.dirskeys :
			for e in d : 
				for i in range(len(e)) : e[i] = ( gtk.gdk.unicode_to_keyval(ord(e[i])) , False )

	def _on_key_pressed( self , widget , data=None ) :
		if not any(self.move) :
			gtk.timeout_add( 20 , self._move_callback )
						  
		for i in range(len(self.dirskeys)) :
			if (data.keyval,False) in self.dirskeys[i][0] :
				self.dirskeys[i][0][ self.dirskeys[i][0].index( (data.keyval,False) ) ] = (data.keyval,True)
				self.move[i]+= 1
			elif (data.keyval,False) in self.dirskeys[i][1] :
				self.dirskeys[i][1][ self.dirskeys[i][1].index( (data.keyval,False) ) ] = (data.keyval,True)
				self.move[i]-= 1

	def _on_key_released( self , widget , data=None ) :
		for i in range(len(self.dirskeys)) :
			if (data.keyval,True) in self.dirskeys[i][0] :
				self.dirskeys[i][0][ self.dirskeys[i][0].index( (data.keyval,True) ) ] = (data.keyval,False)
				self.move[i]-= 1
			elif (data.keyval,True) in self.dirskeys[i][1] :
				self.dirskeys[i][1][ self.dirskeys[i][1].index( (data.keyval,True) ) ] = (data.keyval,False)
				self.move[i]+= 1

	def _move_callback( self ) :
		self.scene.key_pressed( self.move )
		self.drawing_area.queue_draw()
		return any(self.move)

	def _refresh( self ) :            
		self.drawing_area.queue_draw()
		return True    

	def _after_draw( self , widget , data=None ) :
		self.update_statusbar()

	def update_statusbar( self ) :
		pass

	def _on_reshape( self , widget , data=None ) :
		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height

		ratio = float(width)/float(height)

		self.scene.set_screen_size( width , height )
		self.scene.set_ratio( ratio )

	def _on_button_pressed( self , widget , data=None ) :
		if data.button == 3 :
			self.mouse_pos = data.x , data.y
		self.drawing_area.queue_draw()

	def _on_mouse_motion( self , widget , data=None ) :
		diff = map( op.sub , self.mouse_pos , (data.x , data.y) )
			  
		self.scene.mouse_move( diff )
			  
		self.mouse_pos = data.x , data.y
		self.drawing_area.queue_draw()

	def init_glext(self):
		# Query the OpenGL extension version.
#        print "OpenGL extension version - %d.%d\n" % gtk.gdkgl.query_version()

		# Configure OpenGL framebuffer.
		# Try to get a double-buffered framebuffer configuration,
		# if not successful then try to get a single-buffered one.
		display_mode = (gtk.gdkgl.MODE_RGB    |
				gtk.gdkgl.MODE_DEPTH  |
				gtk.gdkgl.MODE_DOUBLE)
		try:
			glconfig = gtk.gdkgl.Config(mode=display_mode)
		except gtk.gdkgl.NoMatches:
			display_mode &= ~gtk.gdkgl.MODE_DOUBLE
			glconfig = gtk.gdkgl.Config(mode=display_mode)

		return glconfig

	def _load_img( self , filename ) :
		gimg = gtk.image_new_from_file( filename )
		gpb  = gimg.get_pixbuf()
		return Image( gpb.get_width() , gpb.get_height() , gpb.get_pixels() )

	def _load_cube_img( self , filenames ) :
		pbs = [ gtk.image_new_from_file(filename).get_pixbuf() for filename in filenames ]
		w = pbs[0].get_width()
		h = pbs[0].get_height()
		for p in pbs : assert( w == p.get_width () )
		for p in pbs : assert( h == p.get_height() )
		return CubeImage( w , h , [ p.get_pixels() for p in pbs ] )

	def on_win_main_destroy(self,widget,data=None):
		gtk.main_quit()
		 
	def on_but_quit_clicked(self,widget,data=None):
		gtk.main_quit()

if __name__ == '__main__':
	app = App()
	gtk.main()

