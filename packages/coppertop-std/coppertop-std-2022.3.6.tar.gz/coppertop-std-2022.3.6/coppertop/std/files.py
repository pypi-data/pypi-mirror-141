# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import os, os.path, json
from io import TextIOWrapper
from coppertop.pipe import *
from bones.core.types import pystr, pylist
from coppertop.std.text import strip
from coppertop.std.transforming import each

getCwd = coppertop(style=unary1, newName='getCwd')(os.getcwd)
isFile = coppertop(style=unary1, newName='isFile')(os.path.isfile)
isDir = coppertop(style=unary1, newName='isDir')(os.path.isdir)
dirEntries = coppertop(style=unary1, newName='dirEntries')(os.listdir)

@coppertop(style=binary2)
def joinPath(a, b):
    return os.path.join(a, *(b if isinstance(b, (list, tuple)) else [b]))

@coppertop
def readlines(f:TextIOWrapper) -> pylist:
    return f.readlines()

@coppertop
def linesOf(pfn:pystr):
    with open(pfn) as f:
        return f >> readlines >> each >> strip(_,'\\n')

@coppertop(style=binary)
def copyTo(src, dest):
    raise NotImplementedError()

@coppertop
def readJson(pfn:pystr):
    with open(pfn) as f:
        return json.load(f)

@coppertop
def readJson(f:TextIOWrapper):
    return json.load(f)

