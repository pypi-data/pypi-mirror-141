import numpy as np
from ..modeling             import box_orientation, shells_fcc
from ..utils.coord_rotation import CoordTransform


## Define scipt to copmute FCCUBIC:
def FCCUBIC_script(a_fcc,orient,**kwargs):
	"""PLUMED script to compute FCCUBIC"""
	## options inputs
	if "label" in kwargs: label = kwargs['label']
	else: 				  label = 'mcv'
	if "alpha" in kwargs: alpha = kwargs['alpha']
	else: 				  alpha = 27
	if "options" in kwargs: options = kwargs['options']
	else: 					 options = ''
	## select atoms
	if "atomsA" in kwargs: 
		partialCompute = True
		atomsA = kwargs['atomsA']
		if "atomsB" in kwargs: atomsB = kwargs['atomsB']
		else:                  raise Exception('Must set "atomsB')
	else: 
		partialCompute = False
		if "atoms" in kwargs: atoms = kwargs['atoms']
		else:                 atoms = '@mdatoms'
	
    ##$ Switching: CUBIC --> compute d0 from lattice constant
    ## FCC_shells
	shell_1,shell_2,*_ = shells_fcc(a_fcc)
	## Cutoff
	d0   = shell_1 + (shell_2 - shell_1)/20
	dmax = shell_1 + (shell_2 - shell_1)/2  # distance between shell 1 and shell 2   

    ### =============================================================================
    ### print FCCUBIC setting 
    ### =============================================================================
	## compute Euler Angles
	newAxis = orient
	oldAxis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
	if np.array_equal(oldAxis,orient)==False:
		BT = CoordTransform(old_orient=newAxis, new_orient=oldAxis)        # use reverse rotation since FCCUBIC roteate positions to principal axes then calculated it
		Phi,Theta,Psi = BT.euler_angle(unit='rad')
	else: 
		Phi,Theta,Psi = 0,0,0
	##
	C = []
	C.append('%s: FCCUBIC ...'                             %(label) )
	C.append('\tSWITCH={CUBIC D_0=%.8f D_MAX=%.8f}'        % (d0, dmax) )
	C.append('\tALPHA=%i PHI=%.10f THETA=%.10f PSI=%.10f'  % (alpha, Phi, Theta, Psi) ) 
	if partialCompute==True:
		C.append('\tSPECIESA=%s SPECIESB=%s %s'            %(atomsA, atomsB, options) )
	else:
		C.append('\tSPECIES=%s %s'                         %(atoms, options) )
	C.append('...')
	return C
##====


## Define scipt to copmute FCCUBIC:
def LOCAL_CRYSTALINITY_script(a_fcc,zDirect,**kwargs):
	"""PLUMED script to compute LOCAL_CRYSTALINITY"""
	## optional inputs
	if "label" in kwargs: label = kwargs['label']
	else: 				  label = 'mcv'
	if "atoms" in kwargs: atoms = kwargs['atoms']
	else: 				    atoms = '@mdatoms'
	if "optional" in kwargs: optional = kwargs['optional']
	else: 					 optional = ''
	if "vectors" in kwargs: vectors = kwargs['vectors']
	else: 				  	vectors = [[1,0,0], [0,1,0], [0,0,1]]
	
    ##$ Switching: CUBIC --> compute d0 from lattice constant
    ## FCC_shells
	shell_1,shell_2,*_ = shells_fcc(a_fcc)
	## Cutoff
	d0 = shell_1 + (shell_2 - shell_1)/8
	dmax = shell_1 + (shell_2 - shell_1)*2/5  # distance between shell 1 and shell 2    

    ### =============================================================================
    ### print LOCAL_CRYSTALINIY setting 
    ### =============================================================================
	## compute reciprocal vectors
	g = (4*np.pi/a)*np.asarray(vectors)  
	## Rotate vectors
	newAxis,_ = box_orientation(zDirect=zDirect)
	BT = CoordTransform(new_orient=newAxis)          # old_orient=newAxis, 
	g = BT.rotate_3d(g)
	##
	C = ['{:s}: LOCAL_CRYSTALINITY ...'.format(label)]
	C.append('\tSPECIES={:s}'.format(atoms) )
	C.append('\tSWITCH={CUBIC D_0=%.8f D_MAX=%.8f}' % (d0,dmax) )
	## G-vetors
	for i in range(g.shape[0]):
		C.append("\tGVECTOR%i=%.9f,%.9f,%.9f" 		% (i+1, g[i,0], g[i,1], g[i,2]) )

	C.append('\t{:s}'.format(optional) )
	C.append('...')
	return C
##====





## Define scipt to copmute LogMFD:
def LOGMFD_script(ARG, FICT, FICT_MIN, FICT_MAX, TEMP, DELTA_T, 
                  INTERVAL, KAPPA, deltaF, deltaX, kB, **kwargs):
	"""PLUMED script to compute LOGFMD
	* Inputs:
		- ARG: the scalar input for this action
		- FICT:  The initial values of the fictitious dynamical variables
		- FICT_MIN, FICT_MAX: Boundaries of CV_space
		- TEMP: Temperature of the fictitious dynamical variables
		- DELTA_T: Time step for the fictitious dynamical variables (MFD step)
		- INTERVAL: Period of MD steps ( Nm) to update fictitious dynamical variables
		- KAPPA: Spring constant of the harmonic restraining potential for the fictitious dynamical variables
		- deltaF: Energy Barrier to estimate ALPHA (Alpha parameter for LogMFD)
		- deltaX: CV distance at each MFDstep, to estimate MFICT, VFICT (mass & velocity of fictitious dynamical variable)
		- kB : Boltzmann constant
		
	* Input optional:
	    - label='mfd':
		- FLOG = 5000: The initial free energy value in the LogMFD, initial F(X)
		- MFDstat='VS': Type of thermostat for the fictitious dynamical variables. NVE, NVT, VS are available.
	"""
	## optional inputs
	if "label" in kwargs: label = kwargs['label']
	else: 				  label = 'mfd'
	if "FLOG" in kwargs: FLOG = kwargs['FLOG']
	else: 				 FLOG = 5000
	if "MFDstat" in kwargs: MFDstat = kwargs['MFDstat']
	else: 				    MFDstat = 'VS'

	### =============================================================================
	### estimated ALPHA
	### =============================================================================
	ALPHA = (1.5/(kB*TEMP)) *np.log(deltaF/(kB*TEMP))         # deltaF in unit eV
	### estimated MFICT + VFICT (initial velocity)
	MFICT = kB*TEMP * (DELTA_T/deltaX)**2
	VFICT = np.sqrt( (kB*TEMP)/MFICT )  

	### =============================================================================
	## Define scipt to copmute LogMFD:
	### =============================================================================
	D = []
	D.append('%s: LOGMFD ...'                         % (label))
	D.append('\tARG=%s'                               % (ARG))
	D.append('\tFICT=%.7f FICT_MIN=%.7f FICT_MAX=%.7f'% (FICT, FICT_MIN, FICT_MAX) )
	D.append('\tTEMP=%.2f DELTA_T=%.2f INTERVAL=%i'     % (TEMP,DELTA_T,INTERVAL) )
	D.append('\tFLOG=%.1f ALPHA=%f KAPPA=%g '         % (FLOG,ALPHA,KAPPA) )
	D.append('\tMFICT=%f VFICT=%f '                   % (MFICT,VFICT) )
	D.append('\tTHERMOSTAT=%s'                        % (MFDstat) )	
	## for NVT thermostat
	if MFDstat=='NVT':  
		META = MFICT/1                          # or take: kB*temp *10000
		VETA = np.sqrt( (kB*TEMP)/META ) 
		D.append('\tMETA=%f VETA=%f'  % (META, VETA)) 
	D.append('...')

	return D
##====


