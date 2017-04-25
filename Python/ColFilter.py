#  Collaborative filtering from practical

from __future__ import division
import numpy as np
import pdb


# MOVIES: Legally Blond; Matrix; Bourne Identity; You’ve Got Mail;
# The Devil Wears Prada; The Dark Knight; The Lord of the Rings.
P = [[0, 0, -1, 0, -1, 1, 1],  # User 1
     [-1, 1, 1, -1, 0, 1, 1],  # User 2
     [0, 1, 1, 0, 0, -1, 1],  # User 3
     [-1, 1, 1, 0, 0, 1, 1],  # User 4
     [0, 1, 1, 0, 0, 1, 1],  # User 5
     [1, -1, 1, 1, 1, -1, 0],  # User 6
     [-1, 1, -1, 0, -1, 0, 1],  # User 7
     [0, -1, 0, 1, 1, -1, -1],  # User 8
     [0, 0, -1, 1, 1, 0, -1]]  # User 9
P = np.array(P)
# Parameters
reg = 0.1  # regularization parameter
f = 2  # number of factors
m, n = P.shape
# Random Initialization
# X is (m x f)
# Y is (f x n)
X = 1 - 2 * np.random.rand(m, f)
Y = 1 - 2 * np.random.rand(f, n)
X *= 0.1
Y *= 0.1

# Alternating Weighted Ridge Regression
C = np.abs(P)  # Will be 0 only when P[i,j] == 0.
for _ in xrange(100):
    # Solve for X keeping Y fixed
    # Each user u has a different set of weights Cu
    for u, Cu in enumerate(C):
        X[u] = np.linalg.solve(
            np.dot(Y * Cu, Y.T) + reg * np.eye(f),
            np.dot(Y * Cu, P[u])
        )
    # Solve for X keeping Y fixed
    for i, Ci in enumerate(C.T):
        Y[:, i] = np.linalg.solve(
            np.dot(X.T * Ci, X) + reg * np.eye(f),
            np.dot(X.T * Ci, P[:, i].T)
        )
print 'Alternating Weighted Ridge Regression:'
print np.dot(X, Y)
