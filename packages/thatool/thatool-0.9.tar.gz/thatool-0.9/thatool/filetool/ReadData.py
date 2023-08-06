import re
import numpy as np
import pandas as pd

# =============================================================================
# Read the Result files
# =============================================================================
class ReadData:
	""" class to read TEXT files which results of simulation
	* Read various types of TEXT file
	"""
	
	def logMFD(file_name, dim=1, mod='full'):
		""" * Compulsory Inputs:
				- file_name   : the logmfd.out file
			** optional Inputs:
				- dim=1: dimension of Mean-Force
				- mod='full'/'compact': mode 'compact' read only Mean-Force and CV, mode 'full' read whole text file
			* Outputs:
				- df: pandas DataFrame
		"""
		
		##=== refine inputs
		if dim<1: raise Exception('dim must > 0')

		##== read data
		if mod=='full':
			myColumn =['MFDstep','Flog','CV_Temp','eta', 'Veta']
			for i in range(dim):
				myColumn.extend(['CV'+str(i+1), 'CV'+str(i+1)+'_vel', 'CV'+str(i+1)+'_force'])
			##--
			data = np.loadtxt(file_name)
		if mod=='compact':
			myColumn =['MFDstep','Flog','CV_Temp']
			useCol = [0,1,2];   cvPosition = 2
			for i in range(dim):
				myColumn.append('CV'+str(i+1))
				cvPosition = cvPosition+3
				useCol.append(cvPosition)
			##--
			data = np.loadtxt(file_name, usecols=useCol )
		##--
		df = pd.DataFrame(data, columns=myColumn)
			
		return df
	##-----

	def matrix_miss_value(file_name, **kwargs):
		""" read Data that number of values in each line are not equal, ex: p2p binance (missing values)
		This cannot be read by Numpy, Pandas,...
		* Compulsory Inputs:
				- file_name   : the simple TEXT file contain data
			** optional Inputs:
				- comment='#' : comment-line mark
			* Outputs:
				- df: pandas DataFrame
		"""  
		##=== refine inputs         
		if not file_name: Exception('Input file is not found!')
		if 'comment' in kwargs: comment = kwargs['comment']
		else: comment = '#'
			
		## read Data line-by-line
		with open(file_name,'r') as f:
			C = f.read().splitlines()          # list of strings (each line is 1 string)

		## eliminate comment lines
		C = [elem for elem in C if "#" not in elem]
		## split words in each straing --> 2d_list
		P = np.char.split(C).tolist()             

		## Creat DataFrame from 2d_list
		df = pd.DataFrame(P).astype(float)   # also covert str-->float
		##====  
		return df
	##=======


	def matrix(file_name, **kwargs):
		""" * Compulsory Inputs:
				- file_name   : the simple TEXT file from LAMMPS,...
			** optional Inputs:
				- columnName=['col1','col2',...]: Names of columns to extract
				- columnLine=0: the Line to extract column's Name if columnName is not available. 
					"columnLine=0" means the first line of text. If "columnLine" is also not availale, then default column's name is: 0 1 2...
				- usecols=(1,2)
			* Outputs:
				- df: pandas DataFrame
		"""  
		##=== refine inputs         
		if not file_name: Exception('Input file is not found!')
			
		##==== read data
		if 'usecols' in kwargs: 
			if 'columnName' not in kwargs: raise Exception('Must provide "columnName" for "usecols" ')
			if 'columnLine' in kwargs: data = np.loadtxt(file_name, usecols=kwargs['usecols'], skiprows=1)
			else: 					   data = np.loadtxt(file_name, usecols=kwargs['usecols'])
		else:
			if 'columnLine' in kwargs: data = np.loadtxt(file_name,skiprows=1)
			else:					   data = np.loadtxt(file_name)
		
		##==== Set Column Names (optional Inputs)
		if 'columnName' in kwargs: 
			myColumn = kwargs['columnName']
		else:
			if 'columnLine' in kwargs: 
				columnLine = kwargs['columnLine']
				## extract column's name
				with open(file_name,'r') as f:
					C = f.read().splitlines()          # list of strings (each line is 1 string)
				## extract column's name
				if data.ndim==2: sizeMat = data.shape[1]    # if data is 2d array
				if data.ndim==1: sizeMat = data.shape[0]   # if data is 1d array
				B = C[columnLine]                       # string
				headString = B.replace('#','')                      # string
				colString = np.char.split(headString).tolist()       # array of list --> list
				myColumn = colString[-sizeMat:]                    # get last items   
		
		##==== create DataFrame if data is 2d; create Series if data is 1d
		if data.ndim==2:     # if data is 2d array
			if 'myColumn' in locals(): df = pd.DataFrame(data, columns=myColumn)        # check if VAR exist
			else:                      df = pd.DataFrame(data)        # a DataFrame
		if data.ndim==1:     # if data is 1d array
			if 'myColumn' in locals(): df = pd.Series(data, index=myColumn)             
			else:                      df = pd.Series(data)             # a Series
		##====  
		return df
	##=======	
	
	def lammps_var(file_name):
		""" * Compulsory Inputs:
				- file_name   : the input file of LAMMPS,...
			** optional Inputs:
			* Outputs:
				- ds: pandas Series contains variable in Lammps file
		"""
		##== read data
		fileID = open(file_name,'r')
		C = fileID.read().splitlines()          # list of strings
		fileID.close() 
		##--
		B = [elem.replace('\t',' ') for elem in C if 'variable' in elem]  # take all lines begins with "variable", and remove '\t'
		## extract var_names and values
		var_name = [elem.split()[1] for elem in B]
		varValue = [float(elem.split()[3]) if elem.split()[2]=='equal' else elem.split()[3] for elem in B]
		##- create Pandas Series
		ds = pd.Series(varValue, index=var_name)
		##--
		return ds
	##-----

	def plumed_var(file_name, var_name='INTERVAL', **kwargs):
		""" Search number: https://stackoverflow.com/questions/15814592/how-do-i-include-negative-decimal-numbers-in-this-regular-expression
		* Compulsory Inputs:
				- file_name   : the input file of PLUMED,...
				- var_name : keyworks in Plumed, ex: INTERVAL,...
			** optional Inputs:
				- block_name='all': block command in Plumed, ex: METAD, LOGMFD
			* Outputs:
				- var: float, value of var_name
		"""
		##== collect args
		block_name = kwargs['block_name'] if 'block_name' in kwargs else 'all'      # x = value1 if "condition" else value2

		##== read data
		with open(file_name,'r') as f:
			C = f.read().splitlines()          # list of strings

		## extract block
		if block_name=="all":
			B = C
		else:
			Index1=[i for i,elem in enumerate(C) if block_name in elem ][0]                # int
			Index2=[i for i,elem in enumerate(C) if ('...' in elem and i>Index1) ][0]
			B = C[Index1:Index2]
		## extract var_names and values
		A = [elem.replace('\t',' ') for elem in B if var_name in elem]  # take all lines begins with "variable", and remove '\t'
		varString=re.search(var_name + '.+\d+', A[0])[0]   # 1
		varValue = float( re.search(r'-?\d+\.\d+|-?\d+', varString)[0] )
		##--
		return varValue
	##-----





