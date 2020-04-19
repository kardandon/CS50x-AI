
#include <bits/stdc++.h>													// that includes all algorithms and functions i need

using namespace std;														// using std namespace

void print_matrix(double** A,int n,int m){									//
	for(int i=0;i<n;i++){													// Print function for n*m matrix A in double** format
		for(int j=0;j<m;j++){												//
			cout << A[i][j]<< " ";											//
		}cout<<endl;
	}
}

void delete_2d_array(double** A,int n){										// Delete function of n*x matrix allocation of A in 
	for (int i=0;i<n;i++)delete[] A[i];										// double** format
	delete[] A;																//
}																			//
																			// Machine Precision check
bool is_almost_zero(double x){												// checking if 0+Epsilon>x>0-Epsilon
	if (abs(x)<numeric_limits<double>::epsilon()*100)return true;			// Epsilon is equal to 2.22e-016*100 (using double)
	else return false;														//
}

bool gaussian_elimination_and_back_substitution(int n,double** A_real,double** b){		
// This is the Function that useses Gaussian elimination with pivoting
// and back substitution to solve the equation Ax=b
//
// To get solution for Ax=b:
//
// We need A matrix(n*n) and b matrix (n*1) in double** form and integer n
//
// The function changes only b vector.
// if the matrix A is singular, then the function returns false
// else it returns true and b will be the x in the correct order.
// 
//
	double** A = new double*[n];											// Declaration of temporary A matrix
																			// and make it equal to A_real matrix
	for(int i=0;i<n;i++){													// I declared it because I do not want to lose A_real
		A[i]=new double[n];													// after that function this is deleted
		for(int j=0;j<n;j++){												//
			A[i][j]=A_real[i][j];											//
		}																	//
	}																		//
	double max;int q;														// I will use them for some calculations
																			//
	for(int i=0;i<n;i++){													// For loop for row number
																			//
		max=abs(A[i][i]);q=i;												// Finding the max absolute value in that column (max)
		for(int j=i+1;j<n;j++){												// and also finding its index (q)
			if(abs(A[j][i])>max){											//
				max=abs(A[j][i]);											//
				q=j;												 		//
			}																//
		}																	//
		if(is_almost_zero(max)){											// There is no proper row to exchange so it lacks at least 1 pivot.
			delete_2d_array(A,n);											// (deleting the temporary 2d array)
			return false;													// Thus, it is singular. Returns false and exits.
		}																	//
		else if(q!=i){														// In order to use partial pivoting i need to row exchange two rows
			swap(A[q],A[i]);												// which is the ith row and the row that includes absolute maximum
			swap(b[q],b[i]);												// of that column (q)
		}																	//
		for(int j=i+1;j<n;j++){												// In that loop, row elemination constant = A[j][i]/A[i][i].
			b[j][0]-=b[i][0]*A[j][i]/A[i][i];								// Row elimination of b vector (Row j - Row i *A[j][i]/A[i][i])
																			// That makes all values remaining in that column 0 so we get the upper
			for(int k=i+1;k<n;k++){											// triangular matrix.
																			//
				A[j][k]-=A[i][k]*A[j][i]/A[i][i];	
																			// 
			}
			A[j][i]=0;														// Finally it will be zero (A[j][i]- A[i][i] *A[j][i]/A[i][i] == 0)
		}																	// 
	}																		// Now we get either the upper triangular matrix or returned false
	for(int i=n-1;i>-1;i--){												//
		for(int j=n-1;j>i;j--){												// It is the back substitution part. I start from x_n then go x_1 
			b[i][0]-=b[j][0]*A[i][j];										// Furthermore, I saved x_n to b[n-1] and to do back-substitution
		}																	// I subtracted all x_(i+1)*A[i][i+1] ,x_(i+2)*A[i][i+2] ... from b[i]
		b[i][0]=b[i][0]/A[i][i];											// to find x_i * A[i][i] then after division it gives me x_i 
	}																		// then i saved x_i to b[i-1] as i mentioned before
	delete_2d_array(A,n);													//
	return true;															//  After all the process works perfect it returned true
}																			//  Which means the matrix A is not a singular matrix
																			//
																			//
																			//
																			//
																			//
																			//
double max_abs_column_sum(double** A){										//  A function returns maximum absolute column sum of a (2*2) matrix A
	return max(abs(A[0][0])+abs(A[1][0]),abs(A[0][1])+abs(A[1][1]));		//  in double** form
}																			//
																			//
																			//
																			//
double max_abs_row_sum(double** A){											//  A function returns maximum absolute row sum of a (2*2) matrix A
	return max(abs(A[0][0])+abs(A[0][1]),abs(A[1][0])+abs(A[1][1]));		//  in double** form
}																			//
																			//
																			//
																			//
int main(int argc,char* argv[]){											//
// That is the main function, i need 2 arguements to run all these processes
// They are the files of A matrix and b matrix in order 
// Then i open the files using ifstream to read matricies and apply gaussian elimination with pivoting and back-substitution method
// in order to get solution for Ax=b equation 
// After that, i print out x to console, and also, i print it to output.txt file (using ofstream) if the
// matrix A is not singular. If not, it returns "The matrix is singular." message and it closes.
// 
// If the matrix A is 2*2 matrix, it also finds the condition numbers at 1 and infinity.
// Then it prints it to the console.
//
	double** A;double** b;double** A_real;									// Defining matrix A,b,and A_real dynamically.
	cout<< fixed << setprecision(5);										// Setting precision 5 after decimal point
																			// I used A_real just for 2*2 matricies in order to get
																			// conditions number.
	ifstream fileA;ifstream fileb;ofstream fileout;							// Defining the filestreams i use
	string line;															// Defining a string variable to use in getline.
	int n=0;																// Defining an integer n for the size of matricies
	fileA.open(argv[1]);													// Opening file for A matrix by using first arguement taken
	fileb.open(argv[2]);													// Opening file for b vector by using second arguement taken
	if((fileA.is_open()==0 || fileb.is_open()==0)){							// Checking if the files are open
		cout << "Couldn't open files."<<endl;								// if not print that message and exit.
	}																		//
	else{
		double x;															// if files are opened correctly, i need to get the n number
		while( fileb >> x){													// Thus i decided to count the numbers in b vector
		n++;																//
		}																	// 
		fileb.close();fileb.open(argv[2]);									// After counting that, i need to reopen the file for b vector
		A = new double*[n];													// Defining the rows of matricies dynamically
		b = new double*[n];													//
		if(n==2)A_real =new double*[2];										// If n is equal to 2, i use A_real matrix which i mentioned before
		for (int i=0;i<n;i++){												//
			A[i]=new double[n];												// Defining the columns dynamically
			b[i]=new double[1];												//
			if(n==2)A_real[i] =new double[2];								//
			fileb>> b[i][0];												// Reading b and A from filestreams
			for(int j=0;j<n;j++){											// (Also A_real if n is equal to 2)
				fileA>> A[i][j];											//
				if(n==2)A_real[i][j]=A[i][j];								//
			}																//
		}																	//
		fileA.close();fileb.close();										// Closing files
																			// Now that is the part	that we use the gaussian function												
																			// I use if statement for checking if the matrix A is singular
																			// if it is, it returns false, so i used !(not) operator to make it true
		if(!gaussian_elimination_and_back_substitution(n,A,b)	){			// and make it print that message									
			cout<< "The Matrix A is Singular!"<<endl;						//
			if (n==2)cout << "The condition numbers are inf by convention";	// if it is singular its condition number is inf
		} 																	//
		else{																// If it is not singular then we got x's.
			cout << "***** The x's *****\n";								// Then I printed x's in the correct order
			print_matrix(b,n,1);											// (I printed b because i changed b with the x vector)
			fileout.open("output.txt");										// Then I opened the output file and write the x vector in it
			for(int i=0;i<n;i++){											//
				fileout<< fixed <<setprecision(5);							// Setting precision 5 after decimal point
				fileout<<b[i][0]<<endl;										//
			}																
			fileout.close();												// Closing output file
																			// *** The condition number part ***
			if(n==2){														// If n is equal to 2, we are asked to find the condition numbers at 1 and 
				cout <<"***** Condition Numbers *****"<<endl;				// infinity.
				double** A_inverse = new double*[2];						// Then A_inverse is declared. I used classic determinant formula
				double determinant= A[0][0]*A[1][1]-A[0][1]*A[1][0];		// for 2*2 matricies and found its inverse
				A_inverse[0] = new double[2];								//
				A_inverse[1] = new double[2];								// After that condition number of A at 1 means that the product of 
				A_inverse[0][0] = A[1][1]/determinant;						// maximum absolute column sum A and A_inverse
				A_inverse[0][1] = -A[0][1]/determinant;						//
				A_inverse[1][0] = -A[1][0]/determinant;						// Condition number of A at 1 means that the product of 
				A_inverse[1][1] = A[0][0]/determinant;						// maximum absolute row sum A and A_inverse
				cout << "Condition number of A at 1 = " << max_abs_column_sum(A_inverse) * max_abs_column_sum(A) << endl;		//
				cout << "Condition number of A at inf = " << max_abs_row_sum(A_inverse) * max_abs_row_sum(A);					//
				delete_2d_array(A_inverse,n);								// deleting the inverse matrix
																			//
			}																//
																			//
																			//
		}																	//
																			//
																			//
	}																		//
																			//
	delete_2d_array(A,n);													// Then I deleted all matricies i have allocated
	delete_2d_array(b,n);													//								
	return 0;																// After that, the function returns 0 .
}
