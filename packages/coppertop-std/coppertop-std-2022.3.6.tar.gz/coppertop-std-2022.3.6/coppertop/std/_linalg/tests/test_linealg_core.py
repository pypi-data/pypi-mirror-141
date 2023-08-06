# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.pipe import *
from coppertop.testing import assertRaises
from coppertop.std.linalg import matrix, to, tvarray
from coppertop.std import check, shape, equal


def test():
    A = [[1, 2], [3, 5]] >> to(_, matrix[tvarray])
    b = [1, 2] >> to(_, matrix[tvarray])
    A @ b >> shape >> check >> equal >> (2,1)
    with assertRaises(Exception) as e:
        b @ A



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')




