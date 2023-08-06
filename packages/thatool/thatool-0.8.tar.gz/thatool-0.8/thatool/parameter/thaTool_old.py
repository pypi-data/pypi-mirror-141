import sys          #, os, glob, re, natsort
sys.path.append("D:\work\myCodes\code_Python")
import thaModel         # thaFileType, thaTool, 
import numpy as np
import pandas as pd
import scipy.spatial
# from tess import Container



### ============================================================================
## Class definition
### ============================================================================








### ============================================================================
## 3D Voronoi Analysis
### ============================================================================
class Voro3D:    # Ver2: copy layer 2nd and 3rd to cover free surface, offset distance = inter-layer distance
	""" Voro ++ library
	* Attributes:
		
	* Methods:
		fAtomicVol_Bulk    : return atomicVol, coord of bulk model
		fAtomicVol_Plate   : return atomicVol, coord of plate model
	By Cao Thang, updated: Jan 2020"""
		
	def __init__(self):
		" "
	## -----------

	def fAtomicVol_Bulk_gen(self, P, Box, calCoord=False):
		"""compute atomic-volume of each atom in Bulk models
		* Input:
			P        : Nx3 Matrix contain positions of atoms
			Box      : simulation box
		**Optional:
			calCoord=False : compute coordiation number
		* Output:    
			atomicVol            : 1xM array of atomic volume 
			coord, cell_neighbor : 1xN list, Nxlist index of neighbors of each atom in original input points

		Ex:	gen2 = thaTool.fAtomicVol_Bulk_gen(P, Box, calCoord=False)   # gen2 = (tomicVol_i, cell_neighbor_i)
			gen3 = thaTool.fAtomicVol_Bulk_gen(P, Box, calCoord=True)    # gen3 = (tomicVol_i, cell_neighbor_i, coord_i)
		"""

		### refine inputs
		boxTuple=((Box[0,0],Box[1,0],Box[2,0]),(Box[0,1],Box[1,1],Box[2,1]))

		voroCell = Container(P, limits=boxTuple, periodic=(1,1,1))
		### compute voronoi volumes/ cell_neighbor (excluded walls)
		for c in voroCell:
			atomicVol_i = c.volume()
			neighbor_i = c.neighbors()
			cell_neighbor_i = [[elem for elem in n if elem>=0] for n in neighbor_i]
			##Coordinate number
			if calCoord==True:
				coord_i = c.number_of_faces()
				yield atomicVol_i, cell_neighbor_i, coord_i   # generator of 3 elements
			else: 
				yield atomicVol_i, cell_neighbor_i          # generator of 2 elements
	##===========
	
	def fAtomicVol_Plate_gen(self, P, simBox, bndCond=(1, 1, 0), maxEdge=3.1, deepSurf=15, virSurface=True, offset=False, calCoord=False):
		"""compute atomic-volume of each atom in Plate models
		update Ver2: copy layer 2nd and 3rd to cover free surface, offset distance = inter-layer distance. So, no need to input offset value
		* Input:
			P        : Nx3 Matrix contain positions of atoms
			simBox   : simulation box

		**Optional:
			bndCond=(1, 1, 0)  : tuple of boundary condtions
			maxEdge=3.1 : value to to compute face-area = maxEdge**2
			deepSurf=15 : = max(peak) - min(valey), unit in Angstrom, use to reduce input data to save memory
			virSurface=True  : apply virtual surface to cover real surface before compute Voronoi
				+ offset=False: extract 2 layers near outmost layer, and use to cover surface, offset_distance is auto computed based on atomic arrangement
				+ offset=true: extract 1 layer near outmost layer, and use to cover surface with offset_distance = offset value
			calCoord=False : compute coordiation number
		* Output:    
			atomicVol            : 1xM array of atomic volume 
			coord, cell_neighbor : 1xN list, Nxlist index of neighbors of each atom in original input points
		"""
		### detect boundary column
		surCond = np.where(np.asarray(bndCond)==0)[0]
		if len(surCond)>1: raise Exception("bndCond is not suitable, only 1 free-surface be accepted")
		col = surCond[0] 

		## =========================
		## conpute cell_neighbor (excluded walls) and Coordination number not use virtual surfaces 
		## =========================
		## reduced Box
		Box = np.copy(simBox)
		Box[col,1] = max(P[:,col]) + 1e-3
		Box[col,0] = min(P[:,col]) - 1e-3
		boxTuple=((Box[0,0],Box[1,0],Box[2,0]),(Box[0,1],Box[1,1],Box[2,1]))
		## compute vornoi reduced Box
		voroCell = Container(P, limits=boxTuple, periodic=bndCond)
		
		## =========================
		## compute voronoi volumes 
		## =========================
		### If not create virtual surfaces 
		if virSurface==False:     
			for c in voroCell:
				atomicVol_i = c.volume()
				neighbor_i = c.neighbors()
				cell_neighbor_i = [[elem for elem in n if elem>=0] for n in neighbor_i]
				##Coordinate number
				if calCoord==True:
					coord_i = c.number_of_faces()
					yield atomicVol_i, cell_neighbor_i, coord_i   # generator of 3 elements
				else: 
					yield atomicVol_i, cell_neighbor_i          # generator of 2 elements
		
		### If use virtual surface (just effect atomic Volume)
		if virSurface==True:               
			### detect surface atoms & make the cover layers for free surfaces
			if offset==False:    # use second layer as virtual surface
				nLayer=3
				hiLayerIndex,loLayerIndex,_ = layer_extractor(P, bndCond, nLayer, maxEdge)
				# lower surface
				d12 = np.mean(P[loLayerIndex[0], col]) - np.mean(P[loLayerIndex[1], col])
				d13 = np.mean(P[loLayerIndex[0], col]) - np.mean(P[loLayerIndex[2], col])
				loAtomLay2 = P[loLayerIndex[1]];    loAtomLay2[:,col] = loAtomLay2[:,col] - 2*abs(d12)
				loAtomLay3 = P[loLayerIndex[2]];    loAtomLay3[:,col] = loAtomLay3[:,col] - 2*abs(d13)
				# higher surface
				d12 = np.mean(P[hiLayerIndex[0], col]) - np.mean(P[hiLayerIndex[1], col])
				d13 = np.mean(P[hiLayerIndex[0], col]) - np.mean(P[hiLayerIndex[2], col])
				hiAtomLay2 = P[hiLayerIndex[1]];    hiAtomLay2[:,col] = hiAtomLay2[:,col] + 2*abs(d12)
				hiAtomLay3 = P[hiLayerIndex[2]];    hiAtomLay3[:,col] = hiAtomLay3[:,col] + 2*abs(d13)
				#--
				Pnew = np.vstack((P, loAtomLay2, loAtomLay3, hiAtomLay2, hiAtomLay3))
			else:   # use first layer as virtual surface
				nLayer=1
				hiLayerIndex,loLayerIndex,_ = layer_extractor(P, bndCond, nLayer, maxEdge)
				# surface atoms
				loAtomLay = P[loLayerIndex[0]];    loAtomLay[:,col] = loAtomLay[:,col] - offset
				hiAtomLay = P[hiLayerIndex[0]];    hiAtomLay[:,col] = hiAtomLay[:,col] + offset
				#--
				Pnew = np.vstack((P, loAtomLay, hiAtomLay))
			###-----------------
			
			### expand Box in surface direction (to cover offsetted surfaces)
			Box = np.copy(simBox)
			Box[col,1] = max(Pnew[:,col]) + 1e-3
			Box[col,0] = min(Pnew[:,col]) - 1e-3
			boxTuple=((Box[0,0],Box[1,0],Box[2,0]),(Box[0,1],Box[1,1],Box[2,1]))
			
			### compute voronoi volumes for enlarged model
			voroCell2 = Container(Pnew, limits=boxTuple, periodic=bndCond)
	
			### retrieve Voronoi volumes for original input P
			# atomicVol2=[c.volume() for c in voroCell2]
			# atomicVol = atomicVol2[:P.shape[0]]

			### retrieve Voronoi volumes for original input P using zip  
			for c,c2 in (voroCell,voroCell2):  # --> this will use the shorter length
				atomicVol_i = c2.volume()
				neighbor_i = c.neighbors()
				cell_neighbor_i = [[elem for elem in n if elem>=0] for n in neighbor_i]
				##Coordinate number
				if calCoord==True:
					coord_i = c.number_of_faces()
					yield atomicVol_i, cell_neighbor_i, coord_i   # generator of 3 elements
				else: 
					yield atomicVol_i, cell_neighbor_i          # generator of 2 elements
	##===========
	
	### ========================================================================
	## Old way, not use generator
	### ========================================================================	
	def fAtomicVol_Bulk(self, P, Box, calCoord=False):
		"""compute atomic-volume of each atom in Bulk models
		* Input:
			P        : Nx3 Matrix contain positions of atoms
			Box      : simulation box
		**Optional:
			calCoord=False : compute coordiation number
		* Output:    
			atomicVol            : 1xM array of atomic volume 
			coord, cell_neighbor : 1xN list, Nxlist index of neighbors of each atom in original input points
		"""
		### refine inputs
		boxTuple=((Box[0,0],Box[1,0],Box[2,0]),(Box[0,1],Box[1,1],Box[2,1]))

		voroCell = Container(P, limits=boxTuple, periodic=(1,1,1))
		### compute voronoi volumes 
		atomicVol = [c.volume() for c in voroCell]

		### conpute cell_neighbor (excluded walls)
		# neighbor = [c.neighbors() for c in voroCell]
		# cell_neighbor = [[elem for elem in n if elem>=0] for n in neighbor]
		cell_neighbor = [[elem for elem in n if elem>=0] for n in [c.neighbors() for c in voroCell] ]   # use this way to save memory
		if calCoord==True:
			coord = [c.number_of_faces() for c in voroCell]
			return np.asarray(atomicVol), cell_neighbor, coord  
		else: 
			return np.asarray(atomicVol), cell_neighbor
	##===========

	def fAtomicVol_Plate(self, P, simBox, bndCond=(1, 1, 0), maxEdge=3.1, deepSurf=15, virSurface=True, offset=False, calCoord=False):
		"""compute atomic-volume of each atom in Plate models
		update Ver2: copy layer 2nd and 3rd to cover free surface, offset distance = inter-layer distance. So, no need to input offset value
		* Input:
			P        : Nx3 Matrix contain positions of atoms
			simBox   : simulation box

		**Optional:
			bndCond=(1, 1, 0)  : tuple of boundary condtions
			maxEdge=3.1 : value to to compute face-area = maxEdge**2
			deepSurf=15 : = max(peak) - min(valey), unit in Angstrom, use to reduce input data to save memory
			virSurface=True  : apply virtual surface to cover real surface before compute Voronoi
				+ offset=False: extract 2 layers near outmost layer, and use to cover surface, offset_distance is auto computed based on atomic arrangement
				+ offset=true: extract 1 layer near outmost layer, and use to cover surface with offset_distance = offset value
			calCoord=False : compute coordiation number
		* Output:    
			atomicVol            : 1xM array of atomic volume 
			coord, cell_neighbor : 1xN list, Nxlist index of neighbors of each atom in original input points
		"""
		### detect boundary column
		surCond = np.where(np.asarray(bndCond)==0)[0]
		if len(surCond)>1: raise Exception("bndCond is not suitable, only 1 free-surface be accepted")
		col = surCond[0] 

		## =========================
		## conpute cell_neighbor (excluded walls)
		## =========================
		## reduced Box
		Box = np.copy(simBox)
		Box[col,1] = max(P[:,col]) + 1e-3
		Box[col,0] = min(P[:,col]) - 1e-3
		boxTuple=((Box[0,0],Box[1,0],Box[2,0]),(Box[0,1],Box[1,1],Box[2,1]))
		## compute vornoi reduced Box
		voroCell = Container(P, limits=boxTuple, periodic=bndCond)
		# neighbor = [c.neighbors() for c in voroCell]        
		# cell_neighbor = [[elem for elem in n if elem>=0] for n in neighbor]
		cell_neighbor = [[elem for elem in n if elem>=0] for n in [c.neighbors() for c in voroCell] ]   # use this way to save memory
		if calCoord==True: coord = [c.number_of_faces() for c in voroCell]
		
		## =========================
		## compute voronoi volumes 
		## =========================
		#### not create virtual surfaces 
		if virSurface==False:               
			atomicVol = [c.volume() for c in voroCell]
		##--------    
		del voroCell    # to release memory
		
		#### use virtual surface
		if virSurface==True:               
			### detect surface atoms & make the cover layers for free surfaces
			if offset==False:    # use second layer as virtual surface
				nLayer=3
				hiLayerIndex,loLayerIndex,_ = layer_extractor(P, bndCond, nLayer, maxEdge)
				# lower surface
				d12 = np.mean(P[loLayerIndex[0], col]) - np.mean(P[loLayerIndex[1], col])
				d13 = np.mean(P[loLayerIndex[0], col]) - np.mean(P[loLayerIndex[2], col])
				loAtomLay2 = P[loLayerIndex[1]];    loAtomLay2[:,col] = loAtomLay2[:,col] - 2*abs(d12)
				loAtomLay3 = P[loLayerIndex[2]];    loAtomLay3[:,col] = loAtomLay3[:,col] - 2*abs(d13)
				# higher surface
				d12 = np.mean(P[hiLayerIndex[0], col]) - np.mean(P[hiLayerIndex[1], col])
				d13 = np.mean(P[hiLayerIndex[0], col]) - np.mean(P[hiLayerIndex[2], col])
				hiAtomLay2 = P[hiLayerIndex[1]];    hiAtomLay2[:,col] = hiAtomLay2[:,col] + 2*abs(d12)
				hiAtomLay3 = P[hiLayerIndex[2]];    hiAtomLay3[:,col] = hiAtomLay3[:,col] + 2*abs(d13)
				#--
				Pnew = np.vstack((P, loAtomLay2, loAtomLay3, hiAtomLay2, hiAtomLay3))
			else:   # use first layer as virtual surface
				nLayer=1
				hiLayerIndex,loLayerIndex,_ = layer_extractor(P, bndCond, nLayer, maxEdge)
				# surface atoms
				loAtomLay = P[loLayerIndex[0]];    loAtomLay[:,col] = loAtomLay[:,col] - offset
				hiAtomLay = P[hiLayerIndex[0]];    hiAtomLay[:,col] = hiAtomLay[:,col] + offset
				#--
				Pnew = np.vstack((P, loAtomLay, hiAtomLay))
			###-----------------
			
			### expand Box in surface direction (to cover offsetted surfaces)
			Box = np.copy(simBox)
			Box[col,1] = max(Pnew[:,col]) + 1e-3
			Box[col,0] = min(Pnew[:,col]) - 1e-3
			boxTuple=((Box[0,0],Box[1,0],Box[2,0]),(Box[0,1],Box[1,1],Box[2,1]))
			
			### compute voronoi volumes for enlarged model
			voroCell = Container(Pnew, limits=boxTuple, periodic=bndCond)
			atomicVol2=[c.volume() for c in voroCell]
			del voroCell
			# retrieve Voronoi volumes for original input P
			atomicVol = atomicVol2[:P.shape[0]]
			
		## OUTPUTs
		if calCoord==True: return np.asarray(atomicVol), cell_neighbor, coord    # 1d array, list-of-lists, list 
		else:              return np.asarray(atomicVol), cell_neighbor        
		# Explain: - atomicVol: 1xM array of atomic volume 
		#          - coord, cell_neighbor: 1xN list, Nxlist index of neighbors of each atom in original input points
	##===========
###========================  End Class  ========================================




# =============================================================================
# Functions definition
# =============================================================================
def layer_extractor(P, bndCond=(1, 1, 0),nLayer=1, maxEdge=3.0, deepSurf=15, method='maxFacePerimeter'):
	"""Extract atoms of outermost layers, based on Voronoi analysis
	* Input:
		  P   : Nx3 Matrix contain positions of atoms
		  bndCond=(1, 1, 0)  : tuple of boundary condtions
		  nLayer   : number of Layers need to extract (nLayer=0 will extract all layers)
		  maxEdge  : value to to compute face-area = maxEdge**2
		  deepSurf : = max(peak) - min(valey), unit in Angstrom, use to reduce input data to save memory
		  method   : 'maxFacePerimeter'  or   'maxFaceArea'
	* Output:    
		hiLayerIndex, loLayerIndex: list of lists (1xM index of atoms in each layer)
	By Cao Thang, Jan 2020"""
	
	## Extract all layers
	if nLayer==0: nLayer = np.inf
	## =========================================================================
	### Detect atoms in each layer
	## =========================================================================
	P1 = np.copy(P)
	oldIndex = np.arange(P1.shape[0])
	# extract outer-most layers
	loLayerIndex =[];   hiLayerIndex =[]     # list 
	while P1.shape[0]!=0 and nLayer>len(loLayerIndex):
		hiSurIndex,loSurIndex = surface_detect(P1, bndCond, maxEdge, deepSurf, method)
		# save outer layer index
		hiLayerIndex.append(oldIndex[hiSurIndex])                           # append high outer layer to list
		if len(loSurIndex)>0: loLayerIndex.append(oldIndex[loSurIndex])     # append low outer layer to list
		# exclude outer layer
		surIndex = np.hstack((hiSurIndex,loSurIndex))
		keepIndex = np.delete(range(P1.shape[0]), surIndex)
		P1 = P1[keepIndex]
		oldIndex = oldIndex[keepIndex]
	#### --
	coreIndex = oldIndex      # the remain atoms of middle core
	return hiLayerIndex, loLayerIndex, coreIndex          # list of lists (lists of (1xM index) of atoms in each layer)
##-------- 

def surface_detect(P, bndCond=(1, 1, 0), maxEdge=3.0, deepSurf=15, method='maxFacePerimeter'):
	"""Extract atoms on free surface, are atoms have Voronoi with max(faceArea) >= maxEdge**2
	* Input:
		  P   : Nx3 Matrix contain positions of atoms
		  bndCond=(1, 1, 0)  : tuple of boundary condtions
		  maxEdge  : value to to compute face-area = maxEdge**2
		  deepSurf : = max(peak) - min(valey), unit in Angstrom, use to reduce input data to save memory
		  method   : 'maxFacePerimeter'  or   'maxFaceArea'
	* Output:    
		hiSurIndex, loSurIndex: 1xM array, index of surface atoms in the original input points  

	* NOTE: - experimental choose: maxEdge=0.73*latticeConst
			- only 1 pair of surface is detect each time
	By Cao Thang, Oct 2019"""
		
	##### if empty P
	if P.shape[0]==0:raise Exception("input P is empty")
		
	# check input
	surCond = np.where(np.asarray(bndCond)==0)[0]
	if len(surCond)>1: raise Exception("bndCond is not suitable, only 1 free-surface be accepted")
	col = surCond[0]
	# ==========================================
	# Reduce size of input P to save memory
	# ==========================================
	oldIndex = np.arange(P.shape[0])
	maxZ=max(P[:,col]);     minZ=min(P[:,col]);        
	if (maxZ-minZ)>2*deepSurf:
		uIndex = oldIndex[P[:,col] >(maxZ-deepSurf)] 
		bIndex = oldIndex[P[:,col] <(minZ+deepSurf)]
		reduceIndex = np.hstack((uIndex, bIndex))
		#--
		Ublock = P[uIndex] 
		Bblock = P[bIndex]
		Bblock[:, col] = Bblock[:, col] + (min(Ublock[:, col]) - max(Bblock[:, col])) +deepSurf/4
		reP = np.vstack((Ublock, Bblock))
	else: 
		reduceIndex = oldIndex    
		reP = P[reduceIndex]         # reduced P
	
	# ==========================================
	# Contruct Box & expand Box in surface direction
	# ==========================================
	box = np.zeros((3,2))
	for i in range(3):
		box[i,0] = min(reP[:,i]) +1e-6;   
		box[i,1] = max(reP[:,i]) +1e-6
	# expand in surface direction
	box[col,0] = box[col,0] -200   
	box[col,1] = box[col,1] +200
	boxTuple=((box[0,0],box[1,0],box[2,0]),(box[0,1],box[1,1],box[2,1]))
	
	# =========================
	# detect surface atoms by Compute Voronoi
	# =========================
	Index_reP = np.arange(reP.shape[0])
	voroCell = Container(reP, limits=boxTuple, periodic=bndCond)
	if method=='maxFacePerimeter':
		maxFacePerimeter = [max(c.face_perimeters()) for c in voroCell]
		chooseIndex_reP = Index_reP[np.asarray(maxFacePerimeter) >= 4*maxEdge]    # atom have large max(face_perimeters)
	if method=='maxFaceArea':
		maxFaceArea = [max(c.face_areas()) for c in voroCell]  
		chooseIndex_reP = Index_reP[np.asarray(maxFaceArea) >= maxEdge**2]        # atom have large max(face_area)
	#--   
	del voroCell         # to release memory
	
	# retrieve original Index in P
	surIndex = reduceIndex[chooseIndex_reP]
	surAtoms = P[surIndex]       # delete non-surface atoms (some wrong-detected atoms inside bulk) - modify "maxEdge" 
	## devide into 2 sufaces
	z0 = np.mean(surAtoms[:,col])
	z1 = np.mean(surAtoms[surAtoms[:,col]>=z0 ,col])   # average of high coordinate atoms
	if abs(z1-z0)>0.1:
		hiSurIndex = surIndex[surAtoms[:,col]>=z0]         
		loSurIndex = surIndex[surAtoms[:,col]<=z0]
	else:
		hiSurIndex = surIndex
		loSurIndex = []
	## --
	return hiSurIndex, loSurIndex          # 1d arrays
##-------- 




def myexp(x):              # use scipy...expit to avoid overload in np.exp
	""" 	"""   
	from scipy.special import expit
	x = np.asarray(x)
	return expit(x) /(1 - expit(x))
##--------







