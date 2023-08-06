from ..utils.coord_rotation      import CoordTransform
from ..utils.compute_distance    import dist2_node2nodes
from ..modeling.box_orientation  import box_orientation
import numpy as np


## 2. FCC CUBIC harmonic
def FCCcubic(points, **kwargs):
    """Function to Calculate Order Parameter with multi_vectors K
    * Compulsory Inputs:
            points   : Nx3 Matrix contain bonding vectors between neighboring  atoms j and ref atom i
    ** optional Inputs:
            switch_function=[1,1...,1] : Nx1 array, contain values of switching function s(Rj) (Rj is positions of atom j)
            alpha=27      : scalar, coefficient of harmonic function
            zDirect='001'  : string, '001'  '110'  '111'
    * Output:       
            LC  : scalar, Order Parameter
        Example: S = thaTool.OrderPara.FCCcubic([1,0,0; 0,1,0], SW=sw)
    By Cao Thang, Mar 2020
    NOTE: Require to best chose Rcut for Switching function
    """
    ##==== compulsory Inputs 
    P = np.asarray(points)	
    
    ##==== optional Inputs 
    if 'switch_function' in kwargs: 
        sw = kwargs['switch_function']
        Rij = dist2_node2nodes([0,0,0], P)   
        mySW,_ = sw.Evaluate(Rij['bond_len'])
    else: mySW = np.ones(P.shape[0]) 

    if 'alpha' in kwargs: alpha = np.asarray(kwargs['alpha'])
    else: alpha = 27
    #--
    if 'zDirect' in kwargs: 
        zDirect = kwargs['zDirect']
        newAxis,_ = box_orientation(zDirect=zDirect)
        # Rotate P  --> rotate after find neighbor
        oldAxis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        BT = CoordTransform(old_orient=newAxis, new_orient=oldAxis)          # reverse rotate
        P = BT.rotate_3d(P)

    ##==== Compute FCC CUBIC Parameter
    x = P[:,0];     y = P[:,1];    z = P[:,2]
    Rij = dist2_node2nodes((0,0,0), P)
    r = Rij['bond_len']
    #--
    Ca = ( (x*y)**4 + (y*z)**4 + (z*x)**4 )/r**8 - alpha*((x*y*z)**4) /r**12
    a = 80080.0/(2717.0+16*alpha)
    b = 16.0*(alpha-143)/(2717.0+16*alpha)
    phi = (a*Ca + b)
    #--
    FCCcubic = sum(mySW*phi)/ sum(mySW)        # Sum over all atoms, Order_Parameter 
    # --  
    return  FCCcubic  
##--------
 
 	

