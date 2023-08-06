# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.std.structs import tvstruct
from bones.core.types import pystr, pyint


def test():
    fred = tvstruct(pystr**(pystr*pyint), [[1,2]])
    fred.a = 1
    fred.b = 2
    print(fred['a'])
    fred['a'] = 5
    fred._fred = 1
    fred = fred | pystr**(pystr*pyint)
    print(fred._fred)
    print(repr(fred))
    print(str(fred))
    for k, v in fred._nvs():
        print(k, v)



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')
