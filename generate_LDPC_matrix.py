# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:53:27 2018

#generate LDPC matrix for WIMAX 802.16e

@author: renbi
"""
import numpy as np
# Prepare matrix
baseMatrix = np.array([[-1,94,73,-1,-1,-1,-1,-1,55,83,-1,-1,7,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                        [-1,27,-1,-1,-1,22,79,9,-1,-1,-1,12,-1,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                        [-1,-1,-1,24,22,81,-1,33,-1,-1,-1,0,-1,-1,0,0,-1,-1,-1,-1,-1,-1,-1,-1],
                        [61,-1,47,-1,-1,-1,-1,-1,65,25,-1,-1,-1,-1,-1,0,0,-1,-1,-1,-1,-1,-1,-1],
                        [-1,-1,39,-1,-1,-1,84,-1,-1,41,72,-1,-1,-1,-1,-1,0,0,-1,-1,-1,-1,-1,-1],
                        [-1,-1,-1,-1,46,40,-1,82,-1,-1,-1,79,0,-1,-1,-1,-1,0,0,-1,-1,-1,-1,-1],
                        [-1,-1,95,53,-1,-1,-1,-1,-1,14,18,-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1,-1,-1],
                        [-1,11,73,-1,-1,-1,2,-1,-1,47,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1,-1],
                        [12,-1,-1,-1,83,24,-1,43,-1,-1,-1,51,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1],
                        [-1,-1,-1,-1,-1,94,-1,59,-1,-1,70,72,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1],
                        [-1,-1,7,65,-1,-1,-1,-1,39,49,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0],
                        [43,-1,-1,-1,-1,66,-1,41,-1,-1,-1,26,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0]])

rows = 12
cols = 24
z = 24;
# Divide to submatrix A, B, C, D, E, T
A_Base = np.zeros((11,12),dtype=int)
B_Base = np.zeros((11,1),dtype=int)
T_Base = np.zeros((11,11),dtype=int)
for i in range(rows-1):
    A_Base[i] = baseMatrix[i][0:rows]
    B_Base[i] = baseMatrix[i][rows:rows+1]
    T_Base[i] = baseMatrix[i][rows+1:cols]
    
C_Base = baseMatrix[rows-1][0:rows].reshape(1,rows)
D_Base = baseMatrix[rows-1][rows:rows+1].reshape(1,1)
E_Base = baseMatrix[rows-1][rows+1:cols].reshape(1,rows-1)

def gen_sub_mat(val1, z):
    
    
    if(val1 == -1):
        return np.zeros((z,z), dtype=int)
    else:
        val = int(val1 * z / 96)
        sub_mat = np.eye(z,dtype=int)
        rest = val % z
        
        tmp = sub_mat[0:rest]
        return np.vstack((sub_mat[rest:z], tmp))
# Generate whole matrix
def gen_whole_mat(Mat_Base, z):
    rows, cols = Mat_Base.shape
    
    for i in range(0, rows):
        for j in range(0,cols):
            if j == 0:
                tmp = gen_sub_mat(Mat_Base[i][j], z)
            else:
                tmp = np.hstack((tmp, gen_sub_mat(Mat_Base[i][j], z)))
        if i == 0:
            temp = tmp
        else:
            temp = np.vstack((temp, tmp))
    return temp
# Whole Matrix of A, B, C, D, E, T
A_Whole = gen_whole_mat(A_Base, 24)
B_Whole = gen_whole_mat(B_Base, 24)
C_Whole = gen_whole_mat(C_Base, 24)
D_Whole = gen_whole_mat(D_Base, 24)
E_Whole = gen_whole_mat(E_Base, 24)
T_Whole = gen_whole_mat(T_Base, 24)

# T inverse and E*(T inverse)
TT_Whole = np.mat(T_Whole, dtype=int).I.astype(int)
ETT_Whole = np.dot(E_Whole, TT_Whole)

# Encoding
len = 12 * z

data_placeholder = np.zeros(len,dtype=int).reshape(1,len)

for i in range(0,len):
    data_placeholder[0][i] = np.random.randint(0,2)

data = np.mat(data_placeholder)
# Algorithm steps
f1 = np.dot(A_Whole, data.T) % 2
f2 = np.dot(C_Whole, data.T) % 2
f3 = np.dot(ETT_Whole, f1) % 2
p1 = f3 + f2

f4 = np.dot(B_Whole, p1) % 2
f5 = f1 + f4
p2 = np.dot(TT_Whole, f5) % 2
# Codeword
codeword = np.hstack((data, p1.T, p2.T))








