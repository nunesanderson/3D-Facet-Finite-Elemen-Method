clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt
import math

mu0=4*math.pi*pow(10,-7)

plt.rc('font',family='Times New Roman')
plt.close("all")
axis_font = { 'size':'28'}
#savepath=r"C:\Anderson\Pessoal\01_Doutorado\08_Relatorios_Papers\4_CEFC_2016\Four_pages\Figures"

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\GetDP_3D\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
y_FEM=(data[:,4])
z_FEM=(data[:,5])


#===================================================
# FEM - Completo
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\GetDP_3D\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
B_FEM_x=data[:,12]
B_FEM_y=data[:,13]
B_FEM_z=data[:,14]
B_list=list()

##===================================================
## FFEM completo
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FFEM_Complete\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_comp_x=(data[:,0])
B_comp_y=(data[:,1])
B_comp_z=(data[:,2])
#
##===================================================
### VS
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FFEM_VS\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_VS_x=(data[:,0])
B_VS_y=(data[:,1])
B_VS_z=(data[:,2])


###===================================================
### BS
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FFEM_VS\results\line_field_BS.txt"
data = np.genfromtxt(data,delimiter=' ')
B_BS_x=(data[:,0])*mu0
B_BS_y=(data[:,1])*mu0
B_BS_z=(data[:,2])*mu0


###===================================================
### VS + Correction
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FFEM_VS_corrected\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_VS_corr_x=(data[:,0])
B_VS_corry=(data[:,1])
B_VS_corrz=(data[:,2])

#=========================
#Plots
plt.figure(1)
#plt.plot(x_FEM, B_FEM_z,label='FEM',color="black",lw=3,linestyle='-',alpha=0.5)
plt.plot(x_FEM, B_comp_z,label='FFEM - Ref.',color="black",lw=3,linestyle='-',alpha=0.5)
plt.plot((x_FEM), B_BS_z*15,label='$\mathbf{B}_1$x15',color="blue",linestyle='-',lw=3,alpha=0.5)
plt.plot((x_FEM), B_VS_z,label='$\mathbf{B}_2$',color="red",linestyle='-',lw=1)
plt.plot((x_FEM), B_VS_z+B_BS_z,label='$\mathbf{B}_1+\mathbf{B}_2$',color="black",linestyle='--',lw=4,alpha=1)
plt.plot((x_FEM), B_VS_corrz+B_BS_z,label='$\mathbf{B}_1+\mathbf{B}_2\,corrected$',color="red",linestyle='-.',lw=4,alpha=1)


plt.xlabel('Position along the device [m]',**axis_font)
plt.ylabel('Bz [T]',**axis_font)
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

#
