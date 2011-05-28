
class Image :
	def __init__( self , w , h , data ) :
		self.width  = w
		self.height = h
		self.data   = data

	@property
	def w( self ) :
		return self.width 

	@property 
	def h( self ) :
		return self.height

class CubeImage :
	def __init__( self , w , h , datas ) :
		self.width  = w
		self.height = h
		self.datas  = datas

