#!/usr/bin/python3
from math import *
import random
import time

# demonstration that when we sum four independent random variables, the
# correlation between the sum and any one of them is r = 0.5

def correl2(xs, ys):
    # Simple-minded code from mathematical definition
    #
    # r =  N * sum(x * y) - sum(x) * sum(y)
    #     -----------------------------------------------------------------
    #      sqrt((N * sum(x**2) -(sum(x))**2) * (N * sum(y**2) -(sum(y))**2))

    N = len(xs)

    sum_xy = sum(x * y for x, y in zip(xs, ys))
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_x2 = sum(x * x for x in xs)
    sum_y2 = sum(y * y for y in ys)

    A = N * sum_xy - sum_x * sum_y
    B = N * sum_x2 - sum_x**2
    C = N * sum_y2 - sum_y**2

    return float(A) / sqrt(B * C)

def correlW(xs, ys):
    assert len(xs) == len(ys)
    # Slightly bizzare code: this is cribbed from Wikipedia article on
    # "correlation", but that assumes that arrays run from 1 to N ...
    # Seems most reliable to pad-out with a dummy element zero.

    N = len(xs)
    x = [None] + xs
    y = [None] + ys

    sum_sq_x = 0
    sum_sq_y = 0
    sum_coproduct = 0
    mean_x = float(x[1])
    mean_y = float(y[1])

    for i in range(2, N + 1): # ie last i is N, as desired
        sweep = (i - 1.0) / i
        delta_x = x[i] - mean_x
        delta_y = y[i] - mean_y
        sum_sq_x += delta_x * delta_x * sweep
        sum_sq_y += delta_y * delta_y * sweep
        sum_coproduct += delta_x * delta_y * sweep
        mean_x += delta_x / i
        mean_y += delta_y / i

    pop_sd_x = sqrt( sum_sq_x / N )
    pop_sd_y = sqrt( sum_sq_y / N )
    cov_x_y = sum_coproduct / N
    correlation = cov_x_y / (pop_sd_x * pop_sd_y)
    return correlation

def quite_close(a, b):
    ratio = a / b
    return abs(ratio - 1) < 1e-9

def correl(*args):
    answer1 = correl2(*args)
    answer2 = correlW(*args)
    if not quite_close(answer1, answer2):
        print("+++ Problem:", answer1, answer2)
        assert False
    return answer1

def one_trial(size):
    dataA = [random.random() for x in range(size)]
    dataB = [random.random() for x in range(size)]
    dataC = [random.random() for x in range(size)]
    dataD = [random.random() for x in range(size)]

    combined = [a + b + c + d for a, b, c, d in zip(dataA, dataB, dataC, dataD)]

    return correl(combined, dataA)

# take an average

repeats = 1000
r_sum = 0.0
for i in range(repeats):
    r_sum += one_trial(1000)

print("r =", r_sum/repeats)


