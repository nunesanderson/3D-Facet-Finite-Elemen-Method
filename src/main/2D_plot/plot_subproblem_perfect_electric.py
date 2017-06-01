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

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\35_Subdomain_Dular_2009_electric\GetDP_3D\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
y_FEM=(data[:,4])
z_FEM=(data[:,5])


#===================================================
# FEM - Completo
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\35_Subdomain_Dular_2009_electric\GetDP_3D\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
B_FEM_x=data[:,12]
B_FEM_y=data[:,13]
B_FEM_z=data[:,14]
B_list=list()

##===================================================
## FFEM SS + BS correction
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\35_Subdomain_Dular_2009_electric\FFEM_Complete\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_comp_x=(data[:,0])
B_comp_y=(data[:,1])
B_comp_z=(data[:,2])


##===================================================
## BS
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\35_Subdomain_Dular_2009_electric\FFEM_Complete\results\line_field_BS.txt"
data = np.genfromtxt(data,delimiter=' ')
B_BS_x=list()
B_BS_y=list()
B_BS_z=list()

for counter in xrange(len(x_FEM)):
	if x_FEM[counter]>=0.015 and x_FEM[counter]<=0.035:
		B_BS_x.append(0)
		B_BS_y.append(0)
		B_BS_z.append(0)
	else:
		B_BS_x.append(data[counter,0]*mu0)
		B_BS_y.append(data[counter,1]*mu0)
		B_BS_z.append(data[counter,2]*mu0)


#=========================
#Plots
plt.figure(1)
plt.plot(x_FEM, B_FEM_y,label='FEM',color="black",lw=3,linestyle='-',alpha=0.5)

#plt.plot((x_FEM), B_VS_y,label='$\mathbf{B}_2$',color="blue",linestyle='--',lw=4,alpha=0.5)
plt.plot((x_FEM), B_BS_y,label='$B_p$: BS',color="blue",linestyle='-',lw=3,alpha=0.5)
#plt.plot(x_FEM, B_comp_y,label='$B_q$',color="red",lw=1,linestyle='-')
plt.plot((x_FEM), B_comp_y+B_BS_y,label='$B_p+B_q$',color="black",linestyle='--',lw=3,alpha=1)
#plt.plot((x_FEM), B_VS_corry+B_BS_y,label='$\mathbf{B}_1+\mathbf{B}_2\,corrected$',color="red",linestyle='-.',lw=4,alpha=1)


plt.xlabel('Position along the device [m]',**axis_font)
plt.ylabel('By [T]',**axis_font)
legend = plt.legend(fontsize='24',loc=3)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.xlim(xmax=0.15)
plt.tick_params(axis='x', labelsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.tight_layout()
plt.grid(True)
