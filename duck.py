import sys

import pygtk
pygtk.require('2.0')
import gtk

import operator as op

from OpenGL.GL import *

from glwidget import GLDrawingArea

from scene import Scene

ui_file = "duck.ui"

class App(object):
	"""Application main class"""

	def __init__(self):

		self.near = 1
		self.fov  = 60

		builder = gtk.Builder()
		builder.add_from_file(ui_file)

		glconfig = self.init_glext()

		self.drawing_area = GLDrawingArea(glconfig)
		self.drawing_area.set_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON1_MOTION_MASK)
		self.drawing_area.set_size_request(800, 800)

		builder.get_object("vbox1").pack_start(self.drawing_area)

		builder.get_object("win_main").show_all()

		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height
		ratio = float(width)/float(height)

		self.scene = Scene( self.fov , ratio , self.near )
		self.drawing_area.add( self.scene )

		builder.connect_signals(self)

		self.statbar = builder.get_object('statbar')

		self.drawing_area.connect('motion_notify_event',self._on_mouse_motion)
		self.drawing_area.connect('button_press_event',self._on_button_pressed)
		self.drawing_area.connect('configure_event',self._on_reshape)
		self.drawing_area.connect_after('expose_event',self._after_draw)

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
		if data.button == 1 :
			self.mouse_pos = -data.x , data.y
		self.drawing_area.queue_draw()

	def _on_mouse_motion( self , widget , data=None ) :
		diff = map( op.sub , self.mouse_pos , (-data.x , data.y) )

		self.scene.mouse_move( diff , axis1 , axis2 )

		self.mouse_pos = -data.x , data.y
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

	def on_win_main_destroy(self,widget,data=None):
		gtk.main_quit()
		 
	def on_but_quit_clicked(self,widget,data=None):
		gtk.main_quit()

if __name__ == '__main__':
	app = App()
	gtk.main()

