from numpy import array

def RMSD(X, Y):
    from numpy import sqrt
    dist = pairwiseDistanceSquared(X, Y)
    # Minimum RMSD for each point in X
    min_rmsd = sqrt(dist.min(axis=1).mean())
    # Normalize for scale
    return min_rmsd / std(X)

def pairwiseDistanceSquared(X, Y):
    # R[i, j] = distance(X[i], Y[j]) ** 2
    return ((X[:, None, :] - Y[None, :, :]) ** 2).sum(axis=2)

def rotationMatrix(*angles):
    from numpy import eye, array
    from math import cos, sin

    if len(angles) == 1:
        theta, = angles
        R = eye(2) * cos(theta)
        R[1, 0] = sin(theta)
        R[0, 1] = -sin(theta)
    elif len(angles) == 2:
        theta, (x, y, z) = angles
        c = cos(theta)
        s = sin(theta)
        R = array([[c+x*x*(1-c),   x*y*(1-c)-z*s, (1-c)*x*z+y*s],
                   [y*x*(1-c)+z*s, c+y*y*(1-c),   y*z*(1-c)-x*s],
                   [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c)]])
    else:
        raise NotImplementedError("Only implemented for D in [2..3], not {}"
                                  .format(len(angles)))
    return R

def spacedRotations(D, N):
    from math import pi, sin, cos, sqrt
    from itertools import product as cartesian, repeat
    from .util import frange

    if D == 2:
        yield from zip(frange(-pi, pi, 2*pi/N))
    elif D == 3:
        # Ken Shoemake
        # Graphics Gems III, pp 124-132
        from .quaternion import Quaternion
        for X, *theta in cartesian(frange(0, 1, 1/N), *repeat(frange(0, 2*pi, 2*pi/N), 2)):
            R = (sqrt(1-X), sqrt(X))
            yield Quaternion(sin(theta[0]) * R[0], cos(theta[0]) * R[0],
                             sin(theta[1]) * R[1], cos(theta[1]) * R[1]).axis_angle
    else:
        raise NotImplementedError("Only defined for D in [2..3], not {}"
                                  .format(D))
# For spaced points on a sphere, see Saff & Kuijlaars,
# The Mathematical Intelligencer Winter 1997, Volume 19, Issue 1, pp 5-11

def randomRotations(D):
    from math import pi, sin, cos, sqrt
    from random import uniform
    from itertools import product as cartesian, repeat
    from .util import frange

    if D == 2:
        while True:
            yield (uniform(-pi, pi),)
    elif D == 3:
        # Ken Shoemake
        # Graphics Gems III, pp 124-132
        from .quaternion import Quaternion
        while True:
            X = uniform(0, 1)
            theta = uniform(0, 2*pi), uniform(0, 2*pi)
            R = (sqrt(1-X), sqrt(X))
            yield Quaternion(sin(theta[0]) * R[0], cos(theta[0]) * R[0],
                             sin(theta[1]) * R[1], cos(theta[1]) * R[1]).axis_angle
    else:
        raise NotImplementedError("Only defined for D in [2..3], not {}"
                                  .format(D))

def std(x):
    from numpy import var, sqrt
    return sqrt(var(x, axis=0).mean())

def rigidXform(X, R=array(1), t=0.0, s=1.0):
    return s * R.dot(X.T).T + t

def affineXform(X, B=array(1), t=0):
    return B.dot(X.T).T + t
