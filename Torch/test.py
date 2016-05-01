import numpy as np

n = 4
B = np.zeros([n,n])
C = np.zeros([n,n])
A = np.array(range(1,n+1))

for ii in range(n):
    for jj in range(ii+1,n):
        sum = 0
        for kk in range(ii,jj+1):
            print ii,kk,jj
            sum += A[kk]
        B[ii,jj] = sum
print A
print B
print B[1,2],1,2

C[0,1] = A[0]+A[1]
for ii in range(2,n):
    C[0,ii] = C[0,ii-1] + A[ii]
for ii in range(1,n):
    for jj in range(ii+1,n):
        C[ii,jj] = C[ii-1,jj] - A[ii-1]
print C
