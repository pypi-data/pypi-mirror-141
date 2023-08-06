import numpy as np

def shells_fcc(a):
	"""find match_indices & mismatch_indices of arr(find_rows) in arr(X), return indices of X
	a   : lattice constant
	"""
	## FCC_shells
	shell_1 = a/np.sqrt(2)  
	shell_2 = a   
	shell_3 = a*np.sqrt(6)/2
	shell_4 = a*np.sqrt(2)
	shell_5 = a*np.sqrt(3)
	
	return shell_1, shell_2, shell_3, shell_4, shell_5
##--------
