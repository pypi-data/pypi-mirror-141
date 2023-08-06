import numpy     as np
import pandas    as pd

# =============================================================================
# RDF LAMMPS
# =============================================================================
class LmpRDF:
	""" class to read Radial Distribution Fuction (RDF) file from Lammps compute
	* Attributes:
		name        : file name
		frame       : 3d pandas Frame (multi-row-index DataFrame)
		
	* Methods:
		ReadRDF       : read RDF file
		AverageRDF    : the Average RDF
	"""
	def __init__(self, **kwargs):
		"""" ** Optional Inputs:
		file_name: input RDF file
		Example:  RDF = thaFileType.lmp_RDF('lammps_RDF/myRDF.txt')"""
		##==== optional Inputs 
		if 'file_name' in kwargs:
			self.name = kwargs['file_name']
			self.readRDF(self.name)
	##-----
	
	def readRDF(self, file_name):
		""" * Compulsory Inputs:
			  file_name   : file_name: input RDF file"""
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		## Extract positions of block
		A = C[3:]
		P = np.char.split(A)            # split each elem of P, result is an array of lists-of-strings
		blockIndex=[i for i,v in enumerate(P) if len(v)==2 ]

		## Extract each block as frame
		frame = [None]* (len(blockIndex))
		for i, elem in enumerate(blockIndex):
			if i < (len(blockIndex)-1): 
				tmp = np.vstack(P[ blockIndex[i]+1 : blockIndex[i+1] ] )   # convert array of lists to array of arrays
			else: tmp = np.vstack(P[blockIndex[i]+1: ] )   
			data = tmp.astype(np.float64)         # convert str to float --> list
			data = np.asarray(data)               # convert list --> array   
			## extract columns
			myColumn = ['row','bin']
			for k in range( int((data.shape[1]-2)/2) ):
				myColumn = myColumn + ['rdf'+str(k+1)] + ['coord'+str(k+1)]
			##--
			frame[i] = pd.DataFrame(data, columns=myColumn)  # create DataFrame
		##-- convert list of dataFrames to multi-index DataFrame
		df3 = pd.concat(frame, keys=['fr%s' %i for i in range(len(frame))], names=['frame'])   # multi-index df

		## Save out put to CLASS's attributes
		self.name      = file_name
		self.frame     = df3           # List of DataFrame
		##--
		return
	##-----

	def averageRDF(self):
		"""compute average of RDF over all frames
		* Output: df_ave: DataFrame of avergave RDF"""
		df3 = self.frame 
		df_ave = df3.groupby(level=1).mean()     # compute average of histogram over multi-frames
		#--
		return df_ave
	##-----

