#!/usr/bin/env python

## 
 # -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "substitutionalEquation.py"
 #                                    created: 11/12/03 {10:39:23 AM} 
 #                                last update: 9/3/04 {10:38:55 PM} 
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
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

from concentrationEquation import ConcentrationEquation

class SubstitutionalEquation(ConcentrationEquation):
    def getConvectionCoeff(self, Cj, fields, relaxation, diffusivity = None):
	Cj.substitutionalSum = Cj.copy()
        Cj.substitutionalSum.setValue(0)

	for component in [component for component in fields['substitutionals'] if component is not Cj]:
	    Cj.substitutionalSum = Cj.substitutionalSum + component

	denom = 1. - Cj.substitutionalSum.getHarmonicFaceValue()
	if diffusivity is None:
	    diffusivity = Cj.getDiffusivity()
	    
	Cj.subsConvCoeff = diffusivity * Cj.substitutionalSum.getFaceGrad() / denom.transpose()
	Cj.weightedDiffusivity = (diffusivity * fields['solvent'].getHarmonicFaceValue() / denom).transpose()

## 	return 0

	return  self.phaseRelaxation * (Cj.subsConvCoeff + ConcentrationEquation.getConvectionCoeff(self, Cj = Cj, fields = fields, diffusivity = Cj.weightedDiffusivity))
	

