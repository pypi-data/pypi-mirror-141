
# import numpy as np



### ============================================================================
### Define CONSTANT
### ============================================================================
## atomic mass
""" atomic_mass in in [g/mol], (1u = 1g/mol = 1.66053904 × 10-27 kg = 1mu)
	Ref atomic mass here: https://tinyurl.com/yzv2namz """
	
ATOMIC_MASS = {
	'H':1.00797, 'He':4.00260, 'Li':6.941, 'Be':9.012183, 'B':10.81, 'C':12.011, 'N':14.0067, 'O':15.9994, 'F':18.998403, 'Ne':20.179, 
	'Na':22.989769, 'Mg':24.305, 'Al':26.98154, 'Si':28.0855, 'P':30.97376, 'S':32.06, 'Cl':35.453, 'Ar':39.948, 'K':39.0983, 'Ca':40.08,
	'Sc':44.9559, 'Ti':47.90, 'V':50.9415, 'Cr':51.996, 'Mn':54.93804, 'Fe':55.847, 'Co':58.9332, 'Ni':58.70, 'Cu':63.546, 'Zn':65.38, 
	'Ga':69.72, 'Ge': 72.59, 'As': 74.9216, 'Se': 78.96, 'Br': 79.904, 'Kr': 83.80, 'Rb': 85.467, 'Sr': 87.6, 'Y': 88.9058, 'Zr': 91.22,
	'Nb': 92.9063, 'Mo': 95.9, 'Ru': 101.0, 'Rh': 102.9055, 'Pd': 106.4, 'Ag': 107.868, 'Cd': 112.41, 'In': 114.81, 'Sn': 118.71, 'Sb': 121.76,
	'Te': 127.6, 'I': 126.9044, 'Xe': 131.29, 'Cs': 132.9054519, 'Ba': 137.32, 'La': 138.9054, 'Ce': 140.11, 'Pr': 140.9076, 'Nd': 144.24, 'Sm': 150.3,
	'Eu': 151.96, 'Gd': 157.2, 'Tb': 158.9253, 'Dy': 162.50, 'Ho': 164.9303, 'Er': 167.25, 'Tm': 168.9342, 'Yb': 173.05, 'Lu': 174.966, 'Hf': 178.4,
	'Ta': 180.9478, 'W': 183.8, 'Re': 186.20, 'Os': 190.2, 'Ir': 192.21, 'Pt': 195.08, 'Au': 196.96656, 'Hg': 200.59, 'Tl': 204.3, 'Pb': 207.0,
	'Bi': 208.9804 
}



### ============================================================================
### Matplot Parameter for Plot
### ============================================================================
""" This class contains some Global parameters to set for Matplotlib 
to see all valid Params:
		import matplotlib as mpl
		mpl.rcParams.keys() 
##--
Use: plt.rcParams.update(gridParam)
https://matplotlib.org/tutorials/introductory/customizing.html
fontsize for legend, stick,...not for text: fontsize : int or float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', 'larger', 'smaller'}
'smaller'= 83%% of the current font size.
### use latex: https://matplotlib.org/stable/tutorials/text/usetex.html
font.family: 'san-serif' 'serif' or 'monospace'
### font family: https://tinyurl.com/ygestjxo
	- 'serif': Serifs are small decorative flourishes attached to stroke ends of characters. Fonts such as Times New Roman, Century, Garamond, and Palatino are serif fonts.
	- 'sans-serif': This means without serif. Fonts such as Helvetica, Arial, Calibri, and DejaVu Sans are sans-serif.
	- 'monospace': Monospace fonts have characters of the same width. They are usually used for code.
	- 'cursive': Cursive features connected brush strokes, usually in italic, that give a sense of classical elegance.
	- 'fantasy': Decorative fonts that look funny.
### Math mode: https://tinyurl.com/yjttcr2c
	#mathtext.fontset: dejavusans  # Should be 'dejavusans' (default), 'dejavuserif', 'cm' (Computer Modern), 'stix',
									# 'stixsans' or 'custom' (unsupported, may go away in the future)
	## "mathtext.fontset: 'custom" is defined by the mathtext.bf, .cal, .it, ...
	## settings which map a TeX font name to a fontconfig font pattern.  (These settings are not used for other font sets.)
	#mathtext.bf:  sans:bold
	#mathtext.cal: cursive
	#mathtext.it:  sans:italic
	#mathtext.rm:  sans
	#mathtext.sf:  sans
	#mathtext.tt:  monospace
	#mathtext.fallback: cm  # Select fallback font from ['cm' (Computer Modern), 'stix'
							# 'stixsans'] when a symbol can not be found in one of the
							# custom math fonts. Select 'None' to not perform fallback
							# and replace the missing character by a dummy symbol.
	#mathtext.default: it 
"""   
myPLOT_PARAM = {                             # define a DICT
	### Set global font
	"font.family":'sans-serif', 'font.sans-serif':'Tahoma',              # 'sans-serif' family of Arial font: Arial, Tahoma, Courier New, Comic Sans MS,Segoe UI,Lucida Console
	# "font.family":'serif', 'font.serif': ['Times New Roman'],          # "serif" family of Times font: Times New Roman, 

	### Math mode
	# 'text.usetex':True,                                                # use latex
	# 'mathtext.fontset':'custom', 'mathtext.sf':'sans',                    # use Mathtext
	
	### Set fontsize
	'font.size':10,
	'legend.fontsize':'smaller', 
	'axes.labelsize': 'medium', 'axes.titlesize':'medium', "figure.titlesize":'larger',
	'xtick.labelsize':'medium', 'ytick.labelsize':'medium',
	### Change the appearance of ticks, tick labels, and gridlines: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.axes.Axes.tick_params.html
	'axes.grid':True, 'axes.grid.axis':'both', 'axes.grid.which': 'major',
	'grid.linestyle': (5, 10), 'grid.linewidth':0.4, 'grid.color':'gray',           # 'grid.linestyle': (0, (5, 10))
	'xtick.direction':'in', 'xtick.major.size': 3.5, 'xtick.major.width': 0.7,
	'ytick.direction':'in', 'ytick.major.size': 3.5, 'ytick.major.width': 0.7,
	### Legend
	'legend.frameon':True,
	### Figure size
	'figure.figsize': [3.375, 2.7], 'figure.dpi': 130.0, 
	'savefig.dpi': 'figure', 'savefig.pad_inches': 0.05,

	### color
	# 'axes.prop_cycle': cycler('color', ['black','red','blue','green','magenta','lime','orange','cyan','violet','purple','olive','gray','yellow','navy',
	#                                     'saddlebrown','darkgreen','lawngreen','skyplue', 'lightgreen','steelblue','lategray']),
}


myPLOT_COLOR = ['black','red','blue','green','magenta','orange','lime','cyan','violet','purple','olive','gray','yellow','navy','saddlebrown','darkgreen','lawngreen', 'lightgreen','steelblue','darkcyan','plum','slateblue','indigo']

myPLOT_MARKER=['^','d','H','X','o','s']			
	
### ======================= End function =======================================




		








