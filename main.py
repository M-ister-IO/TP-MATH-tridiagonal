import numpy as np

# In a n by n matrix we have n^2 cells to stock, in a n by 3 matrix we only have 3n cells to stock so we have n^2-3n cells less

def randomTriDiag(n):
    A=np.random.random(size=(n,n))
    for i in range(n):
        for j in range(n):
            if i-j>1 or j-i>1:
                A[i,j]=0
    print(A)
    return A

def TRIreduite(A):
    n=len(A)
    B=np.zeros((n,3))

    for i in range(n):
        for j in range(n):
            if A[i][j]==0:
                pass
            elif i==j:
                B[i][1]=A[i][j]
            elif i>j:
                B[i][0]=A[i][j]
            elif i<j:
                B[i][2]=A[i][j]

    return B

def TRIcomplete(B):
    n=len(B)
    A=np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            if i==j:
                A[i][j]=B[i][1]
            elif i==j+1:
                A[i][j]=B[i][0]
            elif i==j-1:
                A[i][j]=B[i][2]
            else:
                pass

    return A

def produitTRIvect(B,x):
    n=len(B)
    z=np.zeros((n,1))
    for i in range(n):
        if i==0:
            z[i]+=B[i][1]*x[i]+B[i][2]*x[i+1]
        elif i==n-1:
            z[i]=B[i][0]*x[i-1]+B[i][1]*x[i]
        else:
            for j in range(3):
                z[i]+=B[i][j]*x[j]

    return z

def DecompositionLU(A):
    n=len(A)
    coefs = []


    for p in range(len(A)-1):
        damned=[]

        x = A[p][p]     #this is the coeficient of the diagonal, the one we have to compare every line with

        for i in range(len(A)): #no [p] because it's a square matrix !!!!!!!change it if its not a square matrix!!!!!!!!!!!!!!

            if i in range(0,p+1): #we only take the coeficient of the new line (we pass the already done ones)
                pass
            else:
                c=A[i][p]/x     #this is the coeficient of how many times i have to substract the 'pivot' line to the new line
                damned.append(c)  #store this value


                for j in range(len(A[i])):
                    A[i][j]-=c*A[p][j]      #compute every new coefficient and replace it

        coefs.append(damned)
    U = np.array(A)

    L=np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            if i==j:
                L[i][j]=1
            elif i!=0 and i>j:
                L[i][j]=coefs[j][i-1-j]


    return L,U   #The L matrix is a lower triangular matrix with only the closest(lower) diagonal having values, The matrix U is an upper triangular matrix with the middle diagonal and the closest(upper) one having values
""""
[[ 1.          0.          0.          0.          0.        ]
 [ 1.4873249   1.          0.          0.          0.        ]
 [ 0.         -0.32119203  1.          0.          0.        ]
 [ 0.         -0.          0.0251997   1.          0.        ]
 [ 0.         -0.          0.          0.61679759  1.        ]]
[[ 0.25094614  0.9187219   0.          0.          0.        ]
 [ 0.         -0.47843223  0.43134588  0.          0.        ]
 [ 0.          0.          0.65541333  0.12130508  0.        ]
 [ 0.          0.          0.          0.24991897  0.46514466]
 [ 0.          0.          0.          0.          0.34301855]]
 """
def triLU(B):
    n=len(B)
    M=np.zeros((n,3))
    for k in range(n):
        if k ==0:
            M[k][1]=B[k][1]
            M[k][2]=B[k][2]
        else:
            M[k][0]=B[k][0]/M[k-1][1]
            M[k][1]=B[k][1]-B[k][0]*B[k-1][2]/M[k-1][1]
            M[k][2]=B[k][2]

    return M

def triLUResol(M,b):
    y=np.zeros((len(b),1))
    x = np.zeros((len(b), 1))
    t_start = 0
    t_end = 0
    t_start=time.time()
    for k in range(len(y)):
        if k==0:
            y[k]=b[k]
        else:
            y[k]=b[k]-y[k-1]*M[k][0]


    for j in range(len(y)-1,-1,-1):
        if j==len(y)-1:
            x[j]=y[j]/M[j][1]
        else:
            x[j]=(y[j]-M[j][2]*x[j+1])/M[j][1]
    t_end=time.time()
    return x,t_start,t_end


def triResol(B,b):


    x,t_start,t_end= triLUResol(triLU(B),b)
    return x,t_start,t_end


#n=5
import time


#x=np.random.random(size=(n,1))
#b=np.random.random(size=(n,1))
#print(b)
#print("########################################")
#print(triLUResol(triLU(TRIreduite(randomTriDiag(n))),b))


n=[100,1000,2000,5000,10000]
t_start = []
t_end = []
for i in range(5):
    b = np.random.random(size=(n[i], 1))

    sol,start,end=triResol(TRIreduite(randomTriDiag(n[i])),b)
    t_start.append(start)
    t_end.append(end)



times=[]
for i in range(len(t_start)):
    times.append(t_end[i]-t_start[i])
print(times)

import matplotlib.pyplot as plt
plt.plot(n,times)
plt.show()

