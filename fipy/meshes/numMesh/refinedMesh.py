#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "refinedMesh.py"
 #                                    created: 11/10/03 {3:15:38 PM} 
 #                                last update: 7/29/04 {6:02:31 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
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

"""
The RefinedMesh class provides an alternative way to adapt a mesh without using the
AdaptiveMesh class. The RefinedMesh contructor takes as input an old mesh (baseMesh) as well as
a list of cells to refine (nodeList). The cells are refined by putting an additional vertex in the center of the cell
and dividng up the cell by drawing lines from the center to each vertex. After creating the new mesh, you can
convert variables to use the new mesh by creating a RefinedMeshCellVariable (defined in this module) with the
old variable and the new RefinedMesh as arguments. Note that if the mesh of the variable passed to RefinedMeshCellVariable
is not the same as the old mesh used to generate the RefinedMesh, the results will be erroneous.

NOTE: This currently only works with triangular meshes.

Test case:

   >>> baseMesh = Tri2D(dx = 6., dy = 6., nx = 1, ny = 1)
   >>> baseVar = CellVariable(value = [0., 1., 2., 3.], mesh = baseMesh)
   >>> refinedMesh = RefinedMesh2D(baseMesh, [1, 3])
   >>> refinedVar = RefinedMeshCellVariable(baseVar, refinedMesh)
   >>> print refinedMesh.getVertexCoords()
   [[ 0., 0.,]
    [ 6., 0.,]
    [ 0., 6.,]
    [ 6., 6.,]
    [ 3., 3.,]
    [ 3., 5.,]
    [ 3., 1.,]]
   >>> print refinedMesh.faceVertexIDs
   [[1,0,]
    [2,3,]
    [0,2,]
    [3,1,]
    [4,0,]
    [1,4,]
    [4,2,]
    [4,3,]
    [5,4,]
    [5,3,]
    [5,2,]
    [6,1,]
    [6,4,]
    [6,0,]]
   >>> print refinedMesh.cellFaceIDs
   [[ 3, 5, 7,]
    [ 2, 4, 6,]
    [ 6,10, 8,]
    [ 7, 8, 9,]
    [ 1, 9,10,]
    [ 0,13,11,]
    [ 5,11,12,]
    [ 4,12,13,]]
   >>> print Numeric.array(refinedVar)
   [ 0., 2., 1., 1., 1., 3., 3., 3.,]
   
"""

import Numeric
from fipy.variables.cellVariable import CellVariable
from fipy.meshes.numMesh.mesh2D import Mesh2D
from fipy.meshes.numMesh.tri2D import Tri2D

def listToString(list):
    res = str(list[0])
    for i in list[1:]:
        res = res + ' ' + str(i)
    return res

class RefinedMesh2D(Mesh2D):
    def __init__(self, baseMesh, nodeList):
        ## calculate new vertex coords
        baseNumVertices = baseMesh.getVertexCoords().shape[0]
        baseNumCells = baseMesh.getCellFaceIDs().shape[0]
        newNumVertices = baseNumVertices + len(nodeList)
        newVertexCoords = Numeric.concatenate((baseMesh.getVertexCoords(), Numeric.take(baseMesh.getCellCenters(), nodeList)))
        ## calculate new face vertex IDs
        cellVertexIDs = baseMesh.getOrderedCellVertexIDs()
        maxVerticesPerCell = cellVertexIDs.shape[1]
        refinedCellVertexIDs = Numeric.take(cellVertexIDs, nodeList)
        firstVerticesInAddedFaces = Numeric.repeat(Numeric.arange(baseNumVertices, newNumVertices), maxVerticesPerCell * Numeric.ones(len(nodeList)))
        secondVerticesInAddedFaces = Numeric.ravel(refinedCellVertexIDs)
        facesToAdd = Numeric.transpose([firstVerticesInAddedFaces, secondVerticesInAddedFaces])
        newFaceVertexIDs = Numeric.concatenate((baseMesh.faceVertexIDs, facesToAdd))
        ## calc face string to face IDs
        faceVertexToFaceIDs = {}
        currIndex = 0
        for i in newFaceVertexIDs:
            faceVertexToFaceIDs[listToString(Numeric.sort(i))] = currIndex
            currIndex = currIndex + 1
        ## calculate new cell face IDs
        cellIDsToKeep = Numeric.ones(baseNumCells)
        Numeric.put(cellIDsToKeep, nodeList, 0)
        cellFaceIDsToKeep = Numeric.compress(cellIDsToKeep, baseMesh.cellFaceIDs, 0)
        refinedCellFaceIDs = Numeric.take(baseMesh.cellFaceIDs, nodeList)
        middleIndex = baseNumVertices
        newCellFaceIDs = cellFaceIDsToKeep
        for i in refinedCellVertexIDs:
            outsideFaceVertexList = [[i[x], i[x+1]] for x in range(-1, len(i) - 1)]
            outsideFaceList = [faceVertexToFaceIDs[listToString(Numeric.sort(face))] for face in outsideFaceVertexList]
            rightFaceVertexList = [[middleIndex, i[x]] for x in range(-1, len(i) - 1)]
            rightFaceList = [faceVertexToFaceIDs[listToString(Numeric.sort(face))] for face in rightFaceVertexList]
            leftFaceVertexList = [[middleIndex, i[x+1]] for x in range(-1, len(i) - 1)]
            leftFaceList = [faceVertexToFaceIDs[listToString(Numeric.sort(face))] for face in leftFaceVertexList]
            faceArray = Numeric.transpose(Numeric.array([outsideFaceList, rightFaceList, leftFaceList]))
            newCellFaceIDs = Numeric.concatenate((newCellFaceIDs, faceArray))
            middleIndex = middleIndex + 1
        newNumCells = len(newCellFaceIDs)
        ## calculate newToOldCellIDs. Used for changing variables.
        self.newToOldCellIDs = Numeric.compress(cellIDsToKeep, Numeric.arange(baseNumCells))
        for i in nodeList:
            self.newToOldCellIDs = Numeric.concatenate((self.newToOldCellIDs, [i, i, i]))
        Mesh2D.__init__(self, newVertexCoords, newFaceVertexIDs, newCellFaceIDs)

class RefinedMeshCellVariable(CellVariable):
    def __init__(self, oldVar, newMesh):
        newValues = Numeric.take(Numeric.array(oldVar), newMesh.newToOldCellIDs)
        CellVariable.__init__(self, newMesh, name = oldVar.name, value = newValues, unit = oldVar.getUnit())

def _test():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    baseMesh = Tri2D(dx = 6., dy = 6., nx = 1, ny = 1)
    refinedMesh = RefinedMesh2D(baseMesh, [1, 3])
    _test()
