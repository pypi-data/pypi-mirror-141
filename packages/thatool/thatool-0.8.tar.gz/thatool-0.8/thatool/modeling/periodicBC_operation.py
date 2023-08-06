import numpy as np
import pandas as pd
from ..utils.row_operation    import unique_row, match_row


# =============================================================================
# Functions definition
# =============================================================================
def add_periodic_image(P, Box, bndCond=[1, 1, 1], Rcut=6.5):
	"""%% Function to add "Periodic Images" of atoms at Periodic Boundaries
	% (with a specific cutoff distance)

	% (input) = (P, Box, Rcut, bndCond)
	%        P    : Mx3 Matrix contain positions of atoms before Wrapping
	%        Box  : 3x2 Matrix contain simulation box bounds
	%        Rcut : scalar value of Cutoff distance
	%        bndCond : 1x3 Matrix contain convention of Peridic bounds(ex: bndCond = [1 1 1])

	% [output] = [addAtom, addIndex, allAtom, allIndex]
	%        addAtom : 2d array contain positions of only added atoms 
	%        addIndex :1d array contain conserved Index (added-atoms have the same indices to origin atoms).
	%        allAtom : 2d array combine added atoms + oldAtom
	%        allIndex :1d array combine added Index + oldIndex

	%   Example: addAtom, addIndex, allAtom, allIndex = fBCs_Add_Periodic_Image(P, Box, 2.5, [1 1 0])
	% By Cao Thang, June 2019"""
	
	# refine input 
	P = np.asarray(P);    Box = np.asarray(Box);   bndCond = np.asarray(bndCond);
	
	## Add atoms at Periodic Boundaries
	xB=Box[0,1]-Box[0,0]; yB=Box[1,1]-Box[1,0]; zB=Box[2,1]-Box[2,0];  
	I = np.arange(P.shape[0]);  
	oldIndex = np.copy(I)       # original index of input atoms
	oldAtom = np.copy(P)                    # original input atoms
	# --
	addAtom = np.empty((1,3))       # save all added atoms only, contain 1 dummy-atom as created
	addIndex = np.empty(1)
	
	## on X_bound
	if bndCond[0] == 1:
		col = 0; Dist = xB;
		# left X
		bnd = Box[0,0]; 
		nowIndex = np.arange(P.shape[0]) ; 
		tmpIndex = nowIndex[P[:,col] <= bnd+Rcut] 
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] + Dist;  
		## upadate total P 
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))
		
		# right X
		bnd = Box[0,1]; 
		nowIndex = np.arange(P.shape[0]) ; 
		tmpIndex = nowIndex[P[:,col] >= bnd-Rcut] 
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] - Dist;  
		## upadate total P 
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

	## on Y_bound
	if bndCond[1] == 1:
		col = 1; Dist = yB;
		# left Y
		bnd = Box[1,0]; 
		nowIndex = np.arange(P.shape[0]) ; 
		tmpIndex = nowIndex[P[:,col] <= bnd+Rcut] 
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] + Dist;  
		## upadate total P 
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

		# right Y
		bnd = Box[1,1]; 
		nowIndex = np.arange(P.shape[0]) ; 
		tmpIndex = nowIndex[P[:,col] >= bnd-Rcut] 
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] - Dist;  
		## upadate total P 
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

	## on Z_bound
	if bndCond[2] == 1:
		col = 2; Dist = zB;
		# left Z
		bnd = Box[2,0]; 
		nowIndex = np.arange(P.shape[0]) ; 
		tmpIndex = nowIndex[P[:,col] <= bnd+Rcut] 
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] + Dist;  
		## upadate total P 
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))
		
		# right Z
		bnd = Box[2,1]; 
		nowIndex = np.arange(P.shape[0]) ; 
		tmpIndex = nowIndex[P[:,col] >= bnd-Rcut] 
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] - Dist;  
		## upadate total P 
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))
	
	## Remove first added atom (the dummy-atom when initiate array)
	addAtom = addAtom[1:,:]
	addIndex = addIndex[1:]
	## remove duplicated atoms 
	_,uniqueIndex = unique_row(addAtom, tol_decimal=2)  
	addAtom = addAtom[uniqueIndex]
	addIndex = addIndex[uniqueIndex]
	##--
	_,mismatch_index = match_row(addAtom, oldAtom)
	addAtom = addAtom[mismatch_index]
	addIndex = addIndex[mismatch_index]
	
	# Out put
	allAtom = np.vstack((oldAtom, addAtom))
	allIndex = np.hstack((oldIndex, addIndex))
	
	return addAtom, addIndex, allAtom, allIndex
##--------

def wrap_coord_PBC(P, Box, bndCond=[1, 1, 1]):
  
	  # refine input 
	P = np.asarray(P);    Box = np.asarray(Box);   bndCond = np.asarray(bndCond);
	
	## Add atoms at Periodic Boundaries
	xB=Box[0,1]-Box[0,0]; yB=Box[1,1]-Box[1,0]; zB=Box[2,1]-Box[2,0];  
	oldIndex = np.arange(P.shape[0]);
	
	## on X_bound
	if bndCond[0] == 1:
		col = 0; Dist = xB;
		# left X
		bnd = Box[0,0]; 
		tmpIndex = oldIndex[P[:,col] < bnd] 
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col]%Dist + Dist;
			tmpIndex = oldIndex[P[:,col] < bnd] 

		# right X
		bnd = Box[0,1]; 
		tmpIndex = oldIndex[P[:,col] > bnd] 
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col] - Dist;
			tmpIndex = oldIndex[P[:,col] > bnd]
		
	## on Y_bound
	if bndCond[1] == 1:
		col = 1; Dist = yB;
		# left Y
		bnd = Box[1,0]; 
		tmpIndex = oldIndex[P[:,col] < bnd] 
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col]%Dist + Dist;
			tmpIndex = oldIndex[P[:,col] < bnd] 

		# right Y
		bnd = Box[1,1]; 
		tmpIndex = oldIndex[P[:,col] > bnd] 
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col] - Dist;
			tmpIndex = oldIndex[P[:,col] > bnd]
		
	## on Z_bound
	if bndCond[2] == 1:
		col = 2; Dist = zB;
		# left Z
		bnd = Box[2,0]; 
		tmpIndex = oldIndex[P[:,col] < bnd] 
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col]%Dist + Dist;
			tmpIndex = oldIndex[P[:,col] < bnd] 

		# right Z
		bnd = Box[2,1]; 
		tmpIndex = oldIndex[P[:,col] > bnd] 
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col] - Dist;
			tmpIndex = oldIndex[P[:,col] > bnd]

	return P
##--------




