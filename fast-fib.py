#!/usr/bin/python3
import time
import math

# Faster and faster Fibonacci functions
# This is the obvious recursive one, but it's slow because it does a lot
# of recalculation. (So a version of this was once used as a simple
# functional language bench-mark for that reason: it gives a crude measure
# of function-call overhead.)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# This is the obvious iterative version of the same calculation

def fib_iter(n):
    a = 1
    b = 0
    while True:
        if n == 0:
            return b
        a, b, n = a + b, a, n - 1

# And this is a rather un-obvious iterative version, based on exercise 1.19
# in SICP. (It uses the same idea as a square-and-multiply exponentiator.)

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
        f(*args)
        n -= 1
    result = f(*args)
    end = time.clock()
    return result, end - start

def measure(f, *args):
    # choose a suitable number of repeats, so as to bring
    # the total time for n repeats up to target number of seconds
    TARGET = 1.0 # seconds
    repeats = 1
    while True:
        result, duration = how_long(repeats, f, args)
        if duration > TARGET:
            return duration / repeats
        repeats = 2 * repeats

for i in range(1, 21):
    n = i * 10000
    print(n, measure(fib_iter, n), measure(fib_iter_better, n))
