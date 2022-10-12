import numpy as np
import matplotlib.pyplot as plt

def plotData(data, endPrototypes=None, trajectories=None, startPosPrototypes=None, title="Chart"):
    # initialize legend
    legend = []
    # plot data
    plt.scatter(data[:,0], data[:,1], marker='o', color='black')
    legend.append('Data')
    # plot trajectories if given
    if trajectories is not None:
        for i in trajectories:
            plt.plot(*zip(*trajectories[i]), 'r--')
            legend.append('Trajectory prototype {}'.format(i + 1))
    # plot prototypes if given
    if endPrototypes is not None:
        plt.scatter(endPrototypes[:,0], endPrototypes[:,1], marker='o', color='red')
        legend.append('End Prototypes')
    # plot start position of prototypes if given
    if startPosPrototypes is not None:
        plt.scatter(startPosPrototypes[:,0], startPosPrototypes[:,1], marker='o', color='green')
        legend.append('Start Prototypes')
    plt.legend(legend)
    plt.title(title)

def plotError(error, title="Error", movingAverage=0):
    legend = []
    # plot error
    plt.figure()
    plt.plot(error)
    legend.append('Error')
    # add moving average
    if movingAverage > 0:
        plt.plot(np.convolve(error, np.ones((movingAverage,))/movingAverage, mode='valid'))
        legend.append('Moving Average')
    plt.legend(legend)
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Quantization Error')

def applyVQ(data, prototypes, maxEpochs=100, learningRate=0.1, randomizeData=True):
    # initialize variables
    epoch = 0
    # initialize trajectories using disct and index of prototypes as keys
    trajectories = {i:[prototypes[i].copy()] for i in range(len(prototypes))}
    prototypes = prototypes.copy()
    # save first quantization Error
    quantizationError = np.sum(np.linalg.norm(data - prototypes[np.argmin(np.linalg.norm(prototypes - data[:,None], axis=2), axis=1)], axis=1))
    quantizationErrorHistory = [quantizationError]
    # loop until max epochs reached
    while epoch < maxEpochs:
        # get old prototypes
        # randomize data if required
        if randomizeData:
            np.random.shuffle(data)
        # loop over data
        for x in data:
            # get index of nearest prototype
            index = np.argmin(np.linalg.norm((prototypes - x)**2, axis=1))
            # update prototype
            prototypes[index] = prototypes[index] + learningRate * (x - prototypes[index])
        # get new prototypes
        newPrototypes = prototypes.copy()
        # go through all prototypes
        for i in range(len(prototypes)):
            trajectories[i].append(newPrototypes[i])
        # calculate quantization error
        quantizationError = np.sum(np.linalg.norm(data - prototypes[np.argmin(np.linalg.norm(prototypes - data[:,None], axis=2), axis=1)], axis=1))
        # save quantization error
        quantizationErrorHistory.append(quantizationError)
        # increase epoch
        epoch += 1
    # return trajectories and prototypes
    return trajectories, prototypes, quantizationErrorHistory

def main():
    # set random seed
    np.random.seed(43)
    # Load csv 2-dim data
    data = np.loadtxt('simplevqdata.csv', delimiter=',')
    # set parameters
    maxEpochs = 10
    learningRate = 0.1
    numPrototypes = 2
    # get prototypes by random sampling
    prototypes = data[np.random.choice(len(data), numPrototypes, replace=False)]
    # apply VQ
    trajectories, endPrototypes, errorHistory = applyVQ(data, prototypes.copy(), maxEpochs=maxEpochs, learningRate=learningRate)
    # plot results
    plotData(
        data,
        endPrototypes,
        trajectories,
        prototypes,
        title="VQ Learning {} Epochs, {} Learning Rate and {} prototypes".format(maxEpochs, learningRate, numPrototypes)
    )
    # plot error
    plotError(errorHistory)
    plt.show()

if __name__ == '__main__':
    main()