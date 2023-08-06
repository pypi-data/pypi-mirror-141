### ============================================================================
### Notes about 2D material
### ============================================================================
""" 
* haxagonal Boron Nitride (h-BN) have the same configuration as Graphene
	C-C bond: 1.4 - 1.42 Amstrom
	B-N bond: 1.4 - 1.43 Amstrom
Ref: 10.1039/c7ra00260b
"""
import numpy 	as np
import pandas 	as pd
from matplotlib import path
from ..utils.coord_rotation import rot1axis
from ..utils.row_operation 	import unique_row



### ============================================================================
### Graphene-based Models: 
### ============================================================================
def _UnitCell_Graphene(m, n, bond_CC=1.421, mix_type='AA'): 
	"""Calculates the 3D Cartesian coordinates of atoms of 1 units cell of (n,m)graphene sheet, which which n >= m >= 0
	* Input:
		n,m       : Chiral indices n>=m>=0
		bond_CC    : Length of C-C bonds
		inter_bond : Length of plane-plane bonds
		type='AA'/'A'/'B': to create semi-Graphene lattice for adoptting Hydrogen atoms
			 - 'AA': full Garaphene-like crystal
			 - 'A': semi Graphene-like with atom at A-position
			 - 'B': semi Graphene-like with atom at B-position
	NOTES: n=1, m=0 : is the unit cell for Zigzag
		   n=1, m=1 : is the unit cell for Armchair
		   n>m      : unit cell is automatically computed
		   
	* Output:    
		R         : Nx3 array, contain positions of atoms of 1 units cell of (n,m)graphene sheet.
		lC,LT     : length of Chiral vector and Translational unit vector, corresponding to length on X and Y direction
		ChiralAng : Chiral angle of Graphene sheet
	By Cao Thang Nguyen, Nov 2019 
	Ref: Dresselhaus et al. “Physics of Carbon Nanotubes.”, 1995, doi:10.1016/0008-6223(95)00017-8.
		 Antonsen, and Thomas Garm Pedersen. “Characterisation and Modelling of Carbon Nanotubes,” 2013."""
	
	## check if n >= m >= 0
	if n < m or m < 0: 
		raise Exception('Bad choice of (n,m). Be sure n >= m >= 0')
	if mix_type not in ['AA', 'A', 'B']: 
		raise Exception('Choose mix_type in list: AA/A/B')
	## Compute ONE unit cell
	if m==0:    m=0;   n=n/n;
	elif m==n:  m=n/n;   n=n/n;
	else:       m=m;  n=n;   
	m=int(m) ; n=int(n)  
	## Parameters of 2D graphene
	a = bond_CC*np.sqrt(3)               # length of lattice vector a = |a1| = |a2|
	## Lattice vector and two atomic basis b1, b2 for the graphene sheet
	a1 = a*np.array([1, 0])
	a2 = a*np.array([np.cos(np.pi/3), np.sin(np.pi/3)])
	b1 = np.array([0, 0])
	b2 = a*np.array([1/2, 1/(np.sqrt(3)*2)])
	# Translations vector
	G = np.gcd(2*n+m, 2*m+n)           # Greatest common divisor
	t1 = (2*m+n)/G 
	t2 = -(2*n+m)/G 
	# the number of haxagons in the 1D unit cell
	N = int(2*(n**2 + m**2 + n*m)/G)
	############################################################################
	## Calculations of points for the graphene sheet
	############################################################################
	R = np.zeros((4*N**2,2))    # just estimate sheet_size
	index = -1;
	for i in range(0,N,1):
		for j in range(-N,i,1):
			## For full-Graphene sheet
			if mix_type=='AA':
				index = index + 1 
				R[index, :] = i*a1 + j*a2 + b1        # atom A
				index = index + 1 
				R[index, :] = i*a1+j*a2 + b2          # atom B
			elif mix_type=='A':	
				index = index + 1 
				R[index, :] = i*a1 + j*a2 + b1        # atom A
			elif mix_type=='B':
				index = index + 1 
				R[index, :] = i*a1+j*a2 + b2          # atom B   
			else:
				raise Exception('Choose mix_type in list: AA/A/B')
	###               
	R = R[0:index+1, :]     # remove extra zero-rows
	############################################################################
	
	# Chiral and translations vector
	C = n*a1 + m*a2
	T = t1*a1 + t2*a2
	## Calculation of 2D cartesian coordinates for the (n,m)SWCNT. To avoid identical points 
			# the polygon ABCD restraining the CNT points is moved southwest.
	DD = (bond_CC/1000)/np.linalg.norm(T)         # DD is calculated
	epsilon = (C[0]+T[0])*DD
	myPoly = np.array([[0,0], [C[0],C[1]], [C[0]+T[0],C[1]+T[1]], [T[0],T[1]]]) - epsilon
	# check points inside polygon
	poly = path.Path(myPoly)   
	BoolIndex = poly.contains_points(R)
	RCNT = R[BoolIndex]           # take the inside points          
	# Calculate periodic side 
	lC = np.linalg.norm(C)        # length of Chiral vector, periodic on X
	lT = np.linalg.norm(T)        # length of Translation vector, periodic on Y
	ChiralAng = np.arctan(m*np.sqrt(3)/(2*n+m));   # Chiral angle in rad
	ChiralAng = ChiralAng*180/np.pi;               # convert to deg

	# Rotate matrix to align Chiral direction with X direction
	P = np.column_stack((RCNT, np.zeros((RCNT.shape[0], 1))))    # assign z coordinates = 0
	P = rot1axis(P, ChiralAng, axis='Z')   
	unitbox = np.array([[0, lC], [-lT, 0], [0, 0]])
	# remove duplicate points  
	P,_ = unique_row(P, tol_decimal=2)
	return P, lT, lC, ChiralAng, unitbox
##-------

		
def lattice_Graphene(m, n, bond_CC=1.421, sheet_size=[1,1], sheet_number=1, inter_bond=3.35, mix_type='AA'): 
	"""Calculates the 3D Cartesian coordinates of atoms of (n,m)graphene sheet/ Graphite
	* Input:
		n,m       : Chiral indices n>=m>=0
		bond_CC    : Length of C-C bonds
		inter_bond : Length of plane-plane bonds
		type='AA'/'A'/'B': to create semi-Graphene lattice for adoptting Hydrogen atoms
			 - 'AA': full Garaphene-like crystal
			 - 'A': semi Graphene-like with atom at A-position
			 - 'B': semi Graphene-like with atom at B-position
	NOTES: n=1, m=0 : is the unit cell for Zigzag
		   n=1, m=1 : is the unit cell for Armchair
		   n>m      : unit cell is automatically computed
		   
	* Output:    
		R         : Nx3 array, contain positions of atoms of 1 units cell of (n,m)graphene sheet.
		box       : Simulation box
		ChiralAng : Chiral angle of Graphene sheet"""
	# refine input 
	sheet_size=np.asarray(sheet_size);   sheet_number=int(sheet_number)
	## Compute coordinates of 1 unit cell
	P, lT, lC, ChiralAng, unitbox = _UnitCell_Graphene(m, n, bond_CC, mix_type)
	## Duplicate unit cell
	lx = sheet_size[0]; ly = sheet_size[1]
	repX = int(np.round(lx/lC))           # number of unit cell in X direction
	repY = int(np.round(ly/lT))           # number of unit cell in Y direction
	if repX>=2:
		Pold = np.copy(P)
		for i in range(1,repX,1):
			tmp = np.copy(Pold)
			tmp[:,0] = tmp[:,0]+i*lC
			P = np.vstack((P, tmp))
	if repY>=2:
		Pold = np.copy(P)
		for i in range(1,repY,1):
			tmp = np.copy(Pold)
			tmp[:,1] = tmp[:,1]+i*lT
			P = np.vstack((P, tmp))
	if sheet_number>=2:
		Pold = np.copy(P)
		for i in range(1,sheet_number,1):
			tmp = np.copy(Pold)
			tmp[:,2] = tmp[:,2]+i*inter_bond           
			P = np.vstack((P, tmp))
	# remove duplicate points  
	P,_ = unique_row(P, tol_decimal=2)
	# compute box periodic
	box = np.copy(unitbox)
	if repX>0: box[0,1] = box[0,1] + (repX -1)*lC
	if repY>0: box[1,1] = box[1,1] + (repY -1)*lT
	## box_size in Z
	if sheet_number>0: 
		box[2,1] = box[2,1] + inter_bond/2 + (sheet_number-1)*inter_bond
		box[2,0] = box[2,0] - inter_bond/2 

	return P, ChiralAng, box, lC, lT
##-------
		