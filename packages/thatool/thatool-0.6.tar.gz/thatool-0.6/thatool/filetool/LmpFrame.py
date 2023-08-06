# Imports and external programs
# import sys, re, glob, types

from datetime import datetime
from os import error
import numpy as np
import pandas as pd
from numpy import format_float_scientific as formatE, unicode_            # attach box
from ..data     import ATOMIC_MASS

# Class definition            
# =============================================================================
# LAMMPS Frame (single Frame)
# =============================================================================
class LmpFrame:   
	""" Create an Object of single-FRAME of LAMMPS (use for both DATA/DUMP files)
	This class implemented several ways to create `lmpFRAME` object <br>
		- create an empty data object
		- createFRAME object with input data
		- read from DUMP file 
		- read from DATA file 
		- read frome PDB file 
	""" 
	def __init__(self, **kwargs):
		""" there are several ways to initilize the lmpFRAME object
		* Inputs-Compulsory: <br>
		* Inputs-Optional: <br> 
			- readDUMP='file_name' |`string` | is the name of DUMP file
			- readDATA='file_name' |`string` | is the name of DATA file
				- atom_style = 'atomic'|`string` | option to input type of atomistic system
				- iFlag = False        |`boolean` | read iFlag or not
			- readPDB='file_name' |`string` | is the name of PDB file
			- createFRAME=df |`DataFrame`| pd.DataFrame contains atomic positions and properties of system
				- box = [[0,1],[0,1],[0,1]]	|`array` `list`3x2| option to input boxSize
				- box_angle = [0,0,0]        |`array` `list`1x3| option to input box_angle
		* Usage: <br> 
			# empty object
			da = thaFileType.lmpFRAME()
			# oject with input data 
			da = thaFileType.lmpFRAME(createFRAME=df, box=box, box_angle=box_angle)
			# from DUMP file 
			da = thaFileType.lmpFRAME(readDUMP='test.cfg')
			# from DATA file
			da = thaFileType.lmpFRAME(readDATA='mydata.dat', atom_style='atomic', iFlag=False)
			# from PDB file
			da = thaFileType.lmpFRAME(readPDB='test.pdb')

		* **Attributes:** <br> 
			- .file_name   = 'lammps.dat' |`string` | name of input file
			- .timestep = 0   |`integer`| the timestep of configuration
			- .atom    = None |`DataFrame`| DataFrame of per-atom values
			- .propKey  = None |`list`| column-names of properties
			- .box		= np.asarray([[0,1],[0,1],[0,1]]) |`array` `list`3x2| option to input boxSize
			- .box_angle = np.zeros(3)   				|`array` `list`1x3| option to input box_angle
			- .mass		= np.asarray([])  |`array`nx1|	atomic masses
			- .FMTstr 	= "%.6f" |`string` | default format for float numbers, don't use %g because it will lost precision
		"""
		## Default initial attributes
		self.file_name   = None         # string
		self.timestep    = 0            # int
		self.FMTstr 	 = "%.6f"       # dont use %g, because it will lost precision
		self.atom_style  = None         # string

		self.box 		 = np.asarray([[0,1],[0,1],[0,1]])   # 2d array of float64
		self.box_angle   = np.asarray([0, 0, 0])  			 # 1d array of float64
		self.atom        = None         # DataFrame of per-atom values
		self.prop_key    = None         # list
		self.mass	     = None         # DataFrame of per-type values
		## Coeffs parts
		self.num		 = {'num_atom':0, 'num_atom_type':0}    # dict of numbers of sth
		self.line_pair_coeff     = None     # list-of-strings
		self.line_bond_coeff     = None     # list-of-strings
		self.line_angle_coeff    = None     # list-of-strings		
		self.line_dihedral_coeff = None
		self.line_improper_coeff = None
		## cross_coeff Section
		self.line_cross_pair_coeff     = None
		self.line_cross_bond_coeff     = None
		self.line_cross_angle_coeff    = None
		self.line_cross_dihedral_coeff = None
		self.line_cross_improper_coeff = None
		## Bonds definition section
		self.line_bond 		   = None
		self.line_angle        = None
		self.line_dihedral     = None
		self.line_improper     = None
		
		
		## read DumpFile
		if 'readDUMP' in kwargs:
			file_name = kwargs['readDUMP']
			self.readDUMP(file_name)
		## read DataFile 
		elif 'readDATA' in kwargs:
			file_name = kwargs['readDATA']
			if 'atom_style' in kwargs: atom_style = kwargs['atom_style']  
			else:                      atom_style = 'atomic'
			if 'iFlag' in kwargs: iFlag = kwargs['iFlag'] 
			else:                 iFlag = False
			##--
			self.readDATA(file_name, atom_style=atom_style, iFlag=iFlag)   
		## create FRAME
		elif 'createFRAME' in kwargs:
			DataFrame = kwargs['createFRAME']
			if 'box' in kwargs:      self.box = kwargs['box']            
			if 'box_angle' in kwargs: self.box_angle = kwargs['box_angle']  
			##
			self.createFRAME(DataFrame)
		## read PDB
		elif 'readPDB' in kwargs:
			file_name = kwargs['readPDB']
			self.readPDB(file_name)	
		else: raise Exception('file format is unsupported')
		##
		return
	#####=======
	
	def createFRAME(self, DataFrame, **kwargs):
		""" The **method** create new FRAME object with input data.
		* Inputs-Compulsory: <br>
			- DataFrame			|`DataFrame`| pd.DataFrame of input data
		* Inputs-Optional: <br> 
			- box = [[0,1],[0,1],[0,1]]	|`array` `list`3x2| option to input boxSize
			- box_angle = [0,0,0]        |`array` `list`1x3| option to input box_angle
		* Outputs: <br> 
			- .atom  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
		* Usage: <br> 
			da = thaFileType.lmpFRAME()
			da.createFRAME(DataFrame=df)
		"""
		## Save out put to CLASS's attributes
		self.file_name   = 'lammps.dat'
		self.atom     	 = DataFrame   # DataFrame of per-atom values
		self.prop_key    = DataFrame.columns.tolist()  
		## update num_dict
		self.num['num_atom'] = max(pd.unique(self.atom['id']))
		self.num['num_atom_type'] = max(pd.unique(self.atom['type']))

		## Inputs Optional
		if 'box' in kwargs:       self.box = kwargs['box']            
		if 'box_angle' in kwargs: self.box_angle = kwargs['box_angle']  
		###
		return
	#####=======

	def readDUMP(self, file_name):
		"""The **method** create FRAME object by reading DUMP file.
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of DUMP file 
		* Inputs-Optional: <br> 
		* Outputs: <br> 
			- .atom  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
		* Usage: <br> 
			da = thaFileType.lmpFRAME()
			da.readDUMP('dump.cfg')

		NOTEs: use list comprehension to get better performance"""
		## Read whole text and break lines
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		## Extract positions of atoms, and its properties (pd DataFrame)
		## find some text in line --> return line index   
		idx_atom = [i for i,elem in enumerate(C) if 'ITEM: ATOMS' in elem][0]  
		## split each line & covert type of 2d_list								## old code: use numpy --> bad performance
		P = [line.split() for line in C[idx_atom+1 :] if line.split()]   					##  P = np.char.split( C[index+1 :] ).tolist()   # list-of-lists (2d list) 
		P = [[float(elem) for elem in sublist] for sublist in P]                ##  P1 = [elem for elem in P if elem]            # remove empty element
		## extract column's name                                                ##  P = np.asarray(P1).astype(float)             # convert str to float
		myColumn = C[idx_atom].replace('ITEM: ATOMS','').split() 				##  findString = np.char.split( C[index] ).tolist()    							
		df = pd.DataFrame(P, columns=myColumn)        # create DataFrame

		## Extract Header lines string(any lines before & included line: "ITEM: ATOMS...")
		H = C[0:idx_atom+1]
		## Extract Box
		index = [i for i,elem in enumerate(H) if 'ITEM: BOX' in elem][0]    # find index of element
		B = [line.split() for line in H[index+1 : index+4] ] 
		B = np.asarray(B).astype(float)
		# Ortho box
		box = B[:,0:2]
		# Box angle
		if B.shape[1]>2:
			box_angle = np.array([B[0,-1], B[1,-1], B[2,-1]])
		else:
			box_angle = np.array([0, 0, 0])
		
		## Extract TIMESTEP
		index = [i for i,elem in enumerate(H) if 'ITEM: TIMESTEP' in elem][0]
		timeStep = float(H[index+1])
			
		## Save Outputs to CLASS's attributes
		self.file_name    = file_name
		self.timestep     = timeStep 
		self.box          = box           # 2d array of float64
		self.box_angle    = box_angle     # 1d array of float64
		self.atom         = df         # DataFrame of per-atom values
		self.prop_key     = df.columns.tolist()
		##
		return
	#####=======

	def readDATA(self, file_name, **kwargs):
		"""The **method** create FRAME object by reading DATA file.
		The style of atomistic system.The format of "data file" depend on the definition of ["atom_style"](https://lammps.sandia.gov/doc/atom_style.html). See [list of atom_style format](https://lammps.sandia.gov/doc/read_data.html#description)
				- atomic      : atom-ID atom-type x y z
				- charge      : atom-ID atom-type q x y z
				- molecular   : atom-ID molecule-ID atom-type x y z
				- full        : atom-ID molecule-ID atom-type q x y z
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of DATA file 
		* Inputs-Optional: <br> 
			- iFlag: will be auto dectected
			- atom_style: will be auto dectected
		* Outputs: <br> 
			- .atom  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
		* Usage: <br> 
			da = thaFileType.lmpFRAME()
			da.readDUMP('mydata.dat', atom_style='atomic', iFlag=False)
		###
		NOTEs:  - np.char.split(C[index]).tolist()              return "object"
				- np.char.split(C[index]).tolist()              return list
				- np.char.split(C[index1:idx_vel]).tolist()      return list-of-lists (2d list)
		"""
		## Inputs Compulsory
		## Inputs Optional
		# if 'iFlag' in kwargs: iFlag = kwargs['iFlag'] 
		# else:                 iFlag = False

		## Read whole text and break lines
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		first_line = C[0]
		## Read head parts
		idx_mass = [i for i,item in enumerate(C) if 'Masses' in item][0]         # find index of item
		C_head = C[2:idx_mass]
		
		## Extract number of something
		num_atom = 0
		num_bond = 0 
		num_angle = 0 
		num_dihedral = 0 
		num_improper = 0 

		num_atom_type = 0
		num_bond_type = 0 
		num_angle_type = 0 
		num_dihedral_type = 0 
		num_improper_type = 0 
		for i,item in enumerate(C_head):
			if ' atoms' in item: 		num_atom = int(item.split()[0])
			if ' bonds' in item: 		num_bond = int(item.split()[0])
			if ' angles' in item: 		num_angle = int(item.split()[0])
			if ' dihedrals' in item: 	num_dihedral = int(item.split()[0])
			if ' impropers' in item: 	num_improper = int(item.split()[0])

			if 'atom types' in item: 	num_atom_type = int(item.split()[0])
			if 'bond types' in item: 	num_bond_type = int(item.split()[0])
			if 'angle types' in item: 	num_angle_type = int(item.split()[0])
			if 'dihedral types' in item: num_dihedral_type = int(item.split()[0])
			if 'improper types' in item: num_improper_type = int(item.split()[0])
		## save all number-of-sth to a dict
		num = {'num_atom':num_atom, 'num_bond':num_bond, 'num_angle':num_angle, 'num_dihedral':num_dihedral, 'num_improper':num_improper,
				'num_atom_type':num_atom_type, 'num_bond_type':num_bond_type, 'num_angle_type':num_angle_type, 'num_dihedral_type':num_dihedral_type, 'num_improper_type':num_improper_type}

		### head section
		## Extract box & box_angle
		idx_box = [i for i,elem in enumerate(C_head) if 'xlo xhi' in elem][0]
		B = [line.split() for line in C_head[idx_box : idx_box+3] ]
		B = [item[0:2] for item in B] 
		box = np.asarray(B).astype(float)
		Ba = [line.split() for line in C_head[idx_box+3:idx_box+4] ]
		box_angle = np.asarray( Ba[0][0:3] ).astype(float)   
		
		## Extract masses section, atom_name
		M = [line.split() for line in C[idx_mass+1 : idx_mass+num_atom_type+2] if line.split()]  # remove empty element
		M = np.asarray(M)
		df_mass = pd.DataFrame(columns=['type', 'mass', 'atom_name'])
		df_mass['type'] = M[:,0].astype(int)
		df_mass['mass'] = M[:,1].astype(float)
		if M.shape[1]>2: 
			df_mass['atom_name'] = M[:,-1].astype(str)
		else:
			df_mass['atom_name'] = ['']*M.shape[0]

		### Atoms section
		## Extract positions of atoms 
		idx_atom = [i for i,item in enumerate(C) if 'Atoms ' in item][0]         # find index of element
		P = [line.split() for line in C[idx_atom+1 : idx_atom+num_atom+2] if line.split()]  # list-of-lists (2d list)           
		## Set column names
		line = C[idx_atom]
		if len(line.split())>2:
			atom_style = line.split()[-1]
		else: 
			raise Exception('Cannot recognize atom_style. Please define it using key_word: atom_style="style"')

		if atom_style=='atomic':    
			myColumn = ['id','type','x','y','z']
		elif atom_style=='charge':    
			myColumn = ['id','type','q','x','y','z']
		elif atom_style=='molecular': 
			myColumn = ['id','mol','type','x','y','z']
		elif atom_style=='full':      
			myColumn = ['id','mol','type','q','x','y','z']
		else: raise error('atom_style is not support. Just support: atomic, charge, molecular, full')
		## auto dectect iFlag
		if len(P[0])>len(myColumn): iFlag = True
		else: iFlag = False
		if iFlag==True: myColumn.extend(['xFlag','yFlag','zFlag'])
		## auto detect atom_name
		if len(P[0])>len(myColumn): atomName = True
		else: atomName = False

		## convert str to float 
		if atomName==False:
			P = [[float(item) for item in sublist] for sublist in P] 	
		else: 	
			P = [[float(item) for item in sublist[:-2]] for sublist in P] 		           
		##
		df_atom = pd.DataFrame(P, columns=myColumn)

		### Velocity section - Extract Velocities of atoms 
		idx_vel = [i for i,item in enumerate(C) if 'Velocities' in item]    # find index of element
		if idx_vel:         # if idx_vel not empty
			V = [line.split() for line in C[idx_vel[0]+1 : idx_vel[0]+num_atom+2] if line.split()]   # list-of-lists (2d list)
			V = [[float(item) for item in sublist] for sublist in V] 			  # convert str to float
			##
			df_vel = pd.DataFrame(V, columns=['id','vx','vy','vz'])
			df_atom = pd.concat([df_atom, df_vel[['vx','vy','vz']] ], axis=1)


		#####==========================================
		### Read Coeff section (if have) and save as list-of-strings. This is setting parts, that is not easy to modify but must use specific tool depend on forcefield
		idx_pair=[];  idx_bond=[];  idx_angle=[]; idx_dihedral=[];  idx_improper=[]
		## Coeffs section
		newC = C[(idx_mass+num_atom_type+3) : idx_atom]   # reduce C, index defined before this line cannot use for newC
		if num_atom_type>0:
			idx_pair = [i for i,item in enumerate(newC) if 'Pair Coeffs' in item]    # find index of element
			if idx_pair: self.line_pair_coeff = newC[idx_pair[0]:idx_pair[0]+num_atom_type+2]

		if num_bond_type>0:
			idx_bond = [i for i,item in enumerate(newC) if 'Bond Coeffs' in item]    # find index of element
			if idx_bond: self.line_bond_coeff = newC[idx_bond[0]:idx_bond[0]+num_bond_type+2]

		if num_angle_type>0:
			idx_angle = [i for i,item in enumerate(newC) if 'Angle Coeffs' in item]    # find index of element
			if idx_angle: self.line_angle_coeff = newC[idx_angle[0]:idx_angle[0]+num_angle_type+2]

		if num_dihedral_type>0:
			idx_dihedral = [i for i,item in enumerate(newC) if 'Dihedral Coeffs' in item]    # find index of element
			if idx_dihedral: self.line_dihedral_coeff = newC[idx_dihedral[0]:idx_dihedral[0]+num_dihedral_type+2]

		if num_improper_type>0:
			idx_improper = [i for i,item in enumerate(newC) if 'Improper Coeffs' in item]    # find index of element
			if idx_improper: self.line_improper_coeff = newC[idx_improper[0]:idx_improper[0]+num_improper_type+2]

		## cross_coeff Section
		if idx_pair:
			if idx_bond: 
				self.line_cross_pair_coeff = newC[idx_pair[0]+num_atom_type+3 : idx_bond[0]]
			elif not (idx_angle+idx_dihedral+idx_improper):
				self.line_cross_pair_coeff = newC[idx_pair[0]+num_atom_type+3 : -1]
		if idx_bond: 
			if idx_angle: 
				self.line_cross_bond_coeff = newC[idx_bond[0]+num_bond_type+3 : idx_angle[0]]
			elif not (idx_dihedral+idx_improper):
				self.line_cross_bond_coeff = newC[idx_bond[0]+num_bond_type+3 : -1]
		if idx_angle:    
			if idx_dihedral:
				self.line_cross_angle_coeff = newC[idx_angle[0]+num_angle_type+3 : idx_dihedral[0]]
			elif not (idx_improper):
				self.line_cross_angle_coeff = newC[idx_angle[0]+num_angle_type+3 : -1]
		if idx_dihedral:
			if idx_improper:
				self.line_cross_dihedral_coeff = newC[idx_dihedral[0]+num_dihedral_type+3 : idx_improper[0]]
			else:
				self.line_cross_dihedral_coeff = newC[idx_dihedral[0]+num_dihedral_type+3 : -1]
		if idx_improper: 
			self.line_cross_improper_coeff = newC[idx_improper[0]+num_improper_type+3 :-1]

		## Bonds definition section
		newC = C[idx_atom+num_atom+3 :]   # reduce C, index defined before this line cannot use for newC
		if num_bond>0:
			idx = [i for i,item in enumerate(newC) if 'Bonds' in item]    # find index of element
			if idx: self.line_bond = newC[idx[0]:idx[0]+num_bond+2]
		
		if num_angle>0:
			idx = [i for i,item in enumerate(newC) if 'Angles' in item]    # find index of element
			if idx: self.line_angle = newC[idx[0]:idx[0]+num_angle+2]

		if num_dihedral>0:
			idx = [i for i,item in enumerate(newC) if 'Dihedrals' in item]    # find index of element
			if idx: self.line_dihedral = newC[idx[0]:idx[0]+num_dihedral+2]

		if num_improper>0:
			idx = [i for i,item in enumerate(newC) if 'Impropers' in item]    # find index of element
			if idx: self.line_improper = newC[idx[0]:idx[0]+num_improper+2]


		## Save out put to CLASS's attributes
		self.file_name   = file_name         # string
		self.box         = box               # 2d array of float64
		if box_angle.shape[0]>0:
			self.box_angle   = box_angle    # 1d array of float64
		self.atom        = df_atom          # DataFrame of per-atom values
		self.prop_key    = df_atom.columns.tolist()
		self.atom_style  = atom_style       # string
		self.mass        = df_mass          # DataFrame of per-element values
		## Coeffs parts
		self.num		 = num                         # dict of numbers of sth
		return
	#####=======


	def readPDB(self, file_name):
		"""The **method** create FRAME object by reading PDB file.
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of PDB file 
		* Inputs-Optional: <br> 
		* Outputs: <br> 
			- .atom  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
			- .atom['record_name'] |`string`|
			- .atom['atom_name'] |'string'| same as column 'type' in DUMP format
			- .atom['residue_name'] |`string`|
			- .atom['residue_id'] |`integer`|
			- .atom['chain'] |`string`|
			- .atom['occupancy'] |`float`|
			- .atom['beta'] |`float`|
		* Usage: <br> 
			da = thaFileType.lmpFRAME()
			da.readPDB('dump.pdb')
		"""
		## Read whole text and break lines
		with open(file_name,'r') as fileID:
			C = fileID.read().splitlines()              # a list of strings

		## Extract positions of atom
		data = [line.split(" ") for line in C if "ATOM" in line]          # list-of-lists
		P = [[item for item in line if item] for line in data]
		## extract columns
		myColumn = ['record_name', 'id','atom_name','residue_name','chain','residue_id','x','y','z']
		if len(P[0])>9: myColumn = myColumn + ['occupancy']
		if len(P[0])>9: myColumn = myColumn + ['beta']
		## Conert type on some columns of DataFrame
		df = pd.DataFrame(P, columns=myColumn)  # create DataFrame
		df[['id','residue_id','x','y','z']] = df[['id','residue_id','x','y','z']].astype(float)
		if 'occupancy' in df.columns: df['occupancy'] = df['occupancy'].astype(float)
		if 'beta' in df.columns: df['beta'] = df['beta'].astype(float)

		## extract box
		box = np.zeros((3, 2))
		box_angle = np.zeros((1, 3))
		B = [line.split(" ") for line in C if "CRYST1" in line] 
		if len(B)>0:
			B = [item for item in B[0] if item] 
			box[0,1] = float(B[1])
			box[1,1] = float(B[2])
			box[2,1] = float(B[2])
			box_angle[:] = float(B[3]), float(B[4]), float(B[5])

		## Save out put to CLASS's attributes
		self.file_name      = file_name
		self.atom     = df         # List of DataFrame
		self.box 	   = box
		self.box_angle  = box_angle
		return
	#####=======	

	def writeDUMP(self, file_name, **kwargs):
		""" The **method** to write DUMP file.
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of DUMP file 
		* Inputs-Optional: <br> 
			- column =['id','type',...] | `list`1xN| contains columns to be written, by default all columns will be written 
			- FMTstr	= '%.6f'   	| `string` | string format for output values 
		* Outputs: <br> 			
			- file 					| `*.cfg`  | the DUMP file 
		* Usage: <br> 
			da.writeDUMP('test.cfg', column=['id','type','x','y','z'], FMTstr='%.4f')
		"""    
		## Inputs Compulsory
		df       = self.atom 
		box      = self.box 
		box_angle = self.box_angle 
		## Inputs Optional
		if 'column' in kwargs: myColumn = kwargs['column']  
		else:                  myColumn = df.columns.tolist()
		if 'FMTstr' in kwargs: FMTstr = kwargs['FMTstr']  
		else:               FMTstr = self.FMTstr 
		##
		df = df[myColumn]
			 
		## Construct header (any lines before & included line: "Atoms ")  (new code use list-of-strings)
		H = ['ITEM: TIMESTEP']                       # 1d list of strings , no need to set dtype='U256'
		H.append(str(int(self.timestep)))
		H.append('ITEM: NUMBER OF ATOMS')          # attach number of atoms
		H.append( str(df.shape[0]) )
		H.append('ITEM: BOX BOUNDS xy xz yz pp pp pp')
		H.append(formatE(box[0,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[0,1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[0], precision=12,unique=False,trim='-'))
		H.append(formatE(box[1,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[1,1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[1], precision=12,unique=False,trim='-'))
		H.append(formatE(box[2,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[2,1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[2], precision=12,unique=False,trim='-'))
		H.append('ITEM: ATOMS ' + ' '.join(myColumn))
	  
		### Writing Output file
		## write headers
		with open(file_name,'w') as f:
			for line in H:  
				f.write(line +'\n')

		## write Dump data 
		with open(file_name,'a') as f:
			for i,row in df.iterrows():
				line=[("%s"%item) if isinstance(df[df.columns[j]][0],str)
								else ("%i"%item) if df.columns[j] in ['id','mol','type'] 
								else (FMTstr%item).rstrip('0').rstrip('.') 
					            for j,item in enumerate(row.values) ]
				f.write(' '.join(line) +'\n')      # separater.join(list)
		###
		print('Write DUMP, done !')
		return

		# ## write headers
		# with open('test.txt','wb') as fileID:
		# 	np.savetxt(fileID, H, '%s', newline='\n') 
		# ## write Dump data
		# fmt = ''                             
		# for elem in myColumn:
		# 	if elem == 'id' or elem == 'mol' or elem == 'type':   fmt = fmt + '%i  '
		# 	else:                                                 fmt = fmt +FMTstr +' '       # '%.10g '
		# #--    
		# with open(file_name,'ab') as fileID:
		# 	np.savetxt(fileID, df[myColumn], fmt=fmt)	
	#####=======

	def writeDATA(self, file_name, **kwargs):
		""" The **method** to write DATA file.
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of DATA file 
		* Inputs-Optional: <br> 
			- atom_style = 'atomic'	| `string` | 'atomic', 'charge', 'molecular', 'full': the style of atomistic system 
			- iFlag		= False    	| `boolean`| whether or not include iFlag 
			- vel 		= False    	| `boolean`| whether or not write Velocity 
			- FMTstr	= '%.6f'   	| `string` | string format for output values 
			- comment   = ''      	| `string` | the comment 
		* Outputs: <br> 			
			- file 					| `*.dat`  | the DATA file 
		* Usage: <br> 
			da.writeDATA('test.dat', atom_style='atomic', iFlag=False, vel=False, FMT='%.4f')
		"""    
		## Inputs Compulsory
		num	             = self.num      # dict
		box      		 = self.box 
		box_angle 		 = self.box_angle 
		df           	 = self.atom 
		df_mass 		 = self.mass              # DataFrame of per-element values
		if df_mass is None: 
			raise Exception('Atomic masses are not availabe, please set masses')
		else:
			c = set(pd.unique(df['type'])) - set(df_mass['type'].values)  # check all items in list A not in list B
			if c: raise Exception('masses of types {} are not availabe. Please set it.'.format(c))

		## Inputs Optional
		if 'atom_style' in kwargs: 	atom_style = kwargs['atom_style']  
		else:                      	atom_style = 'atomic'
		if 'iFlag' in kwargs: 	iFlag = kwargs['iFlag'] 
		else:                 	iFlag = False
		if 'vel' in kwargs: 	vel = kwargs['vel']     
		else:               	vel = False
		if 'FMTstr' in kwargs: 	FMTstr = kwargs['FMTstr']  
		else:                   FMTstr = self.FMTstr 
		if 'line2' in kwargs: 	line2 = '# ' + kwargs['comment']  
		else: 				    line2 = ' ' 		
		
		## Construct header (any lines before & included line: "Atoms ")    (new code)
		L = ['# LAMMPS data, created by Thang, DATE:' +datetime.now().strftime('%Y-%b-%d %H:%M:%S')]   # 1d list of strings    
		L.append( line2)        
		# L.append( str(df.shape[0]) +' atoms')          # attach number of atoms
		# L.append( str(int(max(df['type']))) +' atom types')        # attach types of atom
		## num_part
		list1 = ['num_atom','num_bond','num_angle','num_dihedral','num_improper','num_atom_type','num_bond_type', 'num_angle_type', 'num_dihedral_type', 'num_improper_type']
		list2 = ['atoms','bonds','angles','dihedrals','impropers','atom types','bond types','angle types','dihedral types','improper types']
		for i,(item1,item2) in enumerate(zip(list1, list2)):
			if (item1 in num.keys()) and num[item1]>0:			
				L.append(str(int(num[item1])) +' ' +item2)

		L.append(' ')
		L.append(formatE(box[0,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[0,1], precision=14,unique=False,trim='-') + ' xlo xhi')
		L.append(formatE(box[1,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[1,1], precision=14,unique=False,trim='-') + ' ylo yhi')
		L.append(formatE(box[2,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[2,1], precision=14,unique=False,trim='-') + ' zlo zhi')
		if np.any(box_angle):
			L.append(formatE(box_angle[0],precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[2], precision=14,unique=False,trim='-') + ' xy xz yz')

		## Masses section
		L.extend([' ','Masses',' '])    # append just add 1 elem to list, extend add list to list
		for i,row in df_mass.iterrows():
			L.append("\t".join([str(row['type']), str(row['mass']), '#', row['atom_name']]))

		## Coeffs_lines section
		if self.line_pair_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_pair_coeff) 
		if self.line_cross_pair_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_cross_pair_coeff) 

		if self.line_bond_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_bond_coeff) 
		if self.line_cross_bond_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_cross_bond_coeff) 

		if self.line_angle_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_angle_coeff) 
		if self.line_cross_angle_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_cross_angle_coeff) 

		if self.line_dihedral_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_dihedral_coeff) 
		if self.line_cross_dihedral_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_cross_dihedral_coeff) 

		if self.line_improper_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_improper_coeff) 
		if self.line_cross_improper_coeff is not None: 
			L.extend([' ']) 
			L.extend(self.line_cross_improper_coeff) 
			
		## write these parts
		with open(file_name,'w') as f:
			for line in L:
				f.write(line +'\n')

		## Atoms section
		if atom_style=='atomic':    myColumn = ['id','type']
		if atom_style=='charge':    myColumn = ['id','type','q']
		if atom_style=='molecular': myColumn = ['id','mol','type']
		if atom_style=='full':      myColumn = ['id','mol','type','q']
		##
		lis = df.columns.tolist()
		if 'x' in lis: myColumn.extend(['x'])
		if 'y' in lis: myColumn.extend(['y'])
		if 'z' in lis: myColumn.extend(['z'])
		if 'xu' in lis: myColumn.extend(['xu'])
		if 'yu' in lis: myColumn.extend(['yu'])
		if 'zu' in lis: myColumn.extend(['zu'])
		if iFlag: myColumn.extend(['xFlag','yFlag','zFlag'])
		##
		df_pos = df[myColumn]
		L = [' ', 'Atoms # '+atom_style ,' ']
		for i,row in df_pos.iterrows():
			line=[("%i"%item) if df_pos.columns[j] in ['id','mol','type','xFlag','yFlag','zFlag'] 
							else (FMTstr%item).rstrip('0').rstrip('.') 
							for j,item in enumerate(row.values) ]
			L.append('\t'.join(line))		 # separater.join(list)		
			# line=''
			# for j,item in enumerate(row.values):
			# 	if df.columns[j] in ['id','mol','type','xFlag','yFlag','zFlag']: 
			# 		line = line + ("%i " %item)
			# 	else: line = line + ((FMTstr %item).rstrip('0').rstrip('.') +' ')

		## write Atom section
		with open(file_name,'a') as f:
			for line in L:
				f.write(line +'\n')      
					
		## write Velocity        
		if vel:  
			df_vel = df[['id','vx','vy','vz']] 
			L = ['\nVelocities\n\n']
			for i,row in df_vel.iterrows():
				line=[("%i"%item) if df_vel.columns[j] in ['id'] 
								else (FMTstr%item).rstrip('0').rstrip('.') 
								for j,item in enumerate(row.values) ]	
				L.append('\t'.join(line))		 # separater.join(list)						
			##					
			with open(file_name,'a') as f:
				for line in L:
					f.write(line +'\n')     

		### Write Bonds definition section
		L = []
		if self.line_bond is not None: 
			L.extend([' ']) 
			L.extend(self.line_bond) 
		if self.line_angle is not None: 
			L.extend([' ']) 
			L.extend(self.line_angle) 
		if self.line_dihedral is not None: 
			L.extend([' ']) 
			L.extend(self.line_dihedral) 
		if self.line_improper is not None: 
			L.extend([' ']) 
			L.extend(self.line_improper) 
		##
		with open(file_name,'a') as f:
			for line in L:
				f.write(line +'\n') 
			
		###
		# print('Write DATA, {:d} atoms, done! Remmember to set atomic MASSes explicitly! https://tinyurl.com/yzv2namz'.format(df.shape[0]))
		print('Write DATA, {:d} atoms, done!'.format(df.shape[0]))
		return
	#####=======

	
	def writeXYZ(self, file_name, **kwargs):
		""" The `method` to write XYZ file.
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of XYZ file 
		* Inputs-Optional: <br> 
			- column 	= ['X','xu','yu','zu'] | `list` 1xN| list contains columns to be written  
			- FMTstr	= '%.6f'   	| `string` | string format for output values 
		* Outputs: <br> 			
			- file 					| `*.cfg`  | the XYZ file 
		* Usage: <br> 
			da.writeXYZ('test.xyz')
		"""    
		## Inputs Compulsory
		df = self.atom 
		## Inputs Optional
		if 'FMTstr' in kwargs:	FMTstr = kwargs['FMTstr']  
		else:               FMTstr = self.FMTstr 
		
		## Writing to file
		## header
		H = ['Atoms. Timestep: 0']
		with open(file_name,'w') as f:
			for line in H:  
				f.write(line +'\n')
		## position XYZ
		myColumn = ['type']
		lis = df.columns.tolist()
		if 'x' in lis: myColumn.extend(['x'])
		if 'y' in lis: myColumn.extend(['y'])
		if 'z' in lis: myColumn.extend(['z'])
		if 'xu' in lis: myColumn.extend(['xu'])
		if 'yu' in lis: myColumn.extend(['yu'])
		if 'zu' in lis: myColumn.extend(['zu'])
		#--
		df = df[myColumn]
		## write
		with open(file_name,'a') as f:
			for i,row in df.iterrows():
				line=[("%i"%item) if df.columns[j] in ['id','mol','type'] 
								else (FMTstr%item).rstrip('0').rstrip('.') 
					            for j,item in enumerate(row.values) ]
				f.write(' '.join(line) +'\n')      # separater.join(list)
		##--
		print('Write XYZ, done !')
		return 
	#####=======

	def writePDB(self, file_name, **kwargs):
		""" The **method** to write PDB file; https://zhanggroup.org/SSIPe/pdb_atom_format.html
		* Inputs-Compulsory: <br>
			- file_name   			| `string` | the name of XYZ file 
		* Inputs-Optional: <br> 
			- FMTstr	= '%.6f'   	| `string` | string format for output values 
			- writeBox = False : write box or not
		* Outputs: <br> 			
			- file 					| `*.pdb`  | the PDB file 
		* Usage: <br> 
			da.writePDB('test.pdb')
		"""    
		## specific which data to write
		df       = self.atom 
		box      = self.box 
		box_angle = self.box_angle 

		## add column for PDB format
		if 'record_name' not in df.columns.tolist(): 
			df['record_name'] = ['ATOM']*df.shape[0]
		else: pass

		if 'atom_name' not in df.columns.tolist(): 
			if 'type' in df.columns.tolist(): 
				df['atom_name'] = df['type'].astype(int)
			else: df['atom_name'] = ['X']*df.shape[0]
			
		if 'residue_name' not in df.columns.tolist(): 
			df['residue_name'] = ['XX']*df.shape[0]
		else: pass

		if 'residue_id' not in df.columns.tolist(): 
			df['residue_id'] = [1]*df.shape[0]
		else: pass

		if 'chain' not in df.columns.tolist(): 
			df['chain'] = ['L']*df.shape[0]
		else: pass

		if 'occupancy' not in df.columns.tolist(): 
			df['occupancy'] = [0]*df.shape[0]
		else: pass

		if 'beta' not in df.columns.tolist(): 
			df['beta'] = [0]*df.shape[0]
		else: pass

		if 'segment_name' not in df.columns.tolist(): 
			df['segment_name'] = ['THA']*df.shape[0]
		else: pass

		if 'element_sym' not in df.columns.tolist(): 
			df['element_sym'] = ['X']*df.shape[0]
		else: pass

		## specific columns to be written
		if 'x' not in df.columns.tolist(): 
			myColumn = ['record_name','id','atom_name','residue_name','chain','residue_id', 'xu','yu','zu','occupancy','beta','segment_name','element_sym']
		else: myColumn = ['record_name','id','atom_name','residue_name','chain','residue_id', 'x','y','z','occupancy','beta','segment_name','element_sym']
		df = df[myColumn]

		## chose writeBox or not
		if 'writeBox' in kwargs: writeBox = kwargs['writeBox'] 
		else: writeBox = False

		## Construct header (any lines before & included line: "Atoms ")  (new code use list-of-strings)
		H = ['HEADER    PDB reference structure created by Thang ' +datetime.now().strftime('%Y-%b-%d %H:%M:%S')]    # 1d list of strings 
		  
		### Writing Output file
		## write headers
		with open(file_name,'w') as f:
			for line in H:  
				f.write(line +'\n')

		## write Box: http://www.wwpdb.org/documentation/file-format-content/format33/sect8.html#CRYST1
		if writeBox:
			ang1,ang2,ang3 = 90,90,90
			sGroup = 'P 1'
			Zvalue = 1
			FMTstr = "%-6s %-9g %-9g %-9g %-7g %-7g %-7g %-11s %-4i \n"
			with open(file_name,'a') as f:
				f.write(FMTstr % ("CRYST1", box[0,1],box[1,1],box[2,1], ang1,ang2,ang3, sGroup,Zvalue))

		## write Atom coordinates
		fmt = ""                             
		for item in myColumn:
			if item=='record_name': 	fmt = fmt +"%-6s "
			if item=='id': 				fmt = fmt +"%-5i "
			if item=='atom_name': 		fmt = fmt +"%-5s "
			if item=='residue_name': 	fmt = fmt +"%-3s "
			if item=='chain': 			fmt = fmt +"%-1s "
			if item=='residue_id': 	fmt = fmt +"%-4i "
			if item in ['x','y','z','xu','yu','zu']: fmt = fmt +"%-8g "
			if item=='occupancy': 		fmt = fmt +"%-6g "
			if item=='beta': 			fmt = fmt +"%-6g "
			if item=='segment_name':    fmt = fmt +"%-4s "
			if item=='element_sym':     fmt = fmt +"%-2s "
		##   
		with open(file_name,'a') as f:
			for i,row in df.iterrows():
				f.write( (fmt+"\n") % tuple(row.values) ) 
			f.write( 'END') 
		###
		print('Write PDB, done !')
		return
	#####=======


	def addColumn(self, data, **kwargs):
		""" The **method** to add new columns to da.atom.
		* Inputs-Compulsory: <br>
			- data   			| `DataFrame` `Series` `List` | Nxm data of new columns
		* Inputs-Optional: <br> 
			- newColumn	= data.columns | `list-string` | 1xN list contains names of columns, if do not provide, it take columnNames from DataFrame
			- replace	= False | `boolean`| replace column if existed
		* Outputs: <br> 			
			- .atom  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
		* Usage: <br> 
			da.addColumn(df, myColumn=['col1','col2'], replace=True)
		"""    
		## Inputs Compulsory
		if isinstance(data, pd.DataFrame): newdf = data
		if isinstance(data, pd.Series):    newdf = data.to_frame()
		if isinstance(data, list):         newdf = pd.DataFrame(data)
		if isinstance(data, np.ndarray):   newdf = pd.DataFrame(list(data))
		
		## Inputs Optional
		if 'newColumn' in kwargs: 
			myColumn = kwargs['newColumn']  
			newdf.columns = myColumn
		if 'replace' in kwargs: replace = kwargs['replace']  
		else: 					replace = False

		### ==========================================
		### Add columns/column
		### ==========================================
		olddf  = self.atom 
		## If exist columns
		newCols = newdf.columns.tolist()
		oldCols = olddf.columns.tolist()
		existCols = [elem for elem in newCols if elem in oldCols]     # find intersect list
		if existCols:
			if replace==True: olddf.drop(columns=existCols, inplace=True)        # delete columns in olddf. If inplace=False, must return a copy olddr=olddf.drop()
			else: 
				newColChange = [elem+'1' if elem in existCols else elem for elem in newCols] # change name in newCols to avoid duplicate name     
				newdf.columns = newColChange
		##--
		self.atom = pd.concat([olddf, newdf], axis=1)
		return
	#####=======

	def deleteColumn(self, delColumns):
		""" The **method** to delete columns from da.atom.
		* Inputs-Compulsory: <br>
			- delColumns	      | `list-string` | 1xN list contains names of columns to be deleted
		* Inputs-Optional: <br> 
		* Outputs: <br> 			
			- .atom  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
		* Usage: <br> 
			da.deleteColumn(delColumns=['col1','col2'])
		""" 
		for elem in delColumns:
			if elem in self.atom.columns.tolist():
				self.atom.drop(columns=elem, inplace=True)        # delete columns in olddf
		return
	#####=======

	def set_mass(self, element_dict):
		""" The **method** to set masses of atoms in system.
		difine element_dict with 2 keys: 'type', 'atom_name'
		element_dict = {'type':[1,2,3], 'atom_name'=['C','H','N']}
		* Inputs-Compulsory: <br>
			- element_dict={'type': list_values, 'atom_name':list_values}	  | `dict` | 1xN list contains names of columns to be deleted
		* Inputs-Optional: <br> 
		* Outputs: <br> 			
			- .mass  |`DataFrame`| pd.DataFrame contains positions and properties of configuration
		* Usage: <br> 
			da.set_mass(element_dict={'type':[1,2,3], 'atom_name':['C','H','N']})
		""" 
		## Inputs 
		df_mass = self.mass 
		c = set(element_dict['type']) - set(pd.unique(self.atom['type']))   # check all items in list A not in list B
		if c: raise Exception('input types {} are not in system'.format(c))
		##
		new_mass = [ATOMIC_MASS[elem] for elem in element_dict['atom_name']]
		element_dict['mass'] = new_mass
		df = pd.DataFrame.from_dict(element_dict)
		
		if df_mass is None: 
			df_mass = df
		else:
			df_mass.drop(df_mass[df_mass['type'].isin(df['type'])].index, inplace=True)
			df_mass = pd.concat([df_mass, df], axis=0)

		## Output
		self.mass = df_mass.sort_values(['type'])   
		return
	#####=======

	def combine_frame(self, LmpFrame, align_box='MINxyz', **kwargs):
		""" The **method** to combine 2 Lammps Frames.
		* Inputs-Compulsory: <br>
			- LmpFrame	  | `LmpFrame Obj` | an Object of LmpFrame
		* Inputs-Optional: <br> 
			- align_box='MINxyz'/'COM': alignment box
			- shift_dist=[0,0,0]: distance to shift positions in Obj2 in 3 axes respectively.
			- sep_dist=[]
		* Outputs: <br> 			
			- new Object of LmpFrame
		* Usage: <br> 
			da1.combine_frame(da2)
		* NOTEs: cannot combine box_angle
		""" 
		## Inputs 
		da1 = self
		da2 = LmpFrame
		if da2.atom_style != da1.atom_style:
			raise Exception('atom_style of LmpFrame_Obj_2 must same as LmpFrame_Obj_1')

		## Alignment
		if align_box=='COM':	
			com_da1 = da1.atom[['x','y','z']].mean(axis=0)	
			com_da2 = da2.atom[['x','y','z']].mean(axis=0)
			com_dist = com_da1 - com_da2
			##
			da2.atom['x'] = da2.atom['x'] + com_dist[0]
			da2.atom['y'] = da2.atom['y'] + com_dist[1]
			da2.atom['z'] = da2.atom['z'] + com_dist[2]
			da2.box[0,:] = da2.box[0,:] + com_dist[0]
			da2.box[1,:] = da2.box[1,:] + com_dist[1]
			da2.box[2,:] = da2.box[2,:] + com_dist[2]
		if align_box=='MINxyz':
			x_dist = da1.box[0,0] - da2.box[0,0]
			y_dist = da1.box[1,0] - da2.box[1,0]
			z_dist = da1.box[2,0] - da2.box[2,0]
			##
			da2.atom['x'] = da2.atom['x'] + x_dist
			da2.atom['y'] = da2.atom['y'] + y_dist
			da2.atom['z'] = da2.atom['z'] + z_dist
			da2.box[0,:] = da2.box[0,:] + x_dist
			da2.box[1,:] = da2.box[1,:] + y_dist
			da2.box[2,:] = da2.box[2,:] + z_dist
		
		## Shift position of da2
		if 'shift_dist' in kwargs: 
			bias = kwargs['shift_dist']
			da2.atom['x'] = da2.atom['x'] + bias[0]
			da2.atom['y'] = da2.atom['y'] + bias[1]
			da2.atom['z'] = da2.atom['z'] + bias[2]
			da2.box[0,:] = da2.box[0,:] + bias[0]
			da2.box[1,:] = da2.box[1,:] + bias[1]
			da2.box[2,:] = da2.box[2,:] + bias[2]
		if 'sep_dist' in kwargs: 
			bias = kwargs['sep_dist']	
			sep = da2.atom['z'].min()-da1.atom['z'].max()
			if sep>0:
				sep = sep 
			else: 
				sep = -sep 
			da2.atom['z'] = da2.atom['z'] + bias[2] + sep

	

		## combine Atom_section
		df1 = da1.atom
		df2 = da2.atom
		df2['id']   = df2['id'] + df1['id'].max()
		df2['type'] = df2['type'] + df1['type'].max()
		if 'mol' in df1.columns.tolist():
			df2['mol'] = df2['mol'] + df1['mol'].max()
		##
		self.atom = pd.concat([df1,df2], axis=0, ignore_index=True)
		## update number_atom
		self.num['num_atom'] = max(self.atom['id'])
		self.num['num_atom_type'] = pd.unique(self.atom['type']).shape[0]

		## combine Masses_section
		df1 = da1.mass
		df2 = da2.mass
		df2['type'] = df2['type'] + df1['type'].max()
		self.mass = pd.concat([df1,df2], axis=0, ignore_index=True)

		## combine box (Note: cannot combine box_angle so far)
		box1 = da1.box
		box2 = da2.box
		box = np.asarray([[0,0],[0,0],[0,0]]) 
		box[0,0], box[1,0], box[2,0] = min(box1[0,0],box2[0,0]), min(box1[1,0],box2[1,0]), min(box1[2,0],box2[2,0])
		box[0,1], box[1,1], box[2,1] = max(box1[0,1],box2[0,1]), max(box1[1,1],box2[1,1]), max(box1[2,1],box2[2,1])
		self.box = box

		## line_pair_coeff (if have) (not yet implemeted, just insert empty lines)
		if da1.line_pair_coeff is not None:
			for i in range(int(da2.num['num_atom_type'])):
				da1.line_pair_coeff.append(' ')

		return
	#####=======


	def unwrap_coord_DATA(self, iFlag=['x','y','z'], atom_types=[]):
		""" The **method** to upwrap coords in DATA file.
		* Inputs-Compulsory: <br>
		* Inputs-Optional: <br> 
			- iFlag=['x','y','z']: image Flags in data file
			- type=[]: just unwrap some atom-types, default = all-types
		* Outputs: <br> 			
			- new Object of LmpFrame
		* Usage: <br> 
		* NOTEs: cannot unwrap_coord_data if iFlags are not available.
		""" 
		pd.options.mode.chained_assignment = None 
		## Inputs 
		box = self.box
		df = self.atom
		if atom_types: 
			df = df[df['type'].isin(atom_types)]

		if (set(iFlag) - set(df.columns.tolist())):
			raise Exception('Periodic image Flags are not found in data file.')
	
		for i,item in enumerate(iFlag):
			if item=='x':
				df['x'] = df['x'] + (box[0,1]-box[0,0]) *df['xFlag']
				df['xFlag'] = 0
			if item=='y':
				df['y'] = df['y'] + (box[1,1]-box[1,0]) *df['yFlag']
				df['yFlag'] = 0
			if item=='z':
				df['z'] = df['z'] + (box[2,1]-box[2,0]) *df['zFlag']
				df['zFlag'] = 0

		## Save output
		self.atom.loc[self.atom['id'].isin(df['id']), ['x','y','z','xFlag','yFlag','zFlag']] = df[['x','y','z','xFlag','yFlag','zFlag']]
		return 