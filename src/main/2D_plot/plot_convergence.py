clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt
import math

FEM=[15.23784665,
16.25021876,
17.61004353,
19.34358095,
19.68218577,
20.15283737,
20.33762687]

FFEM=[
15.23784665,
16.25021875,
17.61004351,
19.34358092,
19.68218556,
20.15283734,
20.33762705,
]

elements=[
96,
208,
923,
2012,
4624,
10032,
14482]


converged_FEM=20.8514003979938



#Plots
plt.rc('font',family='Times New Roman')
plt.close("all")
axis_font = { 'size':'20'}

error_FEM=list()
error_FFEM=list()
for counter,each in enumerate(FFEM):
	error_FEM.append( 100*abs(FEM[counter]-converged_FEM)/converged_FEM)
	error_FFEM.append( 100*abs(FFEM[counter]-converged_FEM)/converged_FEM)


plt.figure(1)
plt.semilogy(elements, error_FEM,label='FEM (A-Formulation)',color="black",linestyle='-',lw=3,alpha=0.5)
plt.semilogy(elements, error_FFEM,label='FFEM (B-Formulation)',color="black",linestyle='--',lw=3,alpha=1)
#plt.plot(elements, converged_FEM,label='FEM (Converged)',color="black",linestyle='-.',lw=3,alpha=1)

plt.xlabel('Number of elements',**axis_font)
plt.ylabel('Convergence [%]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
plt.tick_params(axis='x', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)