clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt
import math

plt.rc('font',family='Times New Roman')
plt.close("all")
axis_font = { 'size':'28'}
#savepath=r"C:\Anderson\Pessoal\01_Doutorado\08_Relatorios_Papers\4_CEFC_2016\Four_pages\Figures"

#===================================================
#coordinates
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\40_3D_Winding\algo\results\line_coordinates.txt"
data = np.genfromtxt(data,delimiter=' ')
coordinates_x=data[:,0]
coordinates_y=data[:,1]
coordinates_z=data[:,2]


#===================================================
#normal
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\40_3D_Winding\normal\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_normal_x=data[:,0]
B_normal_y=data[:,1]
B_normal_z=data[:,2]


#===================================================
#algo
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\40_3D_Winding\algo\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_algo_x=data[:,0]
B_algo_y=data[:,1]
B_algo_z=data[:,2]


#===================================================
#PLots
plt.figure(1)
plt.plot(coordinates_z, B_normal_z,label='Normal',color="black",lw=3,linestyle='-',alpha=0.5)
plt.plot(coordinates_z, B_algo_z,label='Algo',color="black",linestyle='-.',lw=3)
plt.xlabel('Position along the gap [mm]',**axis_font)
plt.ylabel('By [T]',**axis_font)
legend = plt.legend(fontsize='20',loc='center right')
frame = legend.get_frame()
frame.set_facecolor('0.90')
#plt.xlim(xmax=0.14)
plt.tick_params(axis='x', labelsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.tight_layout()
plt.grid(True)
#plt.savefig(savepath+"\linha_gap_3D_B.pdf", bbox_inches='tight')


#plt.figure(2)
#plt.plot(x, error_completo,label='MEFF - Completo',color="black")
##plt.plot(x, error_reduzido,label='MEFF + MRR',color="black",linestyle='--',lw=3)
#plt.xlabel('Distância [mm]',**axis_font)
#plt.ylabel('Dif. [%]',**axis_font)
#legend = plt.legend(fontsize='20',loc='center right')
#frame = legend.get_frame()
#frame.set_facecolor('0.90')
#plt.tick_params(axis='x', labelsize=20)
#plt.tick_params(axis='y', labelsize=20)
#plt.tight_layout()
#
#plt.grid(True)

#plt.savefig(savepath+"\supe_H_"+mesh_type+"_y.pdf", bbox_inches='tight')
