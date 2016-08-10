clear_all()
import numpy as np
from scipy.sparse import csr_matrix
import scipy
row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 2])
data = np.array([1, 2, 3, 4, 5, 6])

a=csr_matrix((data, (row, col)), shape=(3, 3))
b=csr_matrix((data, (row, col)), shape=(3, 3))
b[0,0]+=1

#print b.toarray()

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

np.save("teste.txt",b)
save_sparse_csr("teste.txt",b)
del a
del b
new_b=load_sparse_csr("teste.txt.npz").toarray()
#new_b_2=np.load("teste.txt.npy")[0,0]

c=csr_matrix((data, (row, col)), shape=(3, 3))
print c.toarray()


def delete_row_sparse(csr_matrix,index_list,dim):
	mask = np.ones(csr_matrix.shape[0], dtype=bool)
	mask[index_list] = False
	
	ans=0
	if dim==1:
		ans=csr_matrix[:,mask].toarray()
	elif dim==0:
		ans=csr_matrix[mask].toarray()
	
	return ans

print delete_row_sparse(c,[0,1],1)

a=csr_matrix((data, (row, col)), shape=(3, 3))

col = np.array([0, 0, 0, 0, 0, 0])
b=csr_matrix((data, (row, col)), shape=(3, 1))
print b.toarray()

c=np.ones((3,3))
a*c