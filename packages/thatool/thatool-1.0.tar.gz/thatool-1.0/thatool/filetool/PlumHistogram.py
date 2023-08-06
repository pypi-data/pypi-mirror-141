import re
import numpy     as np
import pandas    as pd

# =============================================================================
# HISTOGRAM Plumed
# =============================================================================
class PlumHistogram:
	""" Create an Object of DUMP file
	* Attributes:
		name        : file name
		frame       : 3d pandas Frame (multi-row-index DataFrame)
		
	* Methods:
		read_histogram       : read Histogram file
		average_histogram    : the Average Histogram
		AreaHisto       : Area under pdf curve
		find_tail()     : find limit of histogram
		find_center()   : find center of histogram
		
	Example:  RDF = thaFileType.lmp_RDF(file_name='lammps_RDF/myRDF.txt')
	"""
	
	def __init__(self, **kwargs):
		"""" ** Optional Inputs:
				file_name: input RDF file
		Example:  RDF = thaFileType.lmp_RDF(file_name='lammps_RDF/myRDF.txt')"""
		##==== optional Inputs 
		if 'file_name' in kwargs:
			self.name = kwargs['file_name']
			self.read_histogram(self.name)
	##-----

	def read_histogram(self, file_name):
		""" * Compulsory Inputs:
				file_name  :  input HISTOGRAM file
			*Output:
				self.frame: multi-row-index DataFrame
			  """
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		## Extract positions of atoms, and its properties
		findStr = [re.search('#! FIELDS*', elem)  for elem in C]
		index1 = [i for i,v in enumerate(findStr) if v != None]
		findStr = [re.search('#! SET periodic_*', elem)  for elem in C]
		index2 = [i for i,v in enumerate(findStr) if v != None]

		## Extract each block as frame
		my_column = ['grid','hist','dHist']
		frame = [None]*len(index2)                      # list
		for i in range(len(index2)):
			if i < (len(index2)-1): P = C[ (index2[i]+1) : index1[i+1] ]     # list of strings
			else: P = C[ (index2[i]+1) : ]                          
			#--
			P = np.char.split(P)                            # split each elem of P, result is an array of lists
			P = np.vstack(P[:])                             # convert array of lists to array of arrays
			data = P.astype(np.float64)                     # convert str to float
			#--
			frame[i] = pd.DataFrame(data, columns=my_column)  # create DataFrame
		#-- convert list of dataFrames to multi-index DataFrame
		df3 = pd.concat(frame, keys=['fr%s' %i for i in range(len(frame))], names=['frame'])   # multi-index df

		## Save out put to CLASS's attributes
		self.name      = file_name
		self.frame     = df3           # List of DataFrame
		##--
		return
	##-----

	def average_histogram(self):
		"""compute average of histogram over all frames
		* Output: df_ave: DataFrame of avergave histogram"""
		df3 = self.frame 
		df_ave = df3.groupby(level=1).mean()     # compute average of histogram over multi-frames
		#--
		return df_ave
	##-----

	def areaHisto(self):
		hist = self.average_histogram()
		x, y = hist['grid'], hist['hist']
		#--
		return np.trapz(y, x)
	##-----

	def fit_std_gaussian(self):
		"""Fit the average-histogarm to Standard Gaussian function
		* Output: (amp, miu, sigma): parameters of Gaussian function"""
		from scipy.optimize import curve_fit
		hist = self.average_histogram()
		x, y = hist['grid'], hist['hist']
		##- define Gaussina function
		def std_gaussian(x, amp, miu, sigma):
			return amp * np.exp(-(x-miu)**2 / (2.*sigma**2))
		##--fitting
		params, params_covariance = curve_fit(std_gaussian, x, y)
		return params
	##-----


	def find_tail(self, tol=1e-4, gridSize=1e-6):
		hist = self.average_histogram()
		#-- interpolate xgrid (since X spacing in HISTO compute is large --> need to interpolate to have values at smaller interval)
		xp, yp = hist['grid'], hist['hist']
		if np.all(np.diff(xp) > 0):           # check if xp is increasing or not
			xInter = np.linspace( min(xp), max(xp), num=int( (max(xp)-min(xp))/gridSize) )
			yInter = np.interp(xInter, xp, yp)                                   

		#--find limits
		left_Index = np.where(yInter>tol )[0][0]        # find left_limit of the distribution tail
		right_Index = np.where(yInter>tol )[0][-1]       # find right_limit of the distribution tail
		#--
		left_tail = xInter[left_Index]
		right_tail = xInter[right_Index]
		#--
		return left_tail, right_tail
	##-----

	def find_center(self, gridSize=1e-6):
		hist = self.average_histogram()
		#-- interpolate xgrid (since X spacing in HISTO compute is large --> need to interpolate to have values at smaller interval)
		xp, yp = hist['grid'], hist['hist']
		if np.all(np.diff(xp) > 0):           # check if xp is increasing or not
			xInter = np.linspace( min(xp), max(xp), num=int( (max(xp)-min(xp))/gridSize) )
			yInter = np.interp(xInter, xp, yp)                                   

		#--find Max_value of Histogram
		center_Index = np.where(yInter==np.amax(yInter))[0][0]        # find index of max value
		#--
		Xcenter = xInter[center_Index]
		#--
		return Xcenter
	##-----

	## =========================================================================
	### Compute the probability density function (PDF) --> must input raw data, cannot compute from histogram
