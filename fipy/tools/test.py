#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "test.py"
 #                                    created: 11/10/03 {3:23:47 PM}
 #                                last update: 9/3/04 {10:41:39 PM} 
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
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

import unittest
import fipy.tests.testProgram
import tempfile
import fipy.tools.dump as dump
import fipy.tools.dimensions.physicalField
from fipy.meshes.grid2D import Grid2D
from fipy.models.phase.theta.modularVariable import ModularVariable

class TestDump(unittest.TestCase):
    def setUp(self, nx, ny):
        mesh = Grid2D(1.23, 4.5, nx, ny)
        theta = ModularVariable(
            mesh = mesh,
            value = 100.0)

        self.data = (theta, mesh)
        tempFile = tempfile.mktemp()
        dump.write(self.data, tempFile)
        self.dataUnpickled = dump.read(tempFile)

    def assertEqual(self, first, second, msg = None):
        if first == second:
            pass
        else:
            raise self.failureException, (msg or '\n%s\n!=\n%s' % (first, second))

    def testResult(self):
        self.assertEqual(self.data[0], self.dataUnpickled[1])
        self.assertEqual(self.data[1].getCellCenters(), self.dataUnpickled[1].getCellCenters())

class Test10by10(TestDump):
    def setUp(self):
        TestDump.setUp(self, 10, 10)

class Test50by50(TestDump):
    def setUp(self):
        TestDump.setUp(self, 50,50)

def suite():
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(Test10by10))
    theSuite.addTest(unittest.makeSuite(Test50by50))
    
    import doctest
    
    import sparseMatrix
    theSuite.addTest(doctest.DocTestSuite(sparseMatrix))
    import dimensions.physicalField
    theSuite.addTest(doctest.DocTestSuite(dimensions.physicalField))
    
    return theSuite
    
if __name__ == '__main__':
    fipy.tests.testProgram.main(defaultTest='suite')
