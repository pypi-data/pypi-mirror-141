# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

import numpy
from coppertop.pipe import *
from coppertop.std.types import adhoc, right, orth
from coppertop.std._linalg.core import matrix, tvarray

_matrix = matrix[tvarray]

@coppertop(style=unary1)
def QR(A:_matrix) -> adhoc:
    Q, R = numpy.linalg.qr(A)
    return adhoc(Q=_matrix(Q) | +orth, R=_matrix(R) | +right)

@coppertop(style=unary1)
def Cholesky(A:_matrix) -> _matrix&right:
    return _matrix(numpy.linalg.cholesky(A)) | +right
