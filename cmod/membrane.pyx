cimport numpy as np
 
import cython
 
import random as rnd
import math as m
 
import numpy as np
 
cdef float d( int i , int j ) :
	return 0.95 * min( 1 , min(i,j)/0.2 ) 

cdef float get( np.ndarray[ float ] t , int x , int y , int n ) :
	return t[x+y*n]

#@cython.boundscheck(False)
cpdef int step( np.ndarray[ float ] win , np.ndarray[ float ] wout ,
		int n , float h , float c , float dt ) :
	cdef float zipj
	cdef float zimj
	cdef float zijp
	cdef float zijm
	cdef float zij 
	cdef float zoij

	cdef float A = (c*c*dt*dt)/(h*h)
	cdef float B = 2.0 - 4.0*A

	if A >= .5 :
			print '>>>>>>>>>'
			print n , h , c , dt
			print A
			print B
			print '>>>>>>>>>'

	for i in range(n) :
		for j in range(n) :
			zij  = get( win  , i   , j   , n )
			zoij = get( wout , i   , j   , n )
			zipj = get( win  , i+1 , j   , n ) if i+1 <  n else zij
			zimj = get( win  , i-1 , j   , n ) if i-1 >= 0 else zij
			zijp = get( win  , i   , j+1 , n ) if j+1 <  n else zij
			zijm = get( win  , i   , j-1 , n ) if j-1 >= 0 else zij

			wout[ i + j*n ] = d(i,j)*(A*(zipj+zimj+zijp+zijm)+B*zij-zoij)

#                        if m.isnan( wout[ i + j*n ] ) or m.isinf(wout[ i + j*n ]) :
			if wout[ i + j*n ] > 1.0 or wout[ i +j*n ] < -1.0 :
					print '<<<<<<<<<<<<'
					print n , h , c , dt
					print A
					print B
					print
					print zipj 
					print zimj 
					print zijp 
					print zijm 
					print zij  
					print zoij 
					print d(i,j)
					print 
					print wout[ i + j*n ]
					print '<<<<<<<<<<<<'


