# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.pipe import *
from coppertop.core import NotYetImplemented
from coppertop.std.structs import tvstruct
from bones.core.types import pydict, pylist, pyfunc
from coppertop.std.types import adhoc




# **********************************************************************************************************************
# sort
# **********************************************************************************************************************

@coppertop(style=unary1)
def sort(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:tvstruct) -> tvstruct:
    return tvstruct(sorted(x._nvs(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:adhoc) -> adhoc:
    return adhoc(sorted(x._nvs(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:pylist) -> pylist:
    return sorted(x, key=None, reverse=False)


# **********************************************************************************************************************
# sortBy
# **********************************************************************************************************************

@coppertop
def sortBy(agg, names):
    raise NotYetImplemented()

@coppertop
def sortBy(agg, names, directions):
    raise NotYetImplemented()


# **********************************************************************************************************************
# sortRev
# **********************************************************************************************************************

@coppertop(style=unary1)
def sortRev(x:pylist) -> pylist:
    return sorted(x, key=None, reverse=True)

@coppertop(style=unary1)
def sortRev(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=True))


# **********************************************************************************************************************
# sortRevUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def sortRevUsing(x:pylist, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=True)

@coppertop(style=binary2)
def sortRevUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=True))


# **********************************************************************************************************************
# sortUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def sortUsing(x:pylist, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=False)

@coppertop(style=binary2)
def sortUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=False))

@coppertop(style=binary)
def sortUsing(soa, f):
    raise NotYetImplemented()

