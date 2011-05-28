cimport numpy as np
 
import cython
 
import random as rnd
import math as m
 
import numpy as np
 
cdef float d( int i , int j ) :
	return 0.95 * min( 1 , min(i,j)/0.05 ) 

@cython.boundscheck(False)
@cython.cdivision(True)
def step( np.ndarray[ float , ndim=2 ] win not None , np.ndarray[ float , ndim=2 ] wout not None ,
		int n , float h , float c , float dt ) :
	cdef float zij 
	cdef float zoij
	cdef float zipj
	cdef float zimj
	cdef float zijp
	cdef float zijm

	cdef float A = (c*c*dt*dt)/(h*h)
	cdef float B = 2.0 - 4.0*A

	cdef int i
	cdef int j

	if A >= .5 :
			print '>>>>>>>>>'
			print n , h , c , dt
			print A
			print B
			print '>>>>>>>>>'

	for i in range(n) :
		for j in range(n) :
			zij  = win [i  ,j  ]
			zoij = wout[i  ,j  ]
			zipj = win [i+1,j  ] if i+1 <  n else zij
			zimj = win [i-1,j  ] if i-1 >= 0 else zij
			zijp = win [i  ,j+1] if j+1 <  n else zij
			zijm = win [i  ,j-1] if j-1 >= 0 else zij

			wout[i,j] = d(i,j)*(A*(zipj+zimj+zijp+zijm)+B*zij-zoij)

			if wout[i,j] > 10.0 or wout[i,j] < -10.0 :
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
					print wout[i][j]
					print '<<<<<<<<<<<<'
	return None

@cython.boundscheck(False)
def to_normals( np.ndarray[ float , ndim=2 ] mem , np.ndarray[ float , ndim=3 ] norm ,
				int n ) :
	''' Converts height map to normal map by calculating divided differences

		Normal in P is calculating depend on neighbours:
		X  - N1 - X
		|    |    |
		N2 - P  - N3
		|    |    |
		X  - N4 - X
	'''
	cdef int i , j
	cdef float p , n1 , n2 , n3 , n4
	cdef np.ndarray[ float , ndim=1 ] an1 = np.zeros(3,np.float32)
	cdef np.ndarray[ float , ndim=1 ] an2 = np.zeros(3,np.float32)
	cdef np.ndarray[ float , ndim=1 ] an3 = np.zeros(3,np.float32)
	cdef np.ndarray[ float , ndim=1 ] an4 = np.zeros(3,np.float32)

	for i in range(n) :
		for j in range(n) :
			p  = mem[i  ,j  ]
			n1 = mem[i  ,j+1] if j+1 <  n else p
			n2 = mem[i-1,j  ] if i-1 >= 0 else p
			n3 = mem[i+1,j  ] if i+1 <  n else p
			n4 = mem[i  ,j-1] if j-1 >= 0 else p

			an1[0] = i
			an1[1] = n1
			an1[2] = j+1

			an2[0] = i-1
			an2[1] = n2
			an2[2] = j

			an3[0] = i+1
			an3[1] = n3
			an3[2] = j

			an4[0] = i
			an4[1] = n3
			an4[2] = j-1

			an1[0] = an1[0] - an4[0]
			an1[1] = an1[1] - an4[1]
			an1[2] = an1[2] - an4[2]
			an3[0] = an3[0] - an2[0]
			an3[1] = an3[1] - an2[1]
			an3[2] = an3[2] - an2[2]

			norm[i,j,0] = ((an3[1] * an1[2]) - (an3[2] * an1[1]))
			norm[i,j,1] = ((an3[2] * an1[0]) - (an3[0] * an1[2]))
			norm[i,j,2] = ((an3[0] * an1[1]) - (an3[1] * an1[0]))

	return None

