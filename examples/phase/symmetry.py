#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
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
 # ###################################################################
 ##

r"""

This example creates four symmetric quadrilateral regions in a box.
We start with a :class:`CellVariable` object that contains the following
values:

.. math::

   \phi(x, y) = x y, 
   0 \le x \le L,
   0 \le y \le L

We wish to create 4 symmetric regions such that

.. math::

   \phi(x, y) = \phi(L - x, y) = \phi(L - x, y) = \phi(L - x, L - y),
   0 \le x \le L / 2,
   0 \le y \le L / 2
    
We create a square domain

>>> from fipy import *

>>> N = 20
>>> L = 1.
>>> dx = L / N
>>> dy = L / N

>>> mesh = Grid2D(
...    dx = dx,
...    dy = dy,
...    nx = N,
...    ny = N)

>>> var = CellVariable(name = "test", mesh = mesh)
  
First set the values as given in the above equation:

>>> x, y = mesh.getCellCenters()
>>> var.setValue(x * y)

>>> if __name__ == '__main__':
...     viewer = Viewer(vars=var, datamin=0, datamax=L * L / 4.)
...     viewer.plot()

then extract the bottom left quadrant of cells:

>>> bottomLeftCells = mesh.getCells()[(x < L / 2.) & (y < L / 2.)]
>>> bottomRightCells = ()
>>> topLeftCells = ()
>>> topRightCells = ()

Next, extract the corresponding cells from each region in the correct order:

>>> for cell in bottomLeftCells:
...     x, y = cell.getCenter()
...     bottomRightCells += (mesh.getNearestCell(((L - x,), (y,))),)            
...     topRightCells += (mesh.getNearestCell(((L - x,), (L - y,))),)
...     topLeftCells += (mesh.getNearestCell(((x,), (L - y,))),)

The method `1mesh.getNearestCell((x, y))`` finds the nearest cell to
the given coordinate. The cells are then set to the symmetry value:

>>> orderedCells = (bottomRightCells, topRightCells, topLeftCells)
>>> symmetryCells = bottomLeftCells
>>> for cellSet in orderedCells:
...     for i in range(len(cellSet)):
...         id = symmetryCells[i].getID()
...         idOther = cellSet[i].getID()
...         var[idOther] = var[id]


>>> if __name__ == '__main__':
...     viewer.plot()

The following code tests the results with a different algorithm:

>>> testResult = zeros((N / 2, N / 2), 'd')
>>> bottomRight = zeros((N / 2, N / 2), 'd')
>>> topLeft = zeros((N / 2, N / 2), 'd')
>>> topRight = zeros((N / 2, N / 2), 'd')
>>> for j in range(N / 2):
...     for i in range(N / 2):
...         x = dx * (i + 0.5)
...         y = dx * (j + 0.5)
...         testResult[i, j] = x * y
...         bottomRight[i,j] = var(((L - x,), (y,)))
...         topLeft[i,j] = var(((x,), (L - y,)))
...         topRight[i,j] = var(((L - x,), (L - y,)))
>>> allclose(testResult, bottomRight, atol = 1e-10)
1
>>> allclose(testResult,topLeft, atol = 1e-10)
1
>>> allclose(testResult,topRight, atol = 1e-10)
1
"""
__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
    raw_input("finished")

    



