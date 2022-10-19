import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def loadCSV(filename, includesText=False):
    """Load data from csv file."""
    if includesText:
        data = pd.read_csv(filename, header=None)
    else:
        data = np.loadtxt(filename, delimiter=',')
    return data

def divideIntoClasses(data, numClasses, dim):
    """Divide data into classes by adding column with class number."""
    data = np.insert(data, dim, 0, axis=1)
    for i in range(numClasses):
        data[i*(100//numClasses):(i+1)*(100//numClasses), dim] = i
    return data

def initPrototypes(data, numExamples, numPrototypes, dim, random=True, initAtClassMean=False):
    """
    Initialize prototypes.
    Requires labaled data.
    """
    # sort data by class
    dataSorted = data[data[:,dim].argsort()]
    # get random data point(s) for each class
    prototypes = np.zeros((numPrototypes, dim+1))
    if initAtClassMean:
        for i in range(numPrototypes):
            prototypes[i] = np.append(np.mean(dataSorted[i*(numExamples//numPrototypes):(i+1)*(numExamples//numPrototypes), :-1], axis=0), dataSorted[i*(numExamples//numPrototypes)][-1])
    else:
        if random:
            for i in range(numPrototypes):
                prototypes[i] = dataSorted[np.random.randint(i*(numExamples//numPrototypes), (i+1)*(numExamples//numPrototypes)), :dim+1]
        else:
            for i in range(numPrototypes):
                prototypes[i] = dataSorted[i*(numExamples//numPrototypes), :dim+1]
    return prototypes

def scatterPlotData(data):
    """
    Create scatter plot with different colors for different classes.
    Only works for 2D data.
    Returns: scatter object for legend
    """	
    plt.scatter(data[:,0], data[:,1], c=data[:,2], cmap='rainbow')
    return plt.scatter([], [], color='black', label='Data')

def scatterPlotPrototypes(prototypes):
    """
    Create scatter plot with different colors for different classes.
    Only works for 2D data.
    Returns: scatter object for legend
    """	
    plt.scatter(prototypes[:,0], prototypes[:,1], c=prototypes[:,2], marker='*', s=200, cmap='rainbow', edgecolors='black')
    return plt.scatter([], [], color='black', marker='*', s=200, label='Prototypes')

def scatterPlotPrototypeTrajectory(prototypePositionHistory):
    """
    Add prototype trajectories to scatter plot.
    Only works for 2D data.

    Returns: plot object to be used in legend
    """
    for i in range(len(prototypePositionHistory[0])):
        plt.plot([prototypePositionHistory[j][i][0] for j in range(len(prototypePositionHistory))], [prototypePositionHistory[j][i][1] for j in range(len(prototypePositionHistory))], color='black', linestyle='dashed')
    return plt.plot([], [], color='black', linestyle='dashed', label='Prototype Trajectory')

def eaclidianDistance(x, y, labeled=True):
    """
    Calculate euclidian distance between two vectors.
    Supports higher dimensions.
    """
    if labeled:
        return np.linalg.norm(x[:-1] - y[:-1])
    else:
        return np.linalg.norm(x - y)

def getClosestPrototype(point, prototypes, findClosestSameAndDifferent=False):
    """
    Returns closest prototype to point.
    If findClosestSameAndDifferent is True, returns tuple of closest prototype to point with same class and closest prototype to point with different label.
    """
    # sort porotoypes by euclidian distance to point
    prototypesSorted = sorted(prototypes, key=lambda x: eaclidianDistance(point, x))

    if findClosestSameAndDifferent:
        closestSameLabel = [None]
        closestDifferentLabel = [None]
        # find first prototype with same label and first prototype with different label
        for prototype in prototypesSorted:
            if prototype[-1] == point[-1] and closestSameLabel[0] == None:
                closestSameLabel = prototype
            elif prototype[-1] != point[-1] and closestDifferentLabel[0] == None:
                closestDifferentLabel = prototype
            # break if both prototypes have been found
            if(closestSameLabel[0] != None and closestDifferentLabel[0] != None):
                break
        return closestSameLabel, closestDifferentLabel, prototypesSorted[0]
    else:
        # return closest prototype
        return prototypesSorted[0]


def lvq(method, data, prototypes, LR, maxEpochs, random=True, stopWhenStable=False, stableMovingAverage=5):
    """
    Execute Learning Vector Quantization 1.
    `method` can be 'lvq1' or 'glvq'.
    `data`: labeled data
    `prototypes`: prototypes
    `LR`: learning rate
    `maxEpochs`: maximum number of epochs
    `random`: if True, data is shuffled each epoch, default: True
    `stopWhenStable`: if True, learning stops when prototypes do not change significantly, default: False
    `stableMovingAverage`: number of epochs to calculate moving average of training error, default: 5

    Returns:
    `prototypes`: updated prototypes
    `trainingErrors`: list with len(elepsedEpochs) of training errors, containing number of misclassified examples per epoch, percentage of errors and moving average of training error percantage
    """
    # create list for storing training errors
    trainingErrors = []
    # create list of prototype positions for each epoch
    prototypePositionHistory = [prototypes.copy()]
    # loop over epochs
    for _ in range(maxEpochs):
        errors = 0
        # shuffle data if random is True
        if random:
            np.random.shuffle(data)
        # loop over data
        for i in range(data.shape[0]):
            # if method is glvq, find closest prototypes with same and different label
            if method.lower() == 'glvq':
                # get closest prototype and closest prototype of different class
                closestSamePrototype, closestDifferentClass, closestPrototype = getClosestPrototype(data[i], prototypes, findClosestSameAndDifferent=True)
                # update closest prototype of same class
                closestSamePrototype[:-1] += LR * (data[i][:-1] - closestSamePrototype[:-1])
                # update closest prototype of different class
                closestDifferentClass[:-1] -= LR * (data[i][:-1] - closestDifferentClass[:-1])
                if closestPrototype[-1] != data[i][-1]:
                    errors += 1
            else:
                # if method is lvq1, find closest prototype
                # get closest prototype
                closestPrototype = getClosestPrototype(data[i], prototypes)
                # update closest prototype
                changeBy = LR * (data[i][:-1] - closestPrototype[:-1])
                if data[i][-1] == closestPrototype[-1]:
                    closestPrototype[:-1] += changeBy
                else:
                    closestPrototype[:-1] -= changeBy
                    # add error to counter
                    errors += 1
        # calculate training error
        errorPercentage = errors / data.shape[0]
        # calculate error moving average
        if len(trainingErrors) >= stableMovingAverage:
            errorMovingAverage = np.mean([trainingErrors[i][1] for i in range(len(trainingErrors)-stableMovingAverage, len(trainingErrors))])
        else:
            errorMovingAverage = 0
        # add error to list
        trainingErrors.append([errors, errorPercentage, errorMovingAverage])
        # add prototype positions to list
        prototypePositionHistory.append(prototypes.copy())
        # if error moving average seems stable, stop learning
        if stopWhenStable and len(trainingErrors) >= stableMovingAverage*2:
            # get mean of last stableMovingAverage moving averages
            movingAverageMean = np.mean([trainingErrors[i][2] for i in range(len(trainingErrors)-stableMovingAverage, len(trainingErrors))])
            # check if all moving averages are within 0.01 of the mean
            differences = []
            for movingAverage in trainingErrors[-stableMovingAverage:]:
                differences.append(abs(movingAverage[2] - movingAverageMean))
            if max(differences) < 0.001:
                # stop learning
                return prototypes, trainingErrors, prototypePositionHistory
        # if method is glvq, decrease LR 10%
        if method.lower() == 'glvq':
            LR *= 0.9
        
    return prototypes, trainingErrors, prototypePositionHistory

def plotErrorOverEpochs(trainingErrors, errorMovingAverage=5, customTitle=None):
    """
    Plot training error over epochs.
    """
    plt.figure()
    # replace 0 value of moving average with None to avoid plotting 0
    movingAverage = [trainingErrors[i][2] if trainingErrors[i][2] != 0 else None for i in range(len(trainingErrors))]
    plt.plot([round(trainingErrors[i][1]*100, 1) for i in range(len(trainingErrors))], label='Error Percentage (%)')
    plt.plot(
        [i for i in range(len(trainingErrors))],
        [round(ma*100, 1) if ma != None else None for ma in movingAverage],
        label='Moving Average ({})'.format(errorMovingAverage)
    )
    plt.legend()
    if customTitle:
        plt.title(customTitle)
    else:
        plt.title('Training Error over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Error (%)')

def relabel_data(data, prototypes):
    """
    Relabel data according to prototypes.
    """
    newData = data.copy()
    # add column for new labels
    newData = np.append(newData, np.zeros((newData.shape[0], 1)), axis=1)
    for i in range(newData.shape[0]):
        closestPrototype = prototypes[0]
        for j in range(prototypes.shape[0]):
            if eaclidianDistance(newData[i], prototypes[j]) < eaclidianDistance(newData[i], closestPrototype):
                closestPrototype = prototypes[j]
        newData[i][-1] = closestPrototype[-1]
    return newData

def convertLabelToNumber(data):
    """
    Convert labels to integers when lables are given in strings.
    return:
    `data`: data with labels as integers
    `labels`: list of labels with their original name in order of label integers
    """
    # get last column of pandas dataframe
    labels = np.unique(data.iloc[:, -1].values)
    for i in range(data.shape[0]):
        for j in range(len(labels)):
            if data.iloc[i, -1] == labels[j]:
                data.iloc[i, -1] = j
    # convert to numpy array
    data = data.values
    # convert to float
    data = data.astype(float)
    # return data and labels
    return data, labels