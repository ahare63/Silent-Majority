from CFFunctions import saveCF, runCF
import glob
import pandas as pd
import numpy as np

# Save the collaborative filtered matrix with the optimal hyper-parameters

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

myArray = runCF(P, 10**(-5), 128, [], False)
saveCF(myArray, "filteredData.csv")
