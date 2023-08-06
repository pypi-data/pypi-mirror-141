import numpy as np
from ..modeling.periodicBC_operation  import add_periodic_image, wrap_coord_PBC
from ..utils.compute_distance       import dist2_node2nodes
from scipy import spatial


def find_neighbors_gen(P, Box, bndCond=[1, 1, 1], **kwargs):
	""" find Nearest_Neighbors, return generator of Nearest_IDs, "Nearest relative-Position vetors from atom i" 
	Ver 2: spatial.cKDTree
	By Cao Thang, Sep 2019
	Update: Dec 2020 to use generator
	* Input: 
		P          : Nx3 array contain positions of atoms
		Box        : simulation box
		bndCond=[1, 1, 1]:  boundary condition
			Cutoff_Neighbors=6.5: find neighbors within a Cutoff, or 
  			Number_Neighbors=12: find k nearest neighbors
		keepRef=Flase    : include referal-atom in result
	* Ouyput: this output a GEN contains (Near_IDs, Rij_vectors), so access with
		for Near_ID, Rij_vector in GEN:
			print (Near_ID, Rij_vector)

		Near_IDs    : Nx1 list of Mx1-vectors, contain Image_IDs(id of the original atoms before make periodicity) of Nearest atoms 
		Rij_vectors : Nx1 list of Mx3-Matrices, contain Nearest Rij relative-Position vetors from Ref.atom i (Nearest Positions)
		
	Ex:   GEN = thaTool.neighbors_finder_gen(P, Box, bndCond = [1, 1, 1], Cutoff_Neighbors=9, keepRef=False)
	"""
	##==== optional Inputs 
	if 'Cutoff_Neighbors' in kwargs: Rcut = kwargs['Cutoff_Neighbors']  
	elif 'Number_Neighbors' in kwargs:
		near_number = kwargs['Number_Neighbors']  
		if 'Rcut' in kwargs: Rcut = kwargs['Rcut']  
		else: 			     Rcut = 9
	else: raise Exception("The 4th input must be: 'Cutoff_Neighbors' or 'Number_Neighbors'")
	
	if 'keepRef' in kwargs: keepRef = kwargs['keepRef']  
	else: 					keepRef = False
 
	## refine input 
	P = np.asarray(P);    Box = np.asarray(Box);   bndCond = np.asarray(bndCond);
	  
	## Add Periodic_Image at Periodic Boundaries
	_,_,PJ,ImageID = add_periodic_image(P, Box, bndCond, Rcut)
	
	## Detect Neighbors  
	# Near_IDs=[None]*P.shape[0]; Rij_Vectors=[None]*P.shape[0];     # Rij_Bond=[None]*P.shape[0]       # cannot use np array, since it fix the length of rows and cannot assign array to elm    
	if 'Cutoff_Neighbors' in kwargs:  
		treePJ = spatial.cKDTree(PJ)
		treeP = spatial.cKDTree(P)
		ID_listPJ = treeP.query_ball_tree(treePJ, Rcut)   # return list of lists of indice
		
		for i in range(P.shape[0]):
			m = np.asarray(ID_listPJ[i])
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			Rij = dist2_node2nodes(P[i,:], PJ[m,:])
			##--
			yield Near_IDs, Rij[['bx','by','bz']].values     # return 1 element of list
		##--
	 
	if 'Number_Neighbors' in kwargs:   
		treePJ = spatial.cKDTree(PJ)
		for i in range(P.shape[0]):
			_, m = treePJ.query(P[i,:], near_number+1)
			# --
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			Rij = dist2_node2nodes(P[i,:], PJ[m,:])  
			##--    
			yield Near_IDs, Rij[['bx','by','bz']].values      # return 1 element of list
		## --    
	# return Near_IDs, Rij_Vectors          # return all list: Near_IDs, Rij_Vectors, Rij_Bond
##--------

def find_neighbors_list(P, Box, bndCond=[1, 1, 1], **kwargs):
	""" find Nearest_Neighbors, return list of Nearest_IDs, "Nearest relative-Position vetors from atom i" 
	Ver 2: spatial.cKDTree
	By Cao Thang, Sep 2019
	* Input: 
		P          : Nx3 array contain positions of atoms
		Box        : simulation box
		bndCond=[1, 1, 1]:  boundary condition
			Cutoff_Neighbors=6.5: find neighbors within a Cutoff, or 
  			Number_Neighbors=12: find k nearest neighbors
		keepRef=Flase    : include referal-atom in result
	* Ouyput: 
		Near_IDs    : Nx1 list of Mx1-vectors, contain Image_IDs(id of the original atoms before make periodicity) of Nearest atoms 
		Rij_vectors : Nx1 list of Mx3-Matrices, contain Nearest Rij relative-Position vetors from Ref.atom i (Nearest Positions)
		# Rij_Bonds : Nx1 list of scalars, contain Rij_bonds from Ref.atom to Nearest_atoms (Nearest-bonds)
	# NOTEs: don't compute Rij_Bond to save memory
		
	Ex:   Near_IDs, Rij_vectors = thaTool.fNeighbors_finder(P, Box, bndCond = [1, 1, 1], Cutoff_Neighbors=9, keepRef=False)
	"""
	##==== optional Inputs 
	if 'Cutoff_Neighbors' in kwargs: Rcut = kwargs['Cutoff_Neighbors']  
	elif 'Number_Neighbors' in kwargs:
		near_number = kwargs['Number_Neighbors']  
		if 'Rcut' in kwargs: Rcut = kwargs['Rcut']  
		else: 			     Rcut = 9
	else: raise Exception("The 4th input must be: 'Cutoff_Neighbors' or 'Number_Neighbors'")
	
	if 'keepRef' in kwargs: keepRef = kwargs['keepRef']  
	else: 					keepRef = False
 
	## refine input 
	P = np.asarray(P);    Box = np.asarray(Box);   bndCond = np.asarray(bndCond);
	  
	## Add Periodic_Image at Periodic Boundaries
	_,_,PJ,ImageID = add_periodic_image(P, Box, bndCond, Rcut)
	
	## Detect Neighbors  
	Near_IDs=[None]*P.shape[0]; Rij_Vectors=[None]*P.shape[0];     # Rij_Bond=[None]*P.shape[0]       # cannot use np array, since it fix the length of rows and cannot assign array to elm    
	if 'Cutoff_Neighbors' in kwargs:  
		treePJ = spatial.cKDTree(PJ)
		treeP = spatial.cKDTree(P)
		ID_listPJ = treeP.query_ball_tree(treePJ, Rcut)   # return list of lists of indice
		
		for i in range(P.shape[0]):
			m = np.asarray(ID_listPJ[i])
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs[i] = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			# Rij_Bond[i], Rij_Vectors[i] = dist2_node2nodes(P[i,:], PJ[m,:])        # compute distance from atom P[i,:] to its neighbors PJ[m,:]
			df = dist2_node2nodes(P[i,:], PJ[m,:])
			Rij_Vectors[i] = df[['bx','by','bz']] 
		##--
	 
	if 'Number_Neighbors' in kwargs:   
		treePJ = spatial.cKDTree(PJ)
		for i in range(P.shape[0]):
			_, m = treePJ.query(P[i,:], near_number+1)
			# --
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs[i] = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			# Rij_Bond[i], Rij_Vectors[i] = dist2_node2nodes(P[i,:], PJ[m,:])          
			df = dist2_node2nodes(P[i,:], PJ[m,:])
			Rij_Vectors[i] = df[['bx','by','bz']] 			
		## --    
	return Near_IDs, Rij_Vectors          # return all list: Near_IDs, Rij_Vectors, Rij_Bond
##--------




