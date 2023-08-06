# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

import math, numpy
from coppertop.pipe import *
from coppertop.std.linalg import tvarray


@coppertop
def cov(A:tvarray) -> tvarray:
    return numpy.cov(A).view(tvarray)

@coppertop
def mean(ndOrPy):
    # should do full numpy?
    return numpy.mean(ndOrPy)

@coppertop
def std(ndOrPy, dof=0):
    # should do full numpy? std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=<no value>)
    return numpy.std(ndOrPy, dof)

@coppertop
def logisticCDF(x, mu, s):
    return 1 / (1 + math.exp(-1 * (x - mu) / s))

@coppertop
def logisticCDFInv(p, mu, s):
    return mu + -s * math.log(1 / p - 1)
