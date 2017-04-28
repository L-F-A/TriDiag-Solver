import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes
import os 

class TriDiagSol:
#############################################################################################
#			Thomas algorithm for Tridiagonal matrix see: 			    #
#		  https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm		    #
#											    #
#                       Stable for symmetric positive definite matrices			    #
#       Louis-Francois Arsenault, Columbia Universisty (2013-2017), la2518@columbia.edu     #
#############################################################################################
#                                                                                           #
#       The class constructor enables to load the compiled solver at once, hence why I use  #
#		     a class here, such as loading everything just once  		    #
#                                                                                           #
#	Constructor:									    #
#		Mat_rhs	    :If False, b in Ax=b is a vector. If True, b is a matrix	    #
#											    #
#       FUNCTION solve:                                                                     #
#               ld          : Lower diagonal vector					    #
#               d           : Principal diagonal vector					    #
#		ud	    : Upper diagonal vector					    #
#		b	    : Vector of rhs of the system Ax=b where A tridiagonal matrix   # 
#			      that would be formed with ld, d and ud   			    #
#											    #
#	OUTPUT:										    #
#		x	    : Solution vector (or matrix) of Ax=b			    #
#											    #
############################################################################################# 

	def __init__(self,Mat_rhs=False):

		self.Mat_rhs=Mat_rhs
		dir_path = os.path.dirname(os.path.realpath(__file__))

		if Mat_rhs==False:
			_lib = ctypes.cdll.LoadLibrary(dir_path+"/TriDiagSolver.so")
			_func=_lib.TriDiagSolver
			_func.restype=None
			_func.argtypes=[ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_int]
			self._func=_func
		else:
			_lib = ctypes.cdll.LoadLibrary(dir_path+"/TriDiagSolver_Mat_rhs.so")
                        _func=_lib.TriDiagSolver_Mat_rhs
                        _func.restype=None
			_doublepp = ndpointer(dtype=np.uintp, ndim=1)
			_func.argtypes=[ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),_doublepp,_doublepp,ctypes.c_int,ctypes.c_int]
			self._func=_func
		
	def solve(self,ld,d,ud,b):

		if self.Mat_rhs==False:
			n=len(d)
			x=np.zeros(n)
			#the Upper diagonal ud and rhs vector b are modified during the calculation
			#hence I am passing copies of those such that we keep the original unchanged
			self._func(d,ld,ud.copy(),b.copy(),x,n)
		else:
			n,c=b.shape
			x=np.zeros((n,c))
			xpp=(x.__array_interface__['data'][0] + np.arange(x.shape[0])*x.strides[0]).astype(np.uintp)
			#the Upper diagonal ud and rhs matrix b are modified during the calculation
			#hence I am passing copies of those such that we keep the original unchanged
			b1=b.copy() 
    			bpp=(b1.__array_interface__['data'][0] + np.arange(b1.shape[0])*b1.strides[0]).astype(np.uintp)
			self._func(d,ld,ud.copy(),bpp,xpp,n,c)
		return x
