# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.pipe import *
from coppertop.core import NotYetImplemented



# see https://code.kx.com/q/basics/funsql/

@coppertop(style=unary)
def fromselect(listr, defs, byNames, wherePreds):
    raise NotYetImplemented()


@coppertop(style=unary)
def fromreject(listr, wherePreds):
    raise NotYetImplemented()


@coppertop(style=unary)
def fromupdate(defs, byNames, agg, wherePreds):
    raise NotYetImplemented()



def sequenceBreaks(soa, names):
    '''answers a new list with each difference item e.g. hello -> h, e, l, o'''
    raise NotYetImplemented()


def isequenceBreaks(soa, names):
    '''as above but also includes the index of the break'''
    raise NotYetImplemented()


