# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from bones.core.types import pystr, pybool

dict_keys = type({}.keys())
dict_values = type({}.values())
ellipsis = type(...)
function = type(lambda x:x)



# **********************************************************************************************************************
# endsWith
# **********************************************************************************************************************

@coppertop(style=binary2)
def endsWith(s1:pystr, s2:pystr) -> pybool:
    return s1.endswith(s2)


# **********************************************************************************************************************
# startsWith
# **********************************************************************************************************************

@coppertop(style=binary2)
def startsWith(s1:pystr, s2:pystr) -> pybool:
    return s1.startswith(s2)

