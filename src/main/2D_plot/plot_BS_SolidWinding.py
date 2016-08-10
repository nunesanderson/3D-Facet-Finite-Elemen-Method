clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font',family='Times New Roman')
axis_font = { 'size':'20'}
plt.close("all")
savepath=r"C:\Anderson\Pessoal\01_Doutorado\5_Figuras_Inkscape\Tese"
mesh_type="grossa"
#===================================================
#Line along Z
#===================================================

#===================================================
#Analitycal
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\results\analyt.txt"
data = np.genfromtxt(data,delimiter=' ')
x1=data[:,0]*1000
y1=data[:,1]

#===================================================
#BS First order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\results\Biot_first_z.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x2=data_biot[:,0]*1000
y2=abs(data_biot[:,1])

#===================================================
#BS Second order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\results\Biot_sec_z.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x3=data_biot[:,0]*1000
y3=abs(data_biot[:,1])

#===================================================
#Error
error_first=100*abs(y2-y1)/y1
error_second=100*abs(y3-y1)/y1

plt.figure(1)
plt.plot(x1, y1,label='Analítico',color="black")
plt.plot(x2, y2,label='Primeira ordem',color="black",linestyle='-.',lw=3)
plt.plot(x3, y3,label='Segunda ordem',color="black",linestyle='--',lw=3)
plt.xlabel('Distância z [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.grid(True)
plt.savefig(savepath+"\solido_H_"+mesh_type+"_z.pdf", bbox_inches='tight')


fig = plt.figure(2)
ax1 = fig.add_subplot(111)
ax1.semilogy(x3, error_first,label='Primeira ordem',color="black",linestyle='-.',lw=3)
ax1.semilogy(x1, error_second,label='Segunda ordem',color="black")
plt.xlabel('Distância z [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True,which='minor')
plt.grid(True)
plt.savefig(savepath+"\solido_erro_"+mesh_type+"_z.pdf", bbox_inches='tight')



#===================================================
#Line along x
#===================================================

#===================================================
#BS First order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\results\Biot_first_x.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x1=data_biot[:,0]*1000
y1=abs(data_biot[:,1])

#===================================================
#BS Second order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\results\Biot_sec_x.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x2=data_biot[:,0]*1000
y2=abs(data_biot[:,1])

#===================================================
#Error
error_first=100*abs(y2-y1)/y2

plt.figure(3)
plt.plot(x1, y1,label='Primeira ordem',color="black",linestyle='-.',lw=3)
plt.plot(x2, y2,label='Segunda ordem',color="black")
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc="center right")
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.grid(True,which='minor')
plt.grid(True)
plt.axvline(x=-45, color='blue',lw=2)
plt.axvline(x=-60, color='blue',lw=2 )
plt.axvline(x=45, color='blue',lw=2)
plt.axvline(x=60, color='blue',lw=2 )
plt.savefig(savepath+"\solido_H_"+mesh_type+"_x.pdf", bbox_inches='tight')


plt.figure(4)
plt.semilogy(x1, error_first,color="black")
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
frame = legend.get_frame()
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame.set_facecolor('0.90')
plt.grid(True,which='minor')
plt.grid(True)
plt.axvline(x=-45, color='blue',lw=2)
plt.axvline(x=-60, color='blue',lw=2 )
plt.axvline(x=45, color='blue',lw=2)
plt.axvline(x=60, color='blue',lw=2 )
plt.savefig(savepath+"\solido_erro_"+mesh_type+"_x.pdf", bbox_inches='tight')
plt.show()


plt.figure(5)
plt.semilogy(x1, error_first,color="black")
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
frame = legend.get_frame()
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame.set_facecolor('0.90')
plt.grid(True,which='minor')
plt.grid(True)
if mesh_type=="fina":
    plt.ylim(ymin=0.5,ymax=4)
else:
    plt.ylim(ymin=0.5,ymax=4)
plt.axvline(x=-45, color='blue',lw=2)
plt.axvline(x=-60, color='blue',lw=2 )
plt.axvline(x=45, color='blue',lw=2)
plt.axvline(x=60, color='blue',lw=2 )
plt.savefig(savepath+"\solido_erro_"+mesh_type+"_x_zoom.pdf", bbox_inches='tight')
plt.show()
print("Done")

