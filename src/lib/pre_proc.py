#===============================================================================
# Doctoral student: Anderson Santos Nunes
# University: UFSC - GRUCAD
#===============================================================================
from structs import RegionMaterial,RegionExcitation,BC, PreProcData,ExternalReluctances,CouplingNetworks,ExternalMagneticField
from read_write_TXT_files import get_mesh,get_file_block,get_data_from_file
from materials_library import get_materials_lib
import numpy as np
#===============================================================================
# Get the  pre-processing data
#===============================================================================
def get_preproc_data(mesh_file_name, setup_file_name):
	local_mesh = get_mesh(mesh_file_name)
	data = get_data_from_file(setup_file_name)
	materials_library = get_materials_lib()
#------------------------------------------------------------------------------
# Regions
	regions = []
	materials_data = get_file_block('$Material', '$EndMaterial', 0, data,float)
	for line in materials_data:
		regions.append(RegionMaterial(RegionNumber=int(line[0]), MaterialName=line[1]))

#------------------------------------------------------------------------------
# Excitations
	excitations = []
	materials_data = get_file_block('$Excitations', '$EndExcitations', 0, data,float)
	for line in materials_data:
		if len(line)>2:
			this_value=np.array([float(line[1]),float(line[2]),float(line[3])])
		else:
			this_value=float(line[1])
		excitations.append(RegionExcitation(RegionNumber=int(line[0]), Value=this_value))

#------------------------------------------------------------------------------
# External magnetic field
	external_field = []
	external_field_data = get_file_block('$ExternalMagneticField', '$EndExternalMagneticField', 0, data,float)
	for line in external_field_data:
		if len(line)>3:
			this_value=np.array([float(line[1]),float(line[2]),float(line[3])])
		else:
			this_value=np.array([float(line[1]),float(line[2])])
		external_field.append(ExternalMagneticField(RegionNumber=int(line[0]), Value=this_value))

#------------------------------------------------------------------------------
# Boundary condictions
	BCs = []
	materials_data = get_file_block('$BCs', '$EndBCs', 0, data,float)
	for line in materials_data:
		BCs.append(BC(LineNumber=int(line[0]), Value=float(line[1])))

#------------------------------------------------------------------------------
# External reluctances
	relutances=[]
	materials_data = get_file_block('$External_reluctances', '$EndExternal_reluctances', 0, data,float)
	for line in materials_data:
		relutances.append(ExternalReluctances(node_from=int(line[0]),node_to=int(line[1]),LS=float(line[2]),Material= str(line[3]),fmm=line[4]))

#------------------------------------------------------------------------------
# Coupling networks
	coupling_data=[]
	materials_data = get_file_block('$Coupling_reluctances', '$EndCoupling_reluctances', 0, data,float)
	for line in materials_data:
		coupling_data.append(CouplingNetworks(PhysLine=int(line[0]),Node=int(line[1]),Face_ID_List=list()))
	ExternalReluctances
	return PreProcData(MeshData=local_mesh, MaterialProp=materials_library, RegionMaterial=regions, RegionExcitation=excitations,
				BC=BCs,ExternalReluctances=relutances, CoupNet=coupling_data, ExternalMagneticField=external_field)