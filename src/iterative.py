'''
Created on Nov 20, 2012

@author: vinnie
'''

import cProfile
from pprint import pprint
from operator import mul
from random import shuffle
from collections import Counter
from utils import *
import pylab as plb
import numpy as np

# doesn't matter what the upper bound is as long as enough primes can be generated
_MAX_PRIME = 1000

def in1d_running(primes, A):
    '''
    Optimized to compare the modulus of prime products to test set inclusion
    '''
    j = 0
    A_product = reduce(mul, A, 1)
    running_product = primes[0]
    while j < len(primes) and (A_product % running_product) == 0:
        j += 1
        running_product *= primes[j]
    return j

def s_A(Q, A):
    '''
    Optimized to count the occurrences of each element 
    '''
    row_range = xrange(len(Q))
    return Counter([Q[i][k] for i in row_range for k in xrange(in1d_running(Q[i], A))])

def P_map(Q, set_A, set_s_A):
    '''
    Optimized to store each P(A) value and create a map of P(A) values iteratively
    Also slightly optimized by using the counter created in s_A instead of repeating
    sums 
    '''
    m = len(Q)
    p_map = {}
    for A in set_A:
        if len(A) == 0:
            p_map[A] = 0
        if len(A) == 1:
            p_map[A] = (1.0/m)
        else:
            p_map[A] = (1.0/m) * sum(p_map[without(A,aa[0])]*aa[1] for aa in set_s_A[A].items())
    return p_map

def delta_prime(Q):
    '''
    Optimized to use the P(A) map, generate set_A and s_A_map only once
    '''
    m = len(Q)
    m_range = [row[0] for row in Q]
    set_A = generate_A(m_range) # have to be in this order because of P
    s_A_map = {A : s_A(Q, A) for A in set_A}
    p_map = P_map(Q, set_A, s_A_map)
    return (1.0/(m**2)) * sum(p_map[A]*sum(s_A_map[A].values()) for A in set_A)

def d_prime(Q, n):
    '''
    Similar optimizations to delta_prime
    '''
    m = len(Q)
    m_range = [row[0] for row in Q]
    set_A = generate_A(m_range) # have to be in this order because of P
    s_A_map = {A : s_A(Q, A) for A in set_A}
    p_map = P_map(Q, set_A, s_A_map)
    # recompute set_A for |A| == n-1
    set_A = [A for A in set_A if len(A) == n-1]
    return (1.0/m) * sum(p_map[A]*sum(s_A_map[A].values()) for A in set_A)

def primes_sieve(limit):
    '''
    Prime generator by sieving
    '''
    a = [True] * limit                       # Initialize the primality list
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in xrange(i*i, limit, i):  # Mark factors non-prime
                a[n] = False
                
def Q2Prime(Q, primes):
    '''
    Converts the single hashing scheme Q into a prime matrix
    '''
    return [[primes[j] for j in row] for row in Q]

def Prime2Q(Q, primes):
    '''
    Converts the prime single hashing scheme Q into a 0-index matrix
    '''
    primes_idx = {p : i for (p,i) in zip(primes, range(len(primes)))}
    return [[primes_idx[j] for j in row] for row in Q]

def analyze_random_Q(m, n_Q):
    prime_gen = primes_sieve(_MAX_PRIME) 
    primes = [prime_gen.next() for i in xrange(m)]
    
    scores = []
    best_score = float('inf')
    worst_score = 0
    
    for Q in n_random_Q(m, n_Q):
        score = delta_prime(Q2Prime(Q, primes))
        scores.append(score)
        if score < best_score:
            best_score = score
            best_Q = Q
        elif score > worst_score:
            worst_score = score
            worst_Q = Q
            
    scores = np.array(scores)
    plb.hist(scores, bins=100)
    plb.title("M=%d for %d random matrices\nmean=%f, std dev=%f" 
              %(m, n_Q, np.mean(scores), np.std(scores)))
    plb.savefig('m%d_scores_r%d.png' %(m, n_Q))
    
    f = open('m%d_scores_r%d.txt' %(m, n_Q),'w')
    for score in scores:
        print >> f, score
        
    f = open('m%d_matrices_r%d.txt' %(m, n_Q),'w')
    print >> f, "Best", best_score, best_Q
    print >> f, "Worst", worst_score, worst_Q
    
    return

def profile_delta_prime(Q):
    prime_gen = primes_sieve(_MAX_PRIME)
    primes = [prime_gen.next() for i in xrange(len(Q))]
    delta_prime(Q2Prime(Q, primes))
    return

def profile():
    cProfile.run('profile_delta_prime(random_Q(3))')
    cProfile.run('profile_delta_prime(random_Q(4))')
    cProfile.run('profile_delta_prime(random_Q(5))')
    cProfile.run('profile_delta_prime(random_Q(6))')
    cProfile.run('profile_delta_prime(random_Q(7))')
    cProfile.run('profile_delta_prime(random_Q(8))')
    cProfile.run('profile_delta_prime(random_Q(9))')
    cProfile.run('profile_delta_prime(random_Q(10))')
    return

if __name__ == '__main__':
#    profile()
    analyze_random_Q(6, 10000)
    