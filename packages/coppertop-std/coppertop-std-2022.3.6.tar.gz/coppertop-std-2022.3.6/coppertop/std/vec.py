# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

# vector operations

import numpy
import datetime

from coppertop.pipe import *
from coppertop.std.linalg import tvarray
from coppertop.std.datetime import parseDate, toCTimeFormat
from bones.core.types import pystr, pyfloat, pydate, pylist


@coppertop
def diff(v:tvarray) -> tvarray:
    return numpy.diff(v)

@coppertop
def log(v:tvarray) -> tvarray:
    return numpy.log(v)

def parseNum(x:pystr) -> pyfloat:
    try:
        return float(x)
    except:
        return numpy.nan

@coppertop
def to(xs:pylist, t:pyfloat) -> tvarray:
    return tvarray([parseNum(x) for x in xs])

@coppertop
def to(xs:pylist, t:pydate, f:pystr) -> tvarray:
    cFormat = toCTimeFormat(f)
    return tvarray([parseDate(x, cFormat) for x in xs])
