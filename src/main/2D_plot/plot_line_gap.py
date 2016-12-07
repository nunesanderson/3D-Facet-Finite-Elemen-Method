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
savepath=r"C:\Anderson\Pessoal\01_Doutorado\08_Relatorios_Papers\4_CEFC_2016\Four_pages\Figures"



#===================================================
#FEM
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\25_Rele_3D\Line_results_01_02_03\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=abs(data[:,3])*1000

B_FEM_x=data[:,12]
B_FEM_y=data[:,13]
B_FEM_z=data[:,14]
B_list=list()

#
###===================================================
###completo
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\25_Rele_3D\Line_results_01_02_03\complete.txt"
data = np.genfromtxt(data,delimiter=' ')

B_comp_y=data[:,1]
B_comp_z=data[:,2]

#===================================================
#Reduzido
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\25_Rele_3D\Line_results_01_02_03\reduced.txt"
data = np.genfromtxt(data,delimiter=' ')


B_red_y=data[:,1]
B_red_z=data[:,2]
#B_reduzido=list()
#
#for k in xrange(npoints):
#	B_reduzido.append(math.sqrt(pow(B_FEM_x[k],2)+pow(B_FEM_y[k],2)+pow(B_FEM_z[k],2)))
#
#
##===================================================
##Reduzido fonte
#data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\25_Rele_3D\05_FFFM_reduced_Source\results\field_data.txt"
#data = np.genfromtxt(data,delimiter=' ')
#
#B_FEM_x=data[:,0]
#B_FEM_y=data[:,1]
#B_FEM_z=data[:,2]
#B_reduzido_fonte=list()
#
#for k in xrange(npoints):
#	B_reduzido_fonte.append(math.sqrt(pow(B_FEM_x[k],2)+pow(B_FEM_y[k],2)+pow(B_FEM_z[k],2)))

#===================================================
#Error
#error_completo=100*abs(B_copleto-B_list)/B_list
#error_reduzido=100*abs(B_reduzido-B_list)/B_list



#===================================================
#PLots
plt.figure(1)
plt.plot(x_FEM, B_FEM_y,label='FEM',color="black",lw=3,linestyle='-',alpha=0.5)
plt.plot(x_FEM, B_comp_y,label='FFEM (complete)',color="black",linestyle='-.',lw=3)
plt.plot(x_FEM, B_red_y,label='FFEM + RNM',color="black",linestyle='--',lw=3)
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
plt.savefig(savepath+"\linha_gap_3D_B.pdf", bbox_inches='tight')


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
