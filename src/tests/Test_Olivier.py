import numpy as np
def elem0_w0(integ_nodes_coordinates,integ_nodes_results):
#==============================================================================
# Element 0
#==============================================================================
#W0
    integ_nodes_coordinates.append(np.array([[0],[0.333333333333333]]))
    integ_nodes_results.append(np.array([[0.5],[-0.333333333333333]]))
    integ_nodes_coordinates.append(np.array([[0.5],[0.833333333333333]]))
    integ_nodes_results.append(np.array([[0.75],[-0.0833333333333332]]))
    integ_nodes_coordinates.append(np.array([[-0.5],[0.833333333333333]]))
    integ_nodes_results.append(np.array([[0.25],[-0.0833333333333332]]))
    return (integ_nodes_coordinates,integ_nodes_results)

def elem0_w1(integ_nodes_coordinates,integ_nodes_results):
#W1
    integ_nodes_coordinates.append(np.array([[0],[0.333333333333333]]))
    integ_nodes_results.append(np.array([[0],[0.166666666666666]]))
    integ_nodes_coordinates.append(np.array([[0.5],[0.833333333333333]]))
    integ_nodes_results.append(np.array([[0.25],[0.416666666666666]]))
    integ_nodes_coordinates.append(np.array([[-0.5],[0.833333333333333]]))
    integ_nodes_results.append(np.array([[-0.25],[0.416666666666666]]))
    return (integ_nodes_coordinates,integ_nodes_results)
    
def elem0_w2(integ_nodes_coordinates,integ_nodes_results):
#W2
    integ_nodes_coordinates.append(np.array([[0],[0.333333333333333]]))
    integ_nodes_results.append(np.array([[-0.5],[-0.333333333333333]]))
    integ_nodes_coordinates.append(np.array([[0.5],[0.833333333333333]]))
    integ_nodes_results.append(np.array([[-0.25],[-0.0833333333333332]]))
    integ_nodes_coordinates.append(np.array([[-0.5],[0.833333333333333]]))
    integ_nodes_results.append(np.array([[-0.75],[-0.0833333333333332]]))
    return (integ_nodes_coordinates,integ_nodes_results)
#==============================================================================
# Element 1
#==============================================================================
#W0
def elem1_w0(integ_nodes_coordinates,integ_nodes_results):
    integ_nodes_coordinates.append(np.array([[-0.333333333333333],[0]]))
    integ_nodes_results.append(np.array([[-0.333333333333333],[-0.5]]))
    integ_nodes_coordinates.append(np.array([[-0.833333333333333],[0.5]]))
    integ_nodes_results.append(np.array([[-0.0833333333333332],[-0.75]]))
    integ_nodes_coordinates.append(np.array([[-0.833333333333333],[-0.5]]))
    integ_nodes_results.append(np.array([[-0.0833333333333332],[-0.25]]))
    return (integ_nodes_coordinates,integ_nodes_results)
#W1
def elem1_w1(integ_nodes_coordinates,integ_nodes_results):
    integ_nodes_coordinates.append(np.array([[-0.333333333333333],[0]]))
    integ_nodes_results.append(np.array([[-0.166666666666666],[0]]))
    integ_nodes_coordinates.append(np.array([[-0.833333333333333],[0.5]]))
    integ_nodes_results.append(np.array([[-0.416666666666666],[0.25]]))
    integ_nodes_coordinates.append(np.array([[-0.833333333333333],[-0.5]]))
    integ_nodes_results.append(np.array([[-0.416666666666666],[-0.25]]))
    return (integ_nodes_coordinates,integ_nodes_results)
#W2
def elem1_w2(integ_nodes_coordinates,integ_nodes_results):
    integ_nodes_coordinates.append(np.array([[-0.333333333333333],[0]]))
    integ_nodes_results.append(np.array([[0.333333333333333],[-0.5]]))
    integ_nodes_coordinates.append(np.array([[-0.833333333333333],[0.5]]))
    integ_nodes_results.append(np.array([[0.0833333333333332],[-0.25]]))
    integ_nodes_coordinates.append(np.array([[-0.833333333333333],[-0.5]]))
    integ_nodes_results.append(np.array([[0.0833333333333332],[-0.75]]))
    return (integ_nodes_coordinates,integ_nodes_results)

