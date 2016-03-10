from math import log
import operator
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

def clacEntropy(data):
    numEntropy = len(data)
    labels = {}
    for fac in data:
        cur = fac[-1]
        if cur not in labels.keys():
            labels[cur] = 0
        labels[cur] += 1
    entropy = 0.0
    for key in labels:
        prob = float(labels[key]/numEntropy)
        entropy -= prob * log(prob,2)
    return entropy



def splitData(data,axis,value):
    retData = []
    for vec in data:
        if vec[axis] == value:
            reduceFea = vec[:axis]
            reduceFea.extend(vec[axis+1:])
            retData.append(reduceFea)
    return retData

'''
data,label = createDataSet()
print("data:",data)
reduce = splitData(data,0,1)
print("reduce:",reduce)
'''
def chooseFea(data):
    numFea = len(data[0]) - 1
    baseEntropy = clacEntropy(data)
    bestGain = 0.0
    bestFea = -1
    for i in range(numFea):
        feaList = [k[i] for k in data]
        uniqueVals = set(feaList)
        newEntropy = 0.0
        for value in uniqueVals:
            subData = splitData(data,i,value)
            prob = len(subData)/len(data)
            newEntropy += prob*clacEntropy(subData)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestGain):
            bestGain = infoGain
            bestFea = i

    return bestFea
'''
data,label = createDataSet()
print(chooseFea(data))
'''
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClass = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClass[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]#所有label都相同
    if len(dataSet[0]) == 1: #没有可分的特征了~只剩下label
        return majorityCnt(classList)
    bestFeat = chooseFea(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]   #因为传递参数是引用,所以要重新复制一个
        myTree[bestFeatLabel][value] = createTree(splitData(dataSet, bestFeat, value),subLabels)
    return myTree

data,label = createDataSet()
print(createTree(data,label))