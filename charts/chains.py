from itertools import *
import time
r = [-11,-10,-9, 1, 2, 3, 4, -4, -7, -42, -2, 3, 4, 5, -3, -37, -7, 8, 9, -4, -5, -6]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def boundaries_generator(predicate, iterable):
    iterable = iter(iterable)
    while True:
        finished = False
        for x in iterable:
            if predicate(x):
                finished = True
                yield x
                break
        for x in iterable:
            if not predicate(x):
                finished = True
                yield x
                break
        if not finished:
            break
        
    
def boundaries(predicate, iterable, fillvalue=None):
    gen = list(boundaries_generator(predicate, iterable))
    even = gen[::2]
    odd = gen[1::2]
    
    return list(izip_longest(even,odd,fillvalue=fillvalue))
    


print boundaries(lambda x:x<0, r, 'xuxu')
