import glob
import pandas as pd
import numpy as np
from CFFunctions import loadCF
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2

# Find the hyper-parameters for the neural network. O indicates the original data and CF collaborative filtered data

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

myReg = np.logspace(-5, 5, 11)
myF = [2**i for i in range(1, 11)]

N = len(y)
Ntrain = int(0.85*N)

shuffler = np.random.permutation(N)
xTrainO = P[shuffler[:Ntrain]]
xTrainCF = afterFilter[shuffler[:Ntrain]]
yTrain = y[shuffler[:Ntrain]]
xTestO = P[shuffler[Ntrain:]]
xTestCF = afterFilter[shuffler[Ntrain:]]
yTest = y[shuffler[Ntrain:]]

avgsO = []  # Store the average performance for original data
avgsCF = []  # Store the average performance for the filtered data
nCross = 10
Nval = int(.10 * len(yTrain))
friends, features = P.shape
for reg in myReg:
    for f in myF:
        print(reg, f)

        tempO = []  # Store the performance for each round of cross validation
        tempCF = []

        for i in range(0, nCross):
            shuff = np.random.permutation(Ntrain)

            # Use original data
            xValO = xTrainO[shuff[:Nval]]
            xValTrainO = xTrainO[shuff[Nval:]]
            yVal = yTrain[shuff[:Nval]]
            yValTrain = yTrain[shuff[Nval:]]

            # Train Neural Net on data
            model = Sequential()
            model.add(Dense(output_dim=f, input_dim=features, W_regularizer=l2(reg), init='uniform'))
            model.add(Activation("sigmoid"))
            model.add(Dense(output_dim=2, W_regularizer=l2(reg), init='uniform'))
            model.add(Activation("softmax"))
            model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
            model.fit(xValTrainO, yValTrain, batch_size=len(yValTrain), shuffle=True, nb_epoch=10, verbose=0)
            classes = model.predict_classes(xValO, verbose=0)
            acc = np.mean(classes == yVal[:, 1])
            tempO.append(acc)

            # Use filtered data
            xValCF = xTrainCF[shuff[:Nval]]
            xValTrainCF = xTrainCF[shuff[Nval:]]
            model = Sequential()
            model.add(Dense(output_dim=f, input_dim=features, W_regularizer=l2(reg), init='uniform'))
            model.add(Activation("sigmoid"))
            model.add(Dense(output_dim=2, W_regularizer=l2(reg), init='uniform'))
            model.add(Activation("softmax"))
            model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
            model.fit(xValTrainCF, yValTrain, batch_size=len(yValTrain), shuffle=True, nb_epoch=10, verbose=0)
            classes = model.predict_classes(xValCF, verbose=0)
            acc = np.mean(classes == yVal[:, 1])
            tempCF.append(acc)

        avgsO.append([reg, f, np.mean(tempO)])
        print("original", reg, f, np.mean(tempO))
        avgsCF.append([reg, f, np.mean(tempCF)])
        print("filtered", reg, f, np.mean(tempCF))

print(avgsO)
print(avgsCF)
