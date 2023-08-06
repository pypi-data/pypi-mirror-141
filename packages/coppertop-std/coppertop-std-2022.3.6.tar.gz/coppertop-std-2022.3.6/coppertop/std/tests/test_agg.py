# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# **********************************************************************************************************************




from coppertop.std import select, update, delete, sortBy, agg


def test():
    agg = []
    agg2 = select(["a", ], [], agg, [])
    agg3 = update([["a", lambda x: x]], [], agg2, [])
    agg3 = delete(agg3, [])

def test2():
    a = agg(a=[1,2,1,2,1,2],b=[2,2,2,1,1,1],c=['a','b','c','d','e','f'])
    r = a >> sortBy >> ['b', 'a']

def test_groupBy():
    a = freds \
        >> chunkBy('a') \
        >> map >> (lambda g: tvstruct(
            b=g >> first >> at(_, 'b'),
            a=g >> first >> at(_, 'a'),
            N=g >> count,
        ))

    b = freds \
        >> chunkBy('b') \
        >> inject(_, Null, _) >> (lambda p, g: p >> join >> (g >> byA >> join >> Null))


def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')




