from math import sqrt

### ============================================================================
### Functions definition
### ============================================================================
def box_orientation(box_size=[1,1,1], **kwargs): 
	""" covert Orirentation and length of simulation box, unit lattice
	* Input:
		- box_size=[1,1,1]: dimension of box on each side as in 100 direction
		- Defien orient:
			- zDirect: input by direction of z-side
			- xDirect: input by direction of x-side
	Return: 
		- 3x3 2d-lít of 3 directional vectors"""
	### input 
	Lx,Ly,Lz = box_size
	## set orientation of crytal (Z-direction)
	if 'zDirect' in kwargs: 
		zDirect = kwargs['zDirect']
		if zDirect=='001':   
			orient = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] 
		elif zDirect=='110': 
			orient = [[1, -1, 0], [0, 0, -1], [1, 1, 0]]
			Lx,Ly,Lz = round(Lx/sqrt(2)), Ly, round(Lz/sqrt(2)) 
		elif zDirect=='111': 
			orient = [[1, -1, 0], [1, 1, -2], [1, 1, 1,]]
			Lx,Ly,Lz = round(Lx/sqrt(2)), round(Ly/(sqrt(6)/2)), round(Lz/sqrt(3)) 
		elif zDirect=='112': 
			orient = [[-1, -1, 1], [1, -1, 0], [1, 1, 2]] 
			Lx,Ly,Lz = round(Lx/sqrt(3)), round(Ly/sqrt(2)), round(Lz/(sqrt(6)/2))
		else: raise Exception("Crystal orientation is not suitable. zDirect='001'/'110'/'111'/'112' ")

	## Define based on X-direction
	elif 'xDirect' in kwargs: 
		xDirect = kwargs['xDirect']  
		if xDirect=='001' or xDirect=='100':   
			orient = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] 
		elif xDirect=='110': 
			orient = [[1, -1, 0], [0, 0, -1], [1, 1, 0]]
			Lx,Ly,Lz = round(Lx/sqrt(2)), Ly, round(Lz/sqrt(2)) 
		elif xDirect=='111': 
			orient = [[-1, -1, 1], [1, -1, 0], [1, 1, 2]] 
			Lx,Ly,Lz = round(Lx/sqrt(3)), round(Ly/sqrt(2)), round(Lz/(sqrt(6)/2))   
		else: raise Exception("Crystal orientation is not suitable. xDirect='001'/'100'/'110'/'111' ")

	else: raise Exception('Please input: zDirect or xDirect!')
	###
	return orient, (Lx,Ly,Lz)
########
