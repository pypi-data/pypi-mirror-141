from ..utils.compute_distance    import dist2_node2nodes
import numpy as np


## 1. Local Crystallinity
def Local_Crystalinity(g, Points, **kwargs):
	"""Function to Calculate Order Parameter with multi_vectors K
	** Input:
		g   : Kx3 Matrix contain g_vectors  (ex: [1,0,0; 0,1,0])
		P   : Nx3 Matrix contain positions of atoms
    ** optional Inputs:
        switch_function=[1,1...,1] : Nx1 array, contain values of switching function s(Rj) (Rj is positions of atom j)
	** Output:    
		aveLC  	: real number, is average Order Parameter , tage over on input g_factors, 0 <= LC <=1      
		LC  	: Kx1 vetor of real numbers, are Order Parameters corresponding to each g-vector 0 <= LC <=1 
		# S   	: Kx1 vetor of complex numbers, are Static Structure Factors corresponding to each g-vector

		NOTES: if multi g-vectors is input, then OrderPara is take by averaging
			over all g-vectors.
		Example: aveLC,LC = thangTools.Local_Crystalinity([1,0,0; 0,1,0], X)
	By Cao Thang, Apr 2019"""

	##==== compulsory Inputs 
	g = np.asarray(g)
	P = np.asarray(Points)	
	
	##==== optional Inputs (compute switching function)
	if 'switch_function' in kwargs:
		sw = kwargs['switch_function']
		Rij = dist2_node2nodes([0,0,0], P)   
		SW,_ = sw.Evaluate(Rij['bond_len'])
	else:  SW = np.ones(P.shape[0])          # if empty
	
	## Compute Order Parameter
	Ng = g.shape[0]; 
	LC = np.zeros(Ng, dtype=float);    # LC is a vector of Ng components
	# S = np.zeros(Ng, dtype=complex);   # S is a vector of Ng complex-components
	# --
	for i in range(Ng):
		d = np.einsum('ij,j->i', P, g[i,:])   # same d = P @ g[i,:]   , dot product of each row of matrix P w.r.t vetor g[i,:]

		SumNatoms = sum(SW*np.exp(1j*d));     # Sum over all atoms
		tmp  = SumNatoms/ sum(SW) ;      			
		LC[i] = (abs(tmp))**2;                # Order_Parameter square of module of complex number
		# S[i] = tmp;                           # Static Structure Factor 
	# --  
	aveLC = sum(LC)/Ng;                  # Static Structure Factor Averaging over all g_vectors 
	return aveLC, LC   
##--------

	