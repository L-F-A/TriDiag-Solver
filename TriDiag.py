import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes


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
#		     a class here, such as loading everything just once 	            #
#                                                                                           #
#       FUNCTION solve:                                                                     #
#               ld          : Lower diagonal vector					    #
#               d           : Principal diagonal vector					    #
#		ud	    : Upper diagonal vector					    #
#		b	    : Vector of rhs of the system Ax=b where A tridiagonal matrix   # 
#			      that would be formed with ld, d and ud   			    #
#											    #
#	OUTPUT:										    #
#		x	    : Solution vector of Ax=b					    #
#											    #
############################################################################################# 

	def __init__(self):

		_lib = ctypes.cdll.LoadLibrary("./TriDiagSolver.so")
		_func=_lib.TriDiagSolver
		_func.restype=None
		_func.argtypes=[ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_int]
		self._func=_func

	def solve(self,ld,d,ud,b):

		n=len(d)
		x=np.zeros(n)
		#the Upper diagonal ud and rhs vector b are modified during the calculation
		#hence I am passing copies of those such that we keep the original unchanged
		self._func(d,ld,ud.copy(),b.copy(),x,n)
		return x
