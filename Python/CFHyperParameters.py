import glob
import pandas as pd
import numpy as np
from CFFunctions import runCF

# This file is for validating the collaborative filtering hyperparameters

# Gather and read all CSV files
allCSV = glob.glob('/Users/adamhare/Google Drive/Junior Year/Oxford/Hilary/ML/Project/Likes Data/*.csv')

myList = []
for myFile in allCSV:
    df = pd.read_csv(myFile)
    myList.append(df)
rawStack = pd.concat(myList)

# Delete multiple pages liked by one person with the same name
rawStack = rawStack.sort_values(['pageName', 'personid']).drop_duplicates(['pageName', 'personid'])
slimStack = rawStack[rawStack.groupby('pageName').personName.transform(len) > 2]  # Remove pages with only one like

names = slimStack.personName.unique()
friendIds = slimStack.personid.unique()
pages = slimStack.pageName.unique()
pageIds = slimStack.pageid.unique()

if len(names) != len(friendIds):
    raise Exception("Friends Mismatch")  # Assumes each friend has unique name (ok here)

idToName = {}
nameToId = {}
nFriends = len(friendIds)

for i in range(0, nFriends):
    thisName = names[i]
    thisId = friendIds[i]
    idToName[thisId] = thisName
    nameToId[thisName] = thisId

booleanTable = pd.DataFrame(data=np.zeros((nFriends, len(pages))), index=friendIds, columns=pages)

for index, row in slimStack.iterrows():
    booleanTable.set_value(row['personid'], row['pageName'], 1)

P = booleanTable.as_matrix()

myReg = np.logspace(-5, 5, 11)
myF = [2**i for i in range(1, 9)]
score = []  # Record a measure of how well each f, reg pair does

for r in myReg:
    for f in myF:
        runCF(P, r, f, score, True)
print(score)

