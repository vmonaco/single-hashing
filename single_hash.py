'''
Created on Nov 20, 2012

@author: vinnie
'''
from utils import *


def in1d_running(q, A):
    '''
    j where q[k] in A for 0 <= k <= j
    This is the maximum index j where q[0:j] is in A
    '''
    j = 0
    while j < len(q) and q[j] in A:
        j += 1
    return j


def s_A(Q, A):
    '''
    s(A) = {(i,j) | q[i,k] in A for 0 <= k <= j}
    The set of all coordinates where Q[i,0:k] is in A for 0 <= k <= j, 
    where j is defined by the ind1d_running function above 
    '''
    return [(i, k) for i in A for k in range(in1d_running(Q[i], A))]


def P(Q, A, m):
    '''
    Given the single hashing scheme defined by matrix Q,
    compute the probably that the first |A| slots are occupied by the 
    slots in A
    '''
    if len(A) == 0:
        return 0
    elif len(A) == 1:
        return 1.0 / m
    else:
        return (1.0 / m) * sum([P(Q, tuple(a for a in A if a != Q[i][j]), m)
                                for (i, j) in s_A(Q, A)])


def P_map(Q):
    '''
    Compute P(A) for each n-combination in [0,1,2...m) for 0 <= n < m
    Also compute P( [0,1,2...m] ). Only one combination is needed, this should 
    always be equal to 1.0
    '''
    m = len(Q)
    m_range = range(m)
    p = {A: P(Q, A, m) for A in generate_A(m_range)}
    return p


def delta_prime(Q):
    '''
    The average number of spaces probed for each insertion by the time
    the table is full. This is the best measure for the efficiency of a
    single hashing scheme
    '''
    m = len(Q)
    m_range = [row[0] for row in Q]
    set_A = generate_A(m_range)
    return (1.0 / (m ** 2)) * sum(P(Q, A, m) * len(s_A(Q, A)) for A in set_A)


def d_prime(Q, n):
    '''
    The average number of probes needed to insert the nth element
    into a table with single hashing scheme Q
    '''
    m = len(Q)
    m_range = [row[0] for row in Q]
    assert n <= m
    set_A = [A for A in generate_A(m_range) if len(A) == n - 1]
    return (1.0 / m) * sum(P(Q, A, m) * len(s_A(Q, A)) for A in set_A)


def search_random(m, N):
    from operator import itemgetter
    import matplotlib.pyplot as plt
    import random

    random.seed(1234)

    score_Q = [(delta_prime(Q), Q) for Q in [random_Q(m) for _ in range(N)]]

    min_score, min_Q = min(score_Q, key=itemgetter(0))
    max_score, max_Q = max(score_Q, key=itemgetter(0))

    print('Best score:', min_score, min_Q)
    print('Worst score:', max_score, max_Q)

    plt.hist(list(zip(*score_Q))[0], bins=100, normed=True)
    plt.xlabel('Probes per insertion')
    plt.ylabel('Density')
    plt.savefig('m%d_scores.png' % m)

    return


if __name__ == '__main__':
    search_random(5, 10000)
