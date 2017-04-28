# TriDiag-Solver
Thomas algorithm for solving tridiagonal matrix linear equation Ax=b where A is tridiagonal and b can be either a vector or a matrix.

see: https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm

This algorithm is stable for example for symmetric positive definite matrices (This is the reason I wanted this approach).

The core function is written in C. The python class acts more like a wrapper. To use it, the C codes must be compiled in the same directory where TriDiag.py, TriDiagSolver.c and TriDiagSolver_Mat_rhs.c are. The functions that deal with b vector and b matrix are independent for convenience. Both must be compiled. The compilation lines are just:

    gcc -shared -fPIC TriDiagSolver.c -o TriDiagSolver.so
    gcc -shared -fPIC TriDiagSolver_Mat_rhs.c -o TriDiagSolver_Mat_rhs.so
    
Then evrerything should be ok.

The case where b is a matrix is just written as a c file with an extra looping along the columns and solving Thomas algorithm for each and accumulate the results in the matrix x. Perhaps there is a more clever way, need to think about it.

For example:

    n=100
    ld=np.random.rand(n-1)
    d=np.random.rand(n)
    ud=np.random.rand(n-1)
    b=np.random.rand(n)

    #Of course TriDiagSol has been imported already from where it is:
    #--> from blablabla.TriDiag-Solver import TriDiagSol
    TD=TriDiagSol()

    xhat=TD.solve(ld,d,ud,b)
    
