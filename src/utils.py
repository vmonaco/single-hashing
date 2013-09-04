'''
Created on Nov 20, 2012

@author: vinnie
'''

import cProfile
import numpy as np
from pprint import pprint
from operator import itemgetter, mul
from itertools import combinations, permutations, product
from random import shuffle
from collections import Counter

Q_1 = \
[[0,2,1,3],
 [1,0,2,3],
 [2,3,0,1],
 [3,2,1,0]]

Q_linear = \
[[0,1,2,3],
 [1,2,3,0],
 [2,3,0,1],
 [3,0,1,2]]

def without(L, e):
    '''
    The tuple L without elements == e
    '''
    return tuple(a for a in L if a != e)

def permute_skip_n(elements, n=1):
    '''
    Generate all permutations after skipping the first n elements
    '''
    for p in permutations(elements[n:]):
        yield elements[:n] + list(p)

def generate_A(m_range):
    '''
    Generate all A combinations (every possible hash value sequence)
    Grouped by size
    '''
    return [A for i in xrange(len(m_range)) for A in list(combinations(m_range, i))]

def generate_Q(m):
    '''
    Generate all possible m x m single hash matrices
    Under 2 conditions:
        1) Each row contains [0...m) in some order
        2) The first column contains [0...m) in order
    '''
    row_perms = []
    m_range = range(m)
    for i in m_range:
        row_perms.append(list(permute_skip_n(m_range[i:]+m_range[:i])))
    return product(*row_perms)

def random_Q(m):
    '''
    Generate a valid random single hashing scheme according to the rules:
        i) The first colomn contains [0...m) in ascending order
        ii) Each row contains [0...m)
    '''
    m_range = range(m)
    first_col = [[i] for i in m_range]
    rest_col = [m_range[i+1:] + m_range[:i] for i in m_range]
    [shuffle(col) for col in rest_col]
    m = [first_col[i] + rest_col[i] for i in m_range]
    return m

def n_random_Q(m, n):
    return [random_Q(m) for i in xrange(n)]
    