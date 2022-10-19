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

def lvq1(data, prototypes, LR, maxEpochs, random=True, stopWhenStable=False, stableMovingAverage=5):
    """
    Execute Learning Vector Quantization 1.
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
            # get closest prototype
            closestPrototype = prototypes[0]
            for j in range(prototypes.shape[0]):
                if eaclidianDistance(data[i], prototypes[j]) < eaclidianDistance(data[i], closestPrototype):
                    closestPrototype = prototypes[j]
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
        
    return prototypes, trainingErrors, prototypePositionHistory

def plotErrorOverEpochs(trainingErrors, errorMovingAverage=5, customTitle=None):
    """
    Plot training error over epochs.
    """
    plt.figure()
    # replace 0 value of moving average with None to avoid plotting 0
    movingAverage = [trainingErrors[i][2] if trainingErrors[i][2] != 0 else None for i in range(len(trainingErrors))]
    plt.plot([trainingErrors[i][1] for i in range(len(trainingErrors))], label='Error Percentage')
    plt.plot([i for i in range(len(trainingErrors))], movingAverage, label='Moving Average ({})'.format(errorMovingAverage))
    plt.legend()
    if customTitle:
        plt.title(customTitle)
    else:
        plt.title('Training Error over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Error')

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
    Convert labels to numbers.
    return:
    `data`: data with labels as numbers
    `labels`: list of labels
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

def main():
    """Main function."""
    # set seed for repeated results
    np.random.seed(42)
    # Load data
    data = loadCSV('lvqdata.csv')
    # get dim and num of examples
    P, N = data.shape
    # set number of prototypes
    K = 4
    # set number of classes
    C = 2
    # set learning rate
    LR = 0.002
    # set max number of epochs
    TMAX = 500
    # divide data into classes
    dataWithClasses = divideIntoClasses(data, C, N)

    # initialize prototypes
    prototypes = initPrototypes(dataWithClasses, P, K, N, initAtClassMean=False)
    
    legendInfo = []
    plt.figure()
    # execute learning vector quantization 1
    newPrototypes, trainingErrors, prototypePositionHistory = lvq1(dataWithClasses, prototypes, LR, TMAX, stopWhenStable=True, stableMovingAverage=10)
    # plot data with different colors for different classes
    legendInfo.append(scatterPlotData(dataWithClasses))
    # add prototypes
    legendInfo.append(scatterPlotPrototypes(newPrototypes))
    # add prototypes trajectory
    legendInfo.append(scatterPlotPrototypeTrajectory(prototypePositionHistory)[0])
    # set title
    plt.title('LVQ1 with {} prototypes, {} classes and {} learning rate'.format(K, C, LR))
    # add legend to plot 
    plt.legend(handles=legendInfo)

    # plot new data with different colors for different classes
    plt.figure()
    newData = relabel_data(data, newPrototypes)
    scatterPlotData(newData)
    # add prototypes
    scatterPlotPrototypes(newPrototypes)
    plt.title('LVQ1 with {} prototypes, {} classes and {} learning rate'.format(K, C, LR))
    plt.legend()

    # plot error over epochs
    plotErrorOverEpochs(trainingErrors, errorMovingAverage=10)

    # import iris data
    irisData = loadCSV('iris.csv', includesText=True)
    # get dim and num of examples
    P = irisData.shape[0]
    N = irisData.shape[1] - 1
    # convert lable name to number
    newIrisData, lableNames = convertLabelToNumber(irisData)
    # set number of prototypes
    K = 6
    # set learning rate
    LR = 0.005
    # set max number of epochs
    TMAX = 500
    # generate prototypes
    prototypes = initPrototypes(newIrisData, P, K, N)
    # execute learning vector quantization 1
    newPrototypes, trainingErrors, prototypePositionHistory = lvq1(newIrisData, prototypes, LR, TMAX, stopWhenStable=True, stableMovingAverage=10)
    # plot error over epochs
    plotErrorOverEpochs(trainingErrors, errorMovingAverage=10, customTitle='Iris Data Error over Epochs')

    # show all plots
    plt.show()

if __name__ == '__main__':
    main()