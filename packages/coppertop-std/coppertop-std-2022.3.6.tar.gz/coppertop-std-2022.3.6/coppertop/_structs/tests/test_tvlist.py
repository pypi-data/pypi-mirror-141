# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.pipe import typeOf
from coppertop.std.structs import tvseq
from coppertop.std import check, equal, append, join, _v
from bones.core.types import N, num


def test():
    fred = tvseq((N**num)[tvseq], [1, 2])
    fred >> _v >> check >> equal >> [1, 2]
    fred >> check >> typeOf >> (N**num)[tvseq]
    fred = fred >> append >> 3
    fred = fred >> join >> tvseq((N**num)[tvseq], [4, 5])
    fred >> _v >> check >> equal >> [1, 2, 3, 4, 5]
    print(repr(fred))
    print(str(fred))



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')
