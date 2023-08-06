import numpy as np
import pandas as pd



def dist2_node2nodes(node, nodes):
	"""copmute bond_len and postion_vetors from 1 point to a list of points"""
	## inputs
	node = np.asarray(node);  nodes = np.asarray(nodes)
	## compute
	d = nodes - node                                  # Nx3 array of Rij postion_vetors
	dist2 = np.sqrt(np.einsum('ij,ij->i', d, d))      # Nx1 array of distances
	## Out a df
	df = pd.DataFrame(np.column_stack((dist2,d)), columns=['bond_len','bx','by','bz']) 
	return df
	##--------






