import re
import numpy     as np
import pandas    as pd

# =============================================================================
# LOG file LAMMPS
# =============================================================================
class LmpLogFile:
	""" Create an Object of LOG file.
	NOTEs: run 0 without data
	* Attributes:
		name        : file name
		frame       : 3d pandas Frame (multi-row-index DataFrame)
		
	* Methods:
		ReadHisto       : read Histogram file
		AverageHisto    : the Average Histogram
		AreaHisto       : Area under pdf curve
		find_tail()     : find limit of histogram
		find_center()   : find center of histogram
	"""
	def __init__(self, **kwargs):
		"""" ** Optional Inputs:
				file_name: input LOG file
		Example:  RDF = thaFileType.lmp_RDF('lammps_RDF/myRDF.txt')"""
		##==== optional Inputs 
		if 'file_name' in kwargs:
			self.name = kwargs['file_name']
			self.read_log(self.name)
	##-----

	def read_log(self, file_name):
		""" * Compulsory Inputs:
				file_name  : input LOG file
			*Output:
				self.frame: list of DataFrames (cannot use multi-row-index DataFrame, because some runs have different thermo-properties)
			  """
		fileID = open(file_name,'r')
		C = fileID.read().splitlines()              # a list of strings
		# C = np.asarray(C)                         # convert list to numpy array
		fileID.close() 

		## Extract positions of Thermo-properties blocks
		findStr = [re.search('Per MPI rank *', elem)  for elem in C]
		index1 = [i for i,v in enumerate(findStr) if v != None]
		findStr = [re.search('Loop time of *', elem)  for elem in C]
		index2 = [i for i,v in enumerate(findStr) if v != None]

		## Extract each block as frame
		my_column = ['grid','histo','dHisto']
		frames = [None]*len(index1)                      # list
		for i in range(len(index1)):
			if i in range(len(index2)): P = C[ (index1[i]+2) : index2[i] ]     # list of strings 
			else: P = C[ (index1[i]+2) : ]                # for the case simulation interupted
			##--   
			if not(P): pass     # check empty list of run 0
			else: 
				P = np.char.split(P)                            # split each elem of P, result is an array of lists
				P = np.vstack(P[:])                             # convert array of lists to array of arrays
				data = P.astype(np.float64)                     # convert str to float
				#-- extract column's name
				sizeMat = data.shape[1]
				headString = np.char.split(C[index1[i]+1]).tolist()   # array of list --> list
				my_column = headString[:sizeMat]                       # get head items
				##--
				frames[i] = pd.DataFrame(data, columns=my_column)      # create DataFrame
		## eliminate empty items from list
		save_frames = [elem for elem in frames if isinstance(elem, pd.DataFrame) ]

		## Save out put to CLASS's attributes
		self.name      = file_name
		self.frame     = save_frames         # List of DataFrame
		##--
		return
	##-----

