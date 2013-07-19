#!/usr/bin/python3

from problib import *

# This data is from a column in the Guardian
# ("Gavyn Davies does the maths", 20 July 2006),
# In WW2 there were five captured German tanks with these serial numbers:

serials = [20, 31, 43, 78, 92]

# Problem to solve: what is the most likely production run?
# According to the article, here's how to it out:
# let   M = the highest observed serial,
# and   S = number of serials,
# then  E = (M - 1) * (S + 1) / S
#       is a good estimator of the production run
#       (ie max serial that could be observed)
#       (in this case E = 109.2)

# Let's see what Bayes thinks ...
#
# P(H|D) = P(D|H) P(H|)
#          ------------
#             P(D|)
#
# Where P(D|) = sum over all h of P(D|h) P(h|)

max_conceivable_number = 10000 # pick a number that seems big enough
log_probs = []

for i in range(max_conceivable_number):
    # Hypothesis H is "E = i"
    log_P_H_given_nothing = log(1.0 / max_conceivable_number) # uniform prior

    # Data is all the serials, which we can take sequentially
    log_P_D_given_H = log(1.0) # for starters
    for s, n in zip(serials, range(len(serials))):
        if s > i:
            # prob is zero! can't have serial greater than production run!
            log_P_D_given_H += logZERO
        else:
            # uniform prob of picking any in this size production run,
            # but need to account for the ones we already picked
            left_in_run = i - n
            log_P_D_given_H += log(1.0 / left_in_run)

    log_likelihood_D = log_P_D_given_H + log_P_H_given_nothing
    log_probs.append(log_likelihood_D)

# Now need to divide all by P(D|), which is just normalisation ...

log_probs = log_normalise(log_probs)

# Note that this is the probability density function
# The expected production size E comes at the median of this
# so translate to cumulative frequency and plot

cumulative = 0.0
out = open("tmp.csv", "w")

for i, p in zip(range(len(log_probs)), log_probs):
    if i > 200:
        break
    cumulative += exp(p)
    text = "%d,%f" % (i, cumulative)
    print(text)
    print(text, file=out)

out.close()

# we get 108 as the median, and hence the best guess for the
# production run. We can also easily read off lower and upper
# quartiles, namely 98 and 128.


