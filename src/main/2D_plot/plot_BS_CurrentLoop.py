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
mesh_type="fina"
#===================================================
#Line along Z
#===================================================

#===================================================
#Analitycal
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Line\results\analyt.txt"
data = np.genfromtxt(data,delimiter=' ')
x1=data[:,0]*1000.0
y1=data[:,1]

#===================================================
#BS First order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Line\results\Biot_first_z.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x2=data_biot[:,0]*1000.0
y2=data_biot[:,1]

#===================================================
#BS Second order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Line\results\Biot_second_z.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x3=data_biot[:,0]*1000
y3=data_biot[:,1]

#===================================================
#Error
error_first=100.0*abs(y2-y1)/y1
error_second=100.0*abs(y3-y1)/y1

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
plt.savefig(savepath+"\linha_H_"+mesh_type+"_z.pdf", bbox_inches='tight')


fig = plt.figure(2)
ax1 = fig.add_subplot(111)
ax1.semilogy(x3, error_first,label='Primeira ordem',color="black",linestyle='-.',lw=3)
ax1.semilogy(x3, error_second,label='Segunda ordem',color="black")
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
plt.savefig(savepath+"\linha_erro_"+mesh_type+"_z.pdf", bbox_inches='tight')



#===================================================
#Line along x
#===================================================

#===================================================
#BS First order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Line\results\Biot_first_x.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x1=data_biot[:,0]*1000
y1=data_biot[:,1]

#===================================================
#BS Second order
data_biot=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Line\results\Biot_second_x.txt"
data_biot = np.genfromtxt(data_biot,delimiter=' ')
x2=data_biot[:,0]*1000
y2=data_biot[:,1]

#===================================================
#Error
error_first=100*abs(y1-y2)/y2

plt.figure(3)
plt.plot(x1, y1,label='Primeira ordem',color="black",linestyle='-.',lw=3)
plt.plot(x2, y2,label='Segunda ordem',color="black")
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.grid(True,which='minor')
plt.grid(True)
plt.axvline(x=-150, color='blue',lw=2)
plt.axvline(x=150, color='blue',lw=2 )
#plt.savefig(savepath+"\linha_H_"+mesh_type+"_x.pdf", bbox_inches='tight')

plt.figure(4)
plt.plot(x1, y1,label='Primeira ordem',color="black",linestyle='-.',lw=3)
plt.plot(x2, y2,label='Segunda ordem',color="black")
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
if mesh_type=="grossa":
    plt.ylim(ymax=1000.0)
else:
    plt.ylim(ymax=1500.0)

plt.axvline(x=-150, color='blue',lw=2)
plt.axvline(x=150, color='blue',lw=2 )
plt.grid(True)
#plt.savefig(savepath+"\linha_H_"+mesh_type+"_x_zoom.pdf", bbox_inches='tight')


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
plt.axvline(x=-150, color='blue',lw=2)
plt.axvline(x=150, color='blue',lw=2 )
plt.show()
#plt.savefig(savepath+"\linha_erro_"+mesh_type+"_x.pdf", bbox_inches='tight')

plt.figure(6)
plt.semilogy(x1, error_first,color="black")
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
frame = legend.get_frame()
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame.set_facecolor('0.90')

if mesh_type=="grossa":
    plt.ylim(ymin=3,ymax=600)
else:
    plt.ylim(ymin=0.6,ymax=2.0)

plt.grid(True,which='minor')
plt.grid(True)
plt.axvline(x=-150, color='blue',lw=2)
plt.axvline(x=150, color='blue',lw=2 )
#plt.savefig(savepath+"\linha_erro_"+mesh_type+"_x_zoom.pdf", bbox_inches='tight')
plt.show()

print("Done")