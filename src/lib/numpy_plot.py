from pylab import *
from numpy import ma

def PlotRNM(nodesCoordenates,elemType,elemNodes,regionExcitation,elemTags,integNodesCoordinates,integPOintResults,region_ID_list):
#    close('all')
    x = []
    y = []

    for line in range(0, len(nodesCoordenates)):
     
        x.append(nodesCoordenates[line][0])
        y.append(nodesCoordenates[line][1])
    
    triangles = []
    zprint=[]
    counter=0
    for line in range(0,len(elemType)):
#    for line in range(2,4):
#        print(elemNodes[line])
        if elemType[line] >1:
            if elemType[line] ==2:
                triangles.append(elemNodes[line])
                region=elemTags[line][0]
            
                Js=0
                for eachregion in regionExcitation:
                    if eachregion.RegionNumber==region:
                        Js=eachregion.Value
                        break
                zprint.append(Js)
                counter+=1
            
            elif elemType[line] ==3:        
                newElem=[]
                newElem.append(elemNodes[line][0])
                newElem.append(elemNodes[line][1])
                newElem.append(elemNodes[line][2])
                triangles.append(newElem)
                region=elemTags[line][0]
                Js=0
                for eachregion in regionExcitation:
                    if eachregion.RegionNumber==region:
                        Js=eachregion.Value
                        break
                zprint.append(Js)
                
                newElem=[]
                newElem.append(elemNodes[line][0])
                newElem.append(elemNodes[line][2])
                newElem.append(elemNodes[line][3])
                triangles.append(newElem)
                zprint.append(Js)
              
            
                counter+=1
    
    teste=np.zeros((len(zprint)))
    for each in range(0,len(zprint)):
        teste[each]=zprint[each]

    
    plt.close("all")
#    plt.tripcolor(x, y, triangles, facecolors=teste, edgecolors='b')
    plt.rc('font', family='Times New Roman',size=15)
    
    plt.triplot(x, y, triangles, 'go-')
    X=[]
    Y=[]
    U=[]
    V=[]
    
#    Print the mesh nodes coordinates
    for eachNode in range(0,len(x)):
#        plt.annotate(str(x[eachNode])+","+str(y[eachNode]),xy=(x[eachNode], y[eachNode]))
        plt.annotate("Node:"+ str(eachNode),xy=(x[eachNode], y[eachNode]))

#    Print the mesh nodes coordinates       
    counter=0
    for eachElem in triangles:
       xelem=(x[eachElem[0]]+x[eachElem[1]]+x[eachElem[2]])/3
       yelem=(y[eachElem[0]]+y[eachElem[1]]+y[eachElem[2]])/3
#       plt.annotate( str(xelem)+","+str(yelem),xy=(xelem, yelem))
       plt.annotate( "Elem:"+str(counter) ,xy=(xelem, yelem))
#       plt.annotate( "Material:"+str(region_ID_list[counter]) ,xy=(xelem, yelem))
       counter+=1


    for nodeiaha in integNodesCoordinates:
      X.append(nodeiaha[0,0])
      Y.append(nodeiaha[1,0])
         
    for values in integPOintResults:
        U.append(np.round(values[0,0],2))
        V.append(np.round(values[1,0],2))
     
    for nodeCounter in range (0,len(X)):
##        print X[nodeCounter], Y[nodeCounter],  U[nodeCounter], V[nodeCounter]
         plt.annotate("Wx="+ str(U[nodeCounter])+" / Wy="+str(V[nodeCounter]),xy=(X[nodeCounter], Y[nodeCounter]-0.1))
#         plt.annotate("x="+ str(X[nodeCounter])+" / y="+str(Y[nodeCounter]),xy=(X[nodeCounter], Y[nodeCounter]))
###         plt.annotate("x="+ str(X[nodeCounter])+" / y="+str(Y[nodeCounter]),xy=(X[nodeCounter], Y[nodeCounter]))
####         plt.text(X[nodeCounter], Y[nodeCounter], str(math.sqrt( math.pow( U[nodeCounter],2)+math.pow(V[nodeCounter],2))))
#         nodeCounter+=1
##      
    
    Q = quiver(X,Y, U, V)
    ax = axes()
    ax.set_aspect(1.)
    show()