# -*- coding: utf-8 -*-
clear_all()
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import csr_matrix
import scipy.sparse.linalg as splinalg
import scipy
from lib.read_write_TXT_files import read_numeric_file_sparse_csr,write_numeric_file_sparse_csr
import time


Zb=read_numeric_file_sparse_csr("Zb.npz")


Zb=Zb.toarray()
start=time.time()
Zb=csr_matrix(Zb)
dt=time.time()-start
print(dt)

#start=time.time()
#teste= splinalg.inv(Zb)
#dt=time.time()-start
#print(dt)

print "ok"