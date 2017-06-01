clear_all()

import numpy as np
import os

path=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes\40_3D_Winding\results'

faces_rel_spare_algo=np.load(os.path.join(path,"faces_rel_spare_algo.npy"))
fmm_sparse_algo=np.load(os.path.join(path,"fmm_sparse_algo.npy"))
incidence_matrix_sparse_algo=np.load(os.path.join(path,"incidence_matrix_algo.npy"))



faces_rel_spare_normal=np.load(os.path.join(path,"faces_rel_spare_normal.npy"))
fmm_sparse_normal=np.load(os.path.join(path,"fmm_sparse_normal.npy"))
incidence_matrix_sparse_normal=np.load(os.path.join(path,"incidence_matrix_sparse_normal.npy"))