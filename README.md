*****Matrix Calculator*****
This project is written in C++ and needs a C++ compiler.
In this project 2 arguements are needed in order:
A file contains n*n A matrix and another file (n*1) b vector.
It returns a message and quit if A is singular with presicion approximately 1e-14 .
It returns the solution of Ax=b equation if A is not singular.
It also returns the condition numbers at 1 and infinity of A if A is not singular and n==2.

We can run the code
project.exe *The direction of the file that contains A matrix* *The direction of the file that contains b vector*
Example:
project.exe A.txt b.txt

*****The Case of High Condition Numbers*****
A:
1.000 1.000
1.000 1.001
b1:		b2:
2.000		2.000
2.000		2.001
for these matrix and vectors
x1:		x2:
2		1
0		1
and condition number of matrix A at 1 and inf are found
4004
It is strictly greater than 1. Therefore let x be solution of Ax = b and x' be solution to Ax' = b + delta(b)
Delta(x)=x'-x
and
norm(Delta(x))/norm(x) <= cond(A) + norm(Delta(b))/norm(b) from the textbook.
Clearly when condition number is increasing, it becomes much singular. Furthermore, when condition number is rising,
error bound for unknowns increases, which leads to the fact that any small change in b changes x dramatically.

Emre Kucukkaya

