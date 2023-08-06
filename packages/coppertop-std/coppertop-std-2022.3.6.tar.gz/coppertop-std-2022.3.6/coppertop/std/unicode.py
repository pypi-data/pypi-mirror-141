# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.pipe import *


@coppertop
def decode(b, encoding):
    return b.decode(encoding)

@coppertop
def encode(s, encoding):
    return s.encode(encoding)

