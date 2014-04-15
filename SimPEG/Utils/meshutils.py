import numpy as np
from scipy import sparse as sp
from matutils import mkvc, ndgrid, sub2ind, sdiag

def exampleLrmGrid(nC, exType):
    assert type(nC) == list, "nC must be a list containing the number of nodes"
    assert len(nC) == 2 or len(nC) == 3, "nC must either two or three dimensions"
    exType = exType.lower()

    possibleTypes = ['rect', 'rotate']
    assert exType in possibleTypes, "Not a possible example type."

    if exType == 'rect':
        return list(ndgrid([np.cumsum(np.r_[0, np.ones(nx)/nx]) for nx in nC], vector=False))
    elif exType == 'rotate':
        if len(nC) == 2:
            X, Y = ndgrid([np.cumsum(np.r_[0, np.ones(nx)/nx]) for nx in nC], vector=False)
            amt = 0.5-np.sqrt((X - 0.5)**2 + (Y - 0.5)**2)
            amt[amt < 0] = 0
            return [X + (-(Y - 0.5))*amt, Y + (+(X - 0.5))*amt]
        elif len(nC) == 3:
            X, Y, Z = ndgrid([np.cumsum(np.r_[0, np.ones(nx)/nx]) for nx in nC], vector=False)
            amt = 0.5-np.sqrt((X - 0.5)**2 + (Y - 0.5)**2 + (Z - 0.5)**2)
            amt[amt < 0] = 0
            return [X + (-(Y - 0.5))*amt, Y + (-(Z - 0.5))*amt, Z + (-(X - 0.5))*amt]


def meshTensors(*args):
    """
        **meshTensors** takes any number of tuples that have the form::

            mT = ( (numPad, sizeStart [, increaseFactor]), (numCore, sizeCore), (numPad, sizeStart [, increaseFactor]) )

        .. note::

            The increaseFactor is an optional input.


        .. plot::

            from SimPEG import Mesh, Utils
            M = Mesh.TensorMesh(Utils.meshTensors(((10,10),(40,10),(10,10)), ((10,10),(20,10),(0,0))))
            M.plotGrid()

    """
    def padding(num, start, factor=1.3, reverse=False):
        pad = ((np.ones(num)*factor)**np.arange(num))*start
        if reverse: pad = pad[::-1]
        return pad
    tensors = tuple()
    for i, arg in enumerate(args):
        tensors += (np.r_[padding(*arg[0],reverse=True),np.ones(arg[1][0])*arg[1][1],padding(*arg[2])],)

    return list(tensors) if len(tensors) > 1 else tensors[0]

def points2nodes(mesh, pts):
    """
        Move a list of the nearest nodes to a set of points

        :param simpeg.Mesh.TensorMesh mesh: The mesh
        :param numpy.ndarray pts: Points to move}
        :rtype: numpy.ndarray
        :return: nodeInds
    """

    pts = np.atleast_2d(pts)

    assert mesh._meshType in ['TENSOR', 'CYL']
    assert pts.shape[1] == mesh.dim

    nodeInds = np.empty(pts.shape[0], dtype=int)

    for i, pt in enumerate(pts):
        nodeInds[i] = ((np.tile(pt, (mesh.gridN.shape[0],1)) - mesh.gridN)**2).sum(axis=1).argmin()

    return nodeInds



if __name__ == '__main__':
    from SimPEG import Mesh
    import matplotlib.pyplot as plt
    M = Mesh.TensorMesh(meshTensors(((10,10),(40,10),(10,10)), ((10,10),(20,10),(0,0))))
    M.plotGrid()
    plt.gca().axis('tight')
    plt.show()