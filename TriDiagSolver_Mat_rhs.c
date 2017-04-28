#include <stdio.h>
#include <stdlib.h>
/*		Thomas algorithm for Tridiagonal matrix see: https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
					Stable for symmetric positive definite matrices
**************************************************************************************************************************
****************************This version is for the case where the right hand side of Ax=b is a matrix********************
**************************************************************************************************************************

					To compile as a shared library use the command:

			      gcc -shared -fPIC TriDiagSolver_Mat_rhs.c -o TriDiagSolver_Mat_rhs.so

				  ****Could probably be optimized a bit in the forward loop****
*/

void TriDiagSolver_Mat_rhs(double *d,double *ld,double *ud,double **b,double **res,int size_d,int col_b)
{
	double den;
	double num;

	int i,j,k,l;

	int size_ld,size_ud;
	size_ld=size_d-1;
	size_ud=size_ld;


	//rhs is a matrix
	double *udd; //ud is modified along the calculation by we need the original for each row of b. Thus we will copy it each time
	udd=(double *) malloc(size_ud*sizeof(double));

	for(k=0; k<col_b; k++)
	{
		for (l=0;l<size_ud;l++)
			udd[l]=ud[l];

		//Forward
                udd[0]=udd[0]/d[0];
                b[0][k]=b[0][k]/d[0];
                for(i=1; i<size_ud; i++)
                {
                        den=d[i]-ld[i-1]*udd[i-1];
                        num=b[i][k]-ld[i-1]*b[i-1][k];
                        udd[i]/=den;
                        b[i][k]=num/den;
                }

                den=d[size_d-1]-ld[size_ld-1]*udd[size_ud-1];
                num=b[size_d-1][k]-ld[size_ld-1]*b[size_d-2][k];
                b[size_d-1][k]=num/den;

                //Backward
                res[size_d-1][k]=b[size_d-1][k];
                for(j=size_d-2; j>=0 ; j--)
			res[j][k]=b[j][k]-udd[j]*res[j+1][k];
	}
	free(udd);

}
