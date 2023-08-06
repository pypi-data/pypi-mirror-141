# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import builtins
from coppertop.pipe import *
from coppertop.pipe import typeOf
from bones.core.types import tv, T
from bones.core.metatypes import cacheAndUpdate, fitsWithin as _fitsWithin
from coppertop.std.transforming import inject
from coppertop.std.types import TBT


dict_keys = type({}.keys())
dict_values = type({}.values())



@coppertop
def box(v) -> TBT:
    return tv(TBT, v)

@coppertop
def box(v, t:T) -> T:
    return tv(t, v)

@coppertop
def getAttr(x, name):
    return getattr(x, name)

@coppertop
def compose(x, fs):
    return fs >> inject(_, x, _) >> (lambda x, f: f(x))

def not_(b):
    return False if b else True
Not = coppertop(style=unary1, newName='Not')(not_)
not_ = coppertop(style=unary1, newName='not_')(not_)

repr = coppertop(style=unary1, newName='repr')(builtins.repr)

@coppertop(style=unary1)
def _t(x):
    return x._t

@coppertop(style=unary1)
def _v(x):
    return x._v

@coppertop(style=binary2, supressDispatcherQuery=True)
def fitsWithin(a, b):
    doesFit, tByT, distances = cacheAndUpdate(_fitsWithin(a, b), {})
    return doesFit

@coppertop(style=binary2, supressDispatcherQuery=True)
def doesNotFitWithin(a, b):
    return a >> fitsWithin >> b >> not_


