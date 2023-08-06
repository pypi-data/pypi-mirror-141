

def lines(file_name, keywords=[], **kwargs):
	""" Tool to read lines in a script that match some KEY_WORDs
	* Compulsory Inputs:
		- file_name      : the input file of PLUMED,...
		- keywords=[]: list-of-Keywords to extract a line, ex: METAD, LOGMFD
	** optional Inputs:
	* Outputs:
		- list-of-lines: str
	"""
	with open(file_name,'r') as f:
		C = f.read().splitlines()          # list of strings

	## extract block
	if not keywords:
		found_lines = C
		rest_lines = []
	else:
		idx =  [i for i,elem in enumerate(C) for key in keywords if key in elem ]    # int
		found_lines = [C[i] for i in idx]              
		rest_lines = [C[i] for i in range(len(C)) if i not in idx]   
	##
	return found_lines, rest_lines
##-----




def plumed_block(file_name, block_name=' ', **kwargs):
		""" * Compulsory Inputs:
				- file_name   : the input file of PLUMED,...
				- block_name=: block command in Plumed, ex: METAD, LOGMFD
			** optional Inputs:
			* Outputs:
				- block_of_commandlines: ;ist
		"""
		##== read data
		with open(file_name,'r') as f:
			C = f.read().splitlines()          # list of strings
		## extract block
		Index1=[i for i,elem in enumerate(C) if block_name in elem ]             # list
		B = []
		for i in Index1:
			Index2=[j for j,elem in enumerate(C[i:]) if ('...' in elem and j>0) ]
			if Index2:
				k = Index2[0]
				B.extend(C[i:i+k+1])
		return B
	##-----