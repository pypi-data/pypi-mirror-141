# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.std.examples.misc import Fred
from coppertop.pipe import _
from coppertop.std import assertEquals, to, stdout

def test_repr_or_str():
    [Fred(1)] >> to(_, str) >> assertEquals >> '[rep(1)]'


def main():
    test_repr_or_str()


if __name__ == '__main__':
    main()
    stdout << 'pass\n'

