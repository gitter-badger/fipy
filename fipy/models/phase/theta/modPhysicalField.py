#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "modPhysicalField.py"
 #                                    created: 12/28/03 {10:56:55 PM} 
 #                                last update: 9/3/04 {10:35:55 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
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
 # Physical fields or quantities with units
 #
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-12-28 JEG 1.0 original
 # ###################################################################
 ##

from fipy.tools.dimensions.physicalField import PhysicalField

import Numeric

class ModPhysicalField(PhysicalField):

    def mod(self, argument):
        return Numeric.fmod(argument + 3. * Numeric.pi, 2. * Numeric.pi) - Numeric.pi

    def __sub__(self, other):
        if isinstance(other, ModPhysicalField):
            return self.__class__(value = self.mod(self.value - other.value), unit = self.unit)
        else:
            return self._sum(other, sign2 = lambda b: -b)
    
    def __rsub__(self, other):
        if isinstance(other, ModPhysicalField):
            return self.__class__(value = self.mod(argument = other.value - self.value), unit = self.unit)
        else:
            return self._sum(other, sign1 = lambda a: -a)
