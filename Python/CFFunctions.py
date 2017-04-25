import numpy as np
import unicodecsv as csv


# Write names to csv to be labelled manually
def writeFriends(stack):
    allNames = stack.personName.unique()
    fileName = '/Users/adamhare/Google Drive/Junior Year/Oxford/Hilary/ML/Project/Labelled Friends/friends.csv'
    with open(fileName, 'wb') as csvfile:
        writerFriends = csv.writer(csvfile, encoding='utf-8')
        for friend in allNames:
            writerFriends.writerow([friend, ' '])


# Counts the number of friends who have a minimum score of over 0.5 over all page likes
def countFilteredData(data, m):
    counter = 0
    for j in range(0, m):
        thisMin = np.amin(data[j, :])
        if thisMin > 0.5:
            # print(idToName[friendIds[j]], thisMin, np.mean(afterFilter[j, :]), np.amax(afterFilter[j, :]))
            counter += 1
    return counter


# Give a metric for how well the collaborative filtering is performing
def scoreCF(P, CF):
    m, n = P.shape
    # predictOver = 0
    err = 0
    # If a confirmed like is given over 1 in the collaborative filtering, do nothing
    # If it's less than 1 for a confirmed like, add the distance to the error term
    for j in range(0, m):
        for k in range(0, n):
            if P[j, k] != 0:
                err += max(0, P[j, k] - CF[j, k])
    return err


# The following code is adapted from code given in an exercise sheet:
# https://www.cs.ox.ac.uk/teaching/materials14-15/ml/class2.pdf
# It implements collaborative filtering
# The input score is a list to which the score for the given reg and f will be added.
# The input getScore is a boolean indicating if the score should be returned. If True, the score will be appended to
# the score variable and the function won't return anything. If False, the function returns the new matrix.
def runCF(P, reg, f, score, getScore):
    print(reg, f)
    m, n = P.shape

    # Random Initialization
    # X is (m x f)
    # Y is (f x n)
    X = 1 - 2 * np.random.rand(m, f)
    Y = 1 - 2 * np.random.rand(f, n)
    X *= 0.1
    Y *= 0.1

    # Alternating Weighted Ridge Regression
    C = np.abs(P)  # Will be 0 only when P[i,j] == 0. -> all pages equally weighted
    iterCounter = 0
    xPrev = np.sum(X)
    yPrev = np.sum(Y)
    hasConverged = False
    iterConCount = 0
    prevIter = False
    while not hasConverged:
        #  Solve for X keeping Y fixed
        #  Each user u has a different set of weights Cu
        for u, Cu in enumerate(C):
            X[u] = np.linalg.solve(
                np.dot(Y * Cu, Y.T) + reg * np.eye(f),
                np.dot(Y * Cu, P[u]))

        # Solve for X keeping Y fixed
        for i, Ci in enumerate(C.T):
            Y[:, i] = np.linalg.solve(
                np.dot(X.T * Ci, X) + reg * np.eye(f),
                np.dot(X.T * Ci, P[:, i].T))

        # Test to see if the algorithm has (roughly) converged
        if np.abs(np.sum(X) - xPrev) > 0.00075 and np.abs(np.sum(Y) - yPrev) > 0.00075:
            xPrev = np.sum(X)
            yPrev = np.sum(Y)
            iterCounter += 1
            if iterCounter == 5000:
                print("# of Iterations Exceeded 5000")
                hasConverged = True
        else:
            iterCounter += 1
            xPrev = np.sum(X)
            yPrev = np.sum(Y)
            if prevIter:
                iterConCount += 1
            else:
                prevIter = True
                iterConCount = 1
            if iterConCount >= 5 and iterCounter > 100:
                hasConverged = True
                print("Converged in " + str(iterCounter) + " Iterations")
        if iterCounter % 100 == 0:
            print(iterCounter)

    afterFilter = np.dot(X, Y)

    if getScore:
        scr = scoreCF(P, afterFilter)
        off = countFilteredData(afterFilter, m)
        score.append([reg, f, scr, off])
        print(reg, f, scr, off)
    else:
        return afterFilter


# This will print a given matrix to a csv file for later use
def saveCF(CF, fileName):
    np.savetxt(fileName, CF, delimiter=",")


# Load filtered data
def loadCF(fileName):
    return np.loadtxt(fileName, delimiter=",")
