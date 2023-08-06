# import numpy as np

### From this site: https://www.unitconverters.net/force-converter.html
def pressure(key_word='mykey'):
	"""convert unit of pressure
	Pa: Pascal
	atm: standard atmosphere
	at: technical atmosphere

	kgf/cm2 = kg/cm2
	1 Pa = 1 N/m^2
	1 kgf/cm2 = 1    

	* Input:
		- key_word='mykey'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:    
		factor: float, multiply factor of conversion """

	D = {'Pa_atm':0.0000098692, 'Pa_bar':0.00001, 'Pa_mmHg':0.0075006376,
			 'Pa_N/m2':1, 'Pa_kgf/m2':0.1019716213, 'Pa_kgf/cm2':0.0000101972 }
	##
	if key_word=='mykey': 
		return D.keys()
	else:
		return D[key_word]
#######


def force(key_word='mykey'):
	"""convert unit of force
	N: Newton
	kgf = m.g: kilogram-force (weight: one kilogram of mass in a 9.80665 m/s2 gravitational field)
	lbf: pound-force
	p: pond

	1 N = 1 J/m    (Work = Force.distance) 
	1 kcal = 4184 J = 4184 N.m = 4184.10^10 N.Angstrom
	69.4786 pN = 1 kcal/mol Angstrom.     https://tinyurl.com/yb2gnlhc

	* Input:
		- key_word='mykey'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:    
		factor: float, multiply factor of conversion """

	D = {'N_J/m':1, 'N_kgf':0.1019716213, 'N_lbf':0.2248089431, 'N_p':101.9716213,
	     'N_cal/m':0.2390057361, 'N_cal/A':0.2390057361e-10, 'N_kcal/A':0.2390057361e-13,
		 'N_kcal/(mol.A)':1.4393261854684511e10}
	##
	if key_word=='mykey': 
		return D.keys()
	else:
		return D[key_word]
#######

def energy(key_word='mykey'):
	"""convert unit of energy
	J: Joule 
	W.h: watt-hour
	cal: calorie (th)
	hp.h: horsepower hour
	eV: electron-volt

	1 J = 1 N.m    (Work = Force.distance) 
	1J = 1 W.s

	* Input:
		- key_word='mykey'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:    
		factor: float, multiply factor of conversion """

	D = {'J_cal':0.2390057361, 'J_W.h':0.0002777778, 'J_hp.h':3.725061361E-7, 'J_eV':6.241509e18,
	     'J_erg':1e7, 'J_W.s':1, 'J_N.m':1,
		 'J_J/mol': 1.66054e-24}
	##
	if key_word=='mykey': 
		return D.keys()
	else:
		return D[key_word]
#######

def constant(key_word='mykey'):
	"""list of constants
	Na = 6.02214076e23  (1/mol): Avogadro number

	* Input:
		- key_word='mykey'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:    
		factor: float, multiply factor of conversion """

	D = {'Avogadro':6.02214076e23, 
		}
	##
	if key_word=='mykey': 
		return D.keys()
	else:
		return D[key_word]
#######