#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "fixedFlux.py"
 #                                    created: 11/15/03 {9:47:59 PM} 
 #                                last update: 11/21/04 {12:43:54 AM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #  Author: James Warren <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-15 JEG 1.0 original
 # ###################################################################
 ##

"""Fixed flux (Neumann) boundary condition
"""
__docformat__ = 'restructuredtext'

import Numeric

from fipy.boundaryConditions.boundaryCondition import BoundaryCondition
from fipy.boundaryConditions.fixedValue import FixedValue
from fipy.tools import vector

class FixedFlux(BoundaryCondition):
    def __init__(self,faces,value):
	BoundaryCondition.__init__(self,faces,value)
	N = len(self.faces)
	self.contribution = Numeric.zeros((N,),'d')
	# get units right
	self.contribution = self.contribution * self.value * self.faces[0].getArea()
	for i in range(N):
	    self.contribution[i] = self.value * self.faces[i].getArea()
	
    def buildMatrix(self, Ncells, MaxFaces, cell1dia, cell1off, coeffScale):
	"""Leave **L** unchanged and add gradient to **b**
	
	:Parameters:
	  - `Ncells`:   Size of **b**-vector
	  - `MaxFaces`: *unused*
	  - `cell1dia`: *unused*
	  - `cell1off`: *unused*
	  - `coeffScale`: dimensionality of the coefficient matrix
	"""
	bb = Numeric.zeros((Ncells,),'d')
	vector.putAdd(bb, self.adjacentCellIds, self.contribution / coeffScale)
	
	return (0, bb)
        
    def getDerivative(self, order):
	if order == 1:
	    return FixedValue(self.faces, self.value), None
	else:
	    return BoundaryCondition.getDerivative(self, order)


