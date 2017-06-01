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
axis_font = { 'size':'24'}
#savepath=r"C:\Anderson\Pessoal\01_Doutorado\08_Relatorios_Papers\4_CEFC_2016\Four_pages\Figures"

#==============================================================================
# Coordinates
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\GetDP_3D_completo\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
coord_x=(data[:,3])*1000
coord_y=(data[:,4])
coord_z=(data[:,5])

#==============================================================================
# FEM - Completo
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\GetDP_3D_completo\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
FEM_completo_Bx=data[:,12]
FEM_completo_By=data[:,13]
FEM_completo_Bz=data[:,14]

#==============================================================================
# FFEM completo
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FEMM_3D_completo\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
FFEM_completo_Bx=(data[:,0])
FFEM_completo_Bz=(data[:,2])

#==============================================================================
# VS
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FEMM_3D_VS\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
VS_Bx=(data[:,0])
VS_Bz=(data[:,2])


#==============================================================================
# VS-Coupled
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FEMM_3D_VS_coupled\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
VS_coupled_Bx=(data[:,0])
VS_coupled_Bz=(data[:,2])

#==============================================================================
# BS
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FEMM_3D_VS\results\line_field_BS.txt"
data = np.genfromtxt(data,delimiter=' ')
BS_Bx=data[:,0]*mu0
BS_Bz=data[:,2]*mu0


#==============================================================================
# FFEM - Coupled
#==============================================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\FFEM_3D_Acopla\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
FFEM_coupled_Bx=data[:,0]
FFEM_coupled_By=data[:1]
FFEM_coupled_Bz=data[:,2]

#Plots

plt.figure(1)
#plt.plot(coord_x, FEM_completo_Bz,label='FEM',color="red",lw=3,linestyle='-')
plt.plot(coord_x, FFEM_completo_Bz,label=r'FFEM - Ref.',color="black",lw=3,linestyle='-',alpha=0.5)
plt.plot(coord_x, BS_Bz*15,label=r'$B_p:BS \times 15$',color="blue",lw=3,linestyle='-',alpha=0.5)
plt.plot(coord_x, VS_Bz,label=r'$B_q$',color="red",lw=1,linestyle='-')
plt.plot(coord_x, VS_Bz+BS_Bz,label=r'$B_p+B_q$',color="black",lw=3,linestyle='--')

#plt.plot(coord_x, FFEM_completo_Bz,label=r'FFEM - Ref.',color="black",lw=3,linestyle='-',alpha=0.5)
#plt.plot(coord_x, BS_Bz*15,label=r'$B_1 \times 15$',color="blue",lw=3,linestyle='-',alpha=0.5)
#plt.plot(coord_x, VS_coupled_Bz,label=r'$B_2 - Coupled$',color="red",lw=1,linestyle='-')
#plt.plot(coord_x, BS_Bz+VS_coupled_Bz,label=r'$B_1+B_2$',color="black",lw=3,linestyle='--')

#plt.plot(coord_x, FFEM_coupled_Bz,label=r'FFEM coupled - Ref.',color="black",lw=3,linestyle='-',alpha=0.5)
#plt.plot(coord_x, BS_Bz+VS_coupled_Bz,label=r'$B_p+B_q$ coupled',color="black",lw=3,linestyle='--')

plt.xlabel('Position along the probe line [mm]',**axis_font)
plt.ylabel('Bz [T]',**axis_font)
legend = plt.legend(fontsize='24')
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.xlim(xmin=-60,xmax=60)
#plt.axvline(x=-55, color='red',lw=2,linestyle='--')
#plt.axvline(x=-25, color='red',lw=2,linestyle='--' )
#plt.axvline(x=55, color='red',lw=2,linestyle='--')
#plt.axvline(x=25, color='red',lw=2,linestyle='--' )
#plt.text(40, -0.07, 'Probe line in \n the air gap', fontsize=20,horizontalalignment='center',color="red")
#plt.text(-40, -0.07, 'Probe line in \n the air gap', fontsize=20,horizontalalignment='center',color="red")
plt.tick_params(axis='x', labelsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.tight_layout()
plt.grid(True)


#
##===================================================
## Errors
#error_FFEM_coupled_Bz=list()
#error_x=list()
#for counter in range(0,len(coord_x),1):
#	if coord_x[counter]>-20 and coord_x[counter]<20:
#		error_FFEM_coupled_Bz.append('nan')
#		error_x.append('nan')
#	else:
#
#		error_FFEM_coupled_Bz.append(100*abs((FEM_coupled_Bz[counter]-FFEM_coupled_Bz[counter])/FEM_coupled_Bz[counter]))
#		error_x.append(coord_x[counter])
#
#
#plt.figure(3)
#plt.semilogy(error_x, error_FFEM_coupled_Bz,label='FEM (Fine)',color="black",linestyle='-',lw=3)
#
#
#plt.xlabel('Position along the probe line [mm]',**axis_font)
#plt.ylabel('Rel. dif. [%]',**axis_font)
#legend = plt.legend(fontsize='20')
#plt.axvline(x=-55, color='red',lw=2,linestyle='--')
#plt.axvline(x=-25, color='red',lw=2,linestyle='--' )
#plt.axvline(x=55, color='red',lw=2,linestyle='--')
#plt.axvline(x=25, color='red',lw=2 ,linestyle='--')
#plt.text(40, 1, 'Air gap region', fontsize=20,horizontalalignment='center',color="red")
#plt.text(-40, 1, 'Air gap region', fontsize=20,horizontalalignment='center',color="red")
#plt.tick_params(axis='x', labelsize=20)
#frame = legend.get_frame()
#frame.set_facecolor('0.90')
#plt.xlim(xmin=-60,xmax=60)
#plt.tick_params(axis='x', labelsize=20)
#plt.tick_params(axis='y', labelsize=20)
#plt.tight_layout()
#plt.grid(True)

