# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:31:11 2018

@author: renbi

"""

import generate_LDPC_matrix as ldpc_
import numpy as np

len = 288

data_placeholder = np.zeros(288,dtype=int).reshape(1,288)

for i in range(0,288):
    data_placeholder[0][i] = np.random.randint(0,2)

data = np.mat(data_placeholder)

f1 = np.dot(ldpc_.A_Whole, data.T) % 2
f2 = np.dot(ldpc_.C_Whole, data.T) % 2
f3 = np.dot(ldpc_.ETT_Whole, f1) % 2
p1 = f3 + f2

f4 = np.dot(ldpc_.B_Whole, p1) % 2
f5 = f1 + f4
p2 = np.dot(ldpc_.TT_Whole, f5) % 2

codeword = np.hstack((data, p1.T, p2.T))