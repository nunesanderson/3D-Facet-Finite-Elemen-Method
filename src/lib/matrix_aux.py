import scipy
import numpy as np

def delete_sparse_mask(csr_matrix,index_list,dim):
	mask = np.ones(csr_matrix.shape[dim], dtype=bool)
	mask[index_list] = False

	ans=0
	if dim==1:
		ans=csr_matrix[:,mask]
	elif dim==0:
		ans=csr_matrix[mask]

	return ans

def invert_w(w):
	for count in range(0,len(w)):
		w[count,0]=-w[count,0]
	return w

def dot_product(mat1,mat2):
	return np.dot(mat1.T,mat2)[0][0]