# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2020 David Briant
#
# **********************************************************************************************************************

from coppertop.std import check, equal
from coppertop.std.range import each_, rChain
from coppertop.std.range import IndexableFR, ListOR, getIRIter, materialise


def test_listRanges():
    r = IndexableFR([1,2,3])
    o = ListOR([])
    while not r.empty:
        o.put(r.front)
        r.popFront()
    r.indexable >> check >> equal >> o.list

def test_rangeOrRanges():
    rOfR = [] >> rChain
    [e for e in rOfR >> getIRIter] >> check >> equal >> []
    rOfR = (IndexableFR([]), IndexableFR([])) >> rChain
    [e for e in rOfR >> getIRIter] >> check >> equal >> []
    rOfR = (IndexableFR([1]), IndexableFR([2])) >> rChain
    [e for e in rOfR >> getIRIter] >> check >> equal >> [1,2]

def test_other():
    [1, 2, 3] >> each_ >> (lambda x: x) >> materialise >> check >> equal >> [1, 2, 3]

def test_take():
    r1 = IndexableFR([1,2,3])
    r2 = r1 >> take >> 3
    r1.popFront >> check >> equal >> 1
    r3 = r1 >> take >> 4
    r2 >> materialise >> check >> equal >> [1,2,3]
    r3 >> materialise >> check >> equal >> [2,3]


def main():
    test_listRanges()
    test_rangeOrRanges()
    # test_other()
    # test_take()


if __name__ == '__main__':
    main()
    print('pass')


