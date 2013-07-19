# Fiddle around with probabilities

from math import *

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def log_factorial(x):
    if x == 0:
        return log(1)
    else:
        # the usual approximation
        return x * log(x)- x + log(2 * pi * x)/2 + 1/(12 * x) - 1/(360*x*x*x)

def log_choice(n, k):
    return log_factorial(n) - log_factorial(n - k) - log_factorial(k)

def log_falling_power(n, k):
    return log_factorial(n) - log_factorial(n - k)

logZERO = -1.0e100 # set a floor to log probs in log_sum etc

def log_sum(log_probs):
    max_log_prob = max(log_probs)
    s = sum(exp(x - max_log_prob) for x in log_probs)
    if s == 0.0:
        return logZERO
    else:
        return max_log_prob + log(s)

log_product = sum # so our calculations look consistent

def log_normalise(log_probs):
    log_total = log_sum(log_probs)
    if log_total == logZERO:
        return [log(1.0 / len(log_probs))] * len(log_probs) # hopefully not needed
    else:
        return [max(logZERO, log_p - log_total) for log_p in log_probs]

def safe_log(x):
    if x <= 0.0:
        return logZERO
    else:
        return log(x)

# for the birthday "paradox"
# Assumes sampling with replacement (not strictly accurate)
def prob_no_duplicate(items, samples):
    log_top = log_factorial(items) - log_factorial(items - samples)
    log_bottom = log(items) * samples

    return exp(log_top - log_bottom)

