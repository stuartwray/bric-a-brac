from math import *
import random
import time

# demonstration that when we sum four independent random variables, the
# correlation between the sum and one of them is r = 0.5

def correl2(xs, ys):
    # Simple-minded code from definition
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

correl = correlW

def one_trial(size):
    dataA = [random.random() for x in range(size)]
    dataB = [random.random() for x in range(size)]
    dataC = [random.random() for x in range(size)]
    dataD = [random.random() for x in range(size)]

    combined = [a + b + c + d for a, b, c, d in zip(dataA, dataB, dataC, dataD)]

    return correl(combined, dataA)

repeats = 10000
r_sum = 0.0
for i in range(repeats):
    r_sum += one_trial(1000)
    
print("r =", r_sum/repeats)

# this is actually code from another use which might possibly be useful one day ...
# (it uses a bootstrap --- random resampling --- to empirically estimate a p-value
##
###-----------------------------------------------------------------------
### now do a bootstrap, creating fake data based on what we have
##
##def do_bootstrap():
##    fakeYdata = [random.choice(ydata) for i in range(len(data))]
##    return correlW(xdata, fakeYdata)
##
##better = 0
##worse = 0
##
##while True:
##    rep = 100000
##    start = time.clock()
##    for i in range(rep):
##        if do_bootstrap() >= reference_r:
##            better += 1
##        else:
##            worse += 1
##
##    stop = time.clock()
##    total = better + worse
##    p = float(better) / total
##    print "equal or better:", better, "worse:", worse, "total:", total, "p =", p
##    print rep / (stop - start ), "per sec"
##
### if this runs for a long time it gives the following results
### equal or better: 667532 worse: 999332468 total: 1000000000 p = 0.000667532
### 16751.5660487 per sec
##

