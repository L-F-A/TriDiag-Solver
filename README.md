# TriDiag-Solver
Thomas algorithm for solving tridiagonal matrix linear equation Ax=b where A is tridiagonal.

see: https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm

This algorithm is stable for example for symmetric positive definite matrices (This is the reason I wanted this approach).

The core function is written in C. The python class acts more like a wrapper. To use it, the C code must be compiled, in the same directory both ... and ... are. The compilation line is just:

    gcc -shared -fPIC TriDiagSolver.c -o TriDiagSolver.so

Then evrerything should be ok.

For example:

    n=100
    ld=np.random.rand(n-1)
    d=np.random.rand(n)
    ud=np.random.rand(n-1)
    b=np.random.rand(n)

    #Of course TriDiagSol has been imported already from where it is 
    TD=TriDiagSol()

    xhat=TD.solve(ld,d,ud,b)
    
