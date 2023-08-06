from math import sqrt

def mixing_rule_LJ(df1, df2, mix_rule='Lorentz_Berthelot', pair_style='lj/cut'): 
	""" compute parameters (epsilon & sigma) of LJ potential at interface
	Note that in LAMMPS: 'Lorentz_Berthelot'='arithmetic'   https://tinyurl.com/yzpwg2hs
	* Input:
		- df1, df2: pandas DataFrames contain sig & eps of each element of 2 surfaces
        - mix_rule='arithmetic' (also 'Lorentz_Berthelot')
			+ 'arithmetic'/'Lorentz_Berthelot'
			+ 'geometric'
			+ 'sixthpower'
	* Return: 
		- list-of-string: contain pair_coeffs for LAMMPS

	* NOTEs: 
		- energy unit is kcal/mol, but in Foyer is kJ/mol.
		- df1['type'] must < df2['type']
	
	Ex:	PMMA/h_BN interface
	dict1 = {'element':['CT','CT','CT','CT','HC','HC','C_2','O_2','OS','CT','HC'], 
         'name':['opls_135','opls_136','opls_137','opls_139','opls_140','opls_282','opls_465','opls_466','opls_467','opls_468','opls_469'],
         'type':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
         'sigma': [3.5, 3.5, 3.5, 3.5, 2.5, 2.42, 3.75, 2.96, 3.0, 3.5, 2.42], 
         'epsilon':[0.066, 0.066, 0.066, 0.066, 0.03, 0.015, 0.105, 0.21, 0.17, 0.066, 0.015]}
	
	dict2 = {'element':['B','N'], 
			'name':['B','N'],
			'type':[12,13], 
			'sigma': [3.453, 3.365], 
			'epsilon':[0.094988, 0.1448671]}
	df1 = pd.DataFrame(dict1)
	df2 = pd.DataFrame(dict2)
    """
	### input 
	df1.sort_values(['type'], inplace=True)
	df2.sort_values(['type'], inplace=True)
	##
	L = []
	for i,row1 in df1.iterrows():
		for j,row2 in df2.iterrows():
			type1,type2 = row1['type'], row2['type']
			eps1,eps2   = row1['epsilon'], row2['epsilon']
			sig1,sig2   = row1['sigma'], row2['sigma']
			name1,name2 = row1['name'], row2['name']
			if type1<=type2:
				if mix_rule=='Lorentz_Berthelot' or mix_rule=='arithmetic':
					eps,sig = Lorentz(eps1, eps2, sig1, sig2)
				elif mix_rule=='geometric':
					eps,sig = geometric(eps1, eps2, sig1, sig2)
				elif mix_rule=='sixthpower':
					eps,sig = sixthpower(eps1, eps2, sig1, sig2)
				else: raise Exception('mixing rule is not available. Please choose one of: "Lorentz–Berthelot"/"geometric"/"sixthpower"')

				L.append('pair_coeff  %i \t%i \t%s  %.6f %.6f \t\t# %s %s' % (type1, type2, pair_style, eps, sig, name1, name2) )
	##
	return L


### define mixing rule
def Lorentz(eps1, eps2, sig1, sig2):
    eps12 = sqrt(eps1 * eps2)
    sig12 = (sig1 + sig2)/2
    return eps12, sig12

def geometric(eps1, eps2, sig1, sig2):
    eps12 = sqrt(eps1 * eps2)
    sig12 = sqrt(sig1 * sig2)
    return eps12, sig12

def sixthpower(eps1, eps2, sig1, sig2):
    eps12 = (2*sqrt(eps1*eps2) *pow(sig1,3) *pow(sig2,3)) /(pow(sig1,6) + pow(sig2,6)) 
    sig12 = pow((pow(sig1,6) + pow(sig2,6))/2, 1/6)
    return eps12, sig12
