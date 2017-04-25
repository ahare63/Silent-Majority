import glob
import pandas as pd
import numpy as np
from CFFunctions import loadCF
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2

# Run the final training and testing on the data


# Gather the data necessary for a confusion matrix
def getConfusion(predicted, actual, Overall, CC, CL, LC, LL):
    n = len(predicted)
    cc = 0  # predicted conservative and actually conservative
    cl = 0  # predicted conservative and actually liberal
    lc = 0  # predicted liberal and actually conservative
    ll = 0  # predicted liberal and actually liberal

    for i in range(0, n):
        if predicted[i] == 0 and actual[i] == 0:
            cc += 1
        elif predicted[i] == 0 and actual[i] == 1:
            cl += 1
        elif predicted[i] == 1 and actual[i] == 0:
            lc += 1
        elif predicted[i] == 1 and actual[i] == 1:
            ll += 1
        else:
            raise Exception("Values Other Than 0 and 1")
    if cc + cl + lc + ll != n:
        raise Exception("Not All Data Counted")

    CC.append(float(cc)/float(n))
    CL.append(float(cl)/float(n))
    LC.append(float(lc)/float(n))
    LL.append(float(ll)/float(n))
    Overall.append(float(cc + ll)/float(n))


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
# print(myMatrix)

for index, row in slimStack.iterrows():
    booleanTable.set_value(row['personid'], row['pageName'], 1)

# print(booleanTable.shape)

P = booleanTable.as_matrix()

# Optimal Values determined from CFHyperParameters.py
afterFilter = loadCF("filteredData.csv")

# read in labeled data
nameIsDem = {}
nameIsRep = {}
df = pd.read_csv('/Users/adamhare/Google Drive/Junior Year/Oxford/Hilary/ML/Project/Labeled Friends/labeled.csv')
for row in df.iterrows():
    if row[1].isDem == row[1].isRep:
        raise Exception('Label not exclusive')
    nameIsDem[row[1].Name] = row[1].isDem
    nameIsRep[row[1].Name] = row[1].isRep

names = []
y = []
for index, row in booleanTable.iterrows():
    y.append([nameIsRep[idToName[index]], nameIsDem[idToName[index]]])
    names.append(idToName[index])

y = np.array(y)
names = np.array(names)
# print(names)

numIts = 1
original = []
filtered = []
N = len(y)
Ntrain = int(0.85 * N)

Oreg = 10**(-3)
Of = 1024
CFreg = 10**(-3)
CFf = 64
nIt = 300

OOverall = []
OCC = []  # predicted conservative and actually conservative
OCL = []  # predicted conservative and actually liberal
OLC = []  # predicted liberal and actually conservative
OLL = []  # predicted liberal and actually liberal
CFOverall = []
CFCC = []
CFCL = []
CFLC =[]
CFLL = []

for j in range(0, nIt):
    if j % 25 == 0 and j != 0:
        print(j)  # Just to see how the program is progressing
    shuffler = np.random.permutation(N)
    yTrain = y[shuffler[:Ntrain]]
    yTest = y[shuffler[Ntrain:]]
    names = names[shuffler]

    # Use unfiltered, original data
    xTrain = P[shuffler[:Ntrain]]
    xTest = P[shuffler[Ntrain:]]
    nFriends, nFeatures = xTrain.shape
    model = Sequential()
    model.add(Dense(output_dim=Of, input_dim=nFeatures, W_regularizer=l2(Oreg), init='uniform'))
    model.add(Activation("sigmoid"))
    model.add(Dense(output_dim=2, W_regularizer=l2(Oreg), init='uniform'))
    model.add(Activation("softmax"))
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
    model.fit(xTrain, yTrain, batch_size=len(xTrain), shuffle=True, nb_epoch=10, verbose=0)
    classes = model.predict_classes(xTest, verbose=0)
    getConfusion(classes, yTrain[:, 1], OOverall, OCC, OCL, OLC, OLL)

    # Use filtered data
    xTrain = afterFilter[shuffler[:Ntrain]]
    xTest = afterFilter[shuffler[Ntrain:]]
    model = Sequential()
    model.add(Dense(output_dim=CFf, input_dim=nFeatures, W_regularizer=l2(CFreg), init='uniform'))
    model.add(Activation("sigmoid"))
    model.add(Dense(output_dim=2, W_regularizer=l2(CFreg), init='uniform'))
    model.add(Activation("softmax"))
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
    model.fit(xTrain, yTrain, batch_size=len(xTrain), shuffle=True, nb_epoch=10, verbose=0)
    classes = model.predict_classes(xTest, verbose=0)
    getConfusion(classes, yTrain[:, 1], CFOverall, CFCC, CFCL, CFLC, CFLL)

    # if j % 100 == 0 and j != 0:  # Print results along the way in case the program needs to be stopped
    #    print("Iterations completed: ", j)
    #    print("Original Overall", np.mean(OOverall), np.std(OOverall))
    #    print("Original CC", np.mean(OCC), np.std(OCC))
    #    print("Original CL", np.mean(OCL), np.std(OCL))
    #    print("Original LC", np.mean(OLC), np.std(OLC))
    #    print("Original LL", np.mean(OLL), np.std(OLL))
    #    print("")
    #    print("CF Overall", np.mean(CFOverall), np.std(CFOverall))
    #    print("CF CC", np.mean(CFCC), np.std(CFCC))
    #    print("CF CL", np.mean(CFCL), np.std(CFCL))
    #    print("CF LC", np.mean(CFLC), np.std(CFLC))
    #    print("CF LL", np.mean(CFLL), np.std(CFLL))

print("Original Overall", np.mean(OOverall), np.std(OOverall))
print("Original CC", np.mean(OCC), np.std(OCC))
print("Original CL", np.mean(OCL), np.std(OCL))
print("Original LC", np.mean(OLC), np.std(OLC))
print("Original LL", np.mean(OLL), np.std(OLL))
print("")
print("CF Overall", np.mean(CFOverall), np.std(CFOverall))
print("CF CC", np.mean(CFCC), np.std(CFCC))
print("CF CL", np.mean(CFCL), np.std(CFCL))
print("CF LC", np.mean(CFLC), np.std(CFLC))
print("CF LL", np.mean(CFLL), np.std(CFLL))
