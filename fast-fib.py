import time
import math

print "hello"



def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def fib_iter(n):
    a = 1
    b = 0

    while True:
        if n == 0:
            return b

        a, b, n = a + b, a, n - 1

def fib_iter_better(n):
    a = 1
    b = 0
    p = 0
    q = 1

    while True:
        if n == 0:
            return b

        if n % 2 == 0: # even
            p, q, n = p*p + q*q, q*q + 2*p*q, n / 2
        else:
            a, b, n = b*q + a*q + a*p, b*p + a*q, n - 1

#----------------------------------------------------------------
# time calculations

def how_long(n, f, args):
    # returns f(args), time for n calls
    start = time.clock()

    while n > 1:
        apply(f, args)
        n -= 1

    result = apply(f, args)
    end = time.clock()

    return result, end - start
        
def measure(f, args):
    # choose a suitable number of repeats
    # bring total time for n repeats up to 0.1 seconds or more

    TARGET = 0.1 # seconds
    repeats = 1

    while True:
        result, duration = how_long(repeats, f, args)

        if duration > TARGET:
            # print result, duration, repeats
            return duration / repeats

        repeats = 2 * repeats

##for i in range(20):
##    print i, measure(fib, (i,)), measure(fib_iter, (i,))
##

for j in range(20):
    i = j * 100000
    print i, measure(fib_iter, (i,)), measure(fib_iter_better, (i,))    
