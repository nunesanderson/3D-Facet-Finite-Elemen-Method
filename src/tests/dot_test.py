clear_all()
import numpy as np
from lib.RNM_aux import  AuxMethodsRNM
import time

aux=AuxMethodsRNM()

a=np.array([[4],[4],[4]])

n=1000000
print a

t=time.time()
for k in xrange(n):
	aux.dot_product(a,a)
print time.time()-t


t=time.time()
for k in xrange(n):
	np.dot(a.T,a)[0][0]
print time.time()-t