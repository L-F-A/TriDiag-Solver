#include <stdio.h>
//		Thomas algorithm for Tridiagonal matrix see: https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
//					Stable for symmetric positive definite matrices


//					To compile as a shared library use the command:

//				     gcc -shared -fPIC TriDiagSolver.c -o TriDiagSolver.so

//				    ****Could probably be optimized in the forward loop****


void TriDiagSolver(double *d,double *ld,double *ud,double *b,double *res,int size_d)
{
	double den;
	double num;

	int i,j;

	int size_ld,size_ud;
	size_ld=size_d-1;
	size_ud=size_ld;

	//Forward
	ud[0]=ud[0]/d[0];
	b[0]=b[0]/d[0];
	for(i=1; i<size_ud; i++)
	{
		den=d[i]-ld[i-1]*ud[i-1];
		num=b[i]-ld[i-1]*b[i-1];
		ud[i]/=den;
		b[i]=num/den;
	}

	den=d[size_d-1]-ld[size_ld-1]*ud[size_ud-1];
        num=b[size_d-1]-ld[size_ld-1]*b[size_d-2];
	b[size_d-1]=num/den;

	//Backward: solution vector res is populated
	res[size_d-1]=b[size_d-1];
	for(j=size_d-2; j>=0 ; j--)
		res[j]=b[j]-ud[j]*res[j+1];
}
