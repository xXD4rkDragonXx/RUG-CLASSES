import numpy as np
import matplotlib.pyplot as plt

def plotData(
        data,
        endPrototypes=None,
        trajectories=None,
        startPosPrototypes=None,
        title="Chart",
        saveToFile=False,
        fileName="chart.png"
    ):
    # initialize legend
    legend = []
    # plot data
    plt.scatter(data[:,0], data[:,1], marker='o', color='black')
    legend.append('Data')
    # plot trajectories if given
    if trajectories is not None:
        for i in trajectories:
            plt.plot(*zip(*trajectories[i]), 'r--')
            legend.append('Trajectory {}'.format(i + 1))
    # plot start position of prototypes if given
    if startPosPrototypes is not None:
        plt.scatter(startPosPrototypes[:,0], startPosPrototypes[:,1], marker='o', color='green')
        legend.append('Start Prototypes')
    # plot prototypes if given
    if endPrototypes is not None:
        plt.scatter(endPrototypes[:,0], endPrototypes[:,1], marker='o', color='red')
        legend.append('End Prototypes')
    # set size of plot
    plt.gcf().set_size_inches(10, 5)
    plt.legend(legend, loc='upper right')
    plt.title(title)
    if(saveToFile):
        plt.savefig(fileName)

def plotError(
        error,
        title="Error",
        movingAverage=0,
        saveToFile=False,
        fileName="error.png"
    ):
    legend = []
    # plot error
    plt.figure()
    plt.plot(error)
    legend.append('Error')
    # draw horizontal line at minimum
    # and show value to the right of the plot
    plt.axhline(y=min(error), color='r', linestyle='--')
    plt.text(len(error) - 1, min(error), "Min: {:.0f}".format(min(error)))
    # highlight minimum
    plt.scatter(error.index(min(error)), min(error), marker='o', color='red')
    # add moving average
    if movingAverage > 0:
        plt.plot(np.convolve(error, np.ones((movingAverage,))/movingAverage, mode='valid'))
        legend.append('Moving Average')
    plt.legend(legend)
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Quantization Error')
    if(saveToFile):
        plt.savefig(fileName)

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

def generateVQPlots(k=[2,4], maxEpochs=10, learningRates=[0.1, 0.05, 0.01], randomizeData=True, randomSeed=None):
    # set random seed if given
    if randomSeed is not None:
        np.random.seed(randomSeed)
    # Load csv 2-dim data
    data = np.loadtxt('simplevqdata.csv', delimiter=',')
    # loop over k
    for i in k:
        # get prototypes by random sampling
        prototypes = data[np.random.choice(len(data), i, replace=False)]
        # loop over learning rates
        for j in learningRates:
            # apply VQ
            trajectories, endPrototypes, errorHistory = applyVQ(data, prototypes.copy(), maxEpochs=maxEpochs, learningRate=j, randomizeData=randomizeData)
            # plot results
            plotData(
                data,
                endPrototypes,
                trajectories,
                prototypes,
                title="VQ Learning {} Epochs, {} Learning Rate and {} prototypes".format(maxEpochs, j, i),
                saveToFile=True,
                fileName="output/vq-learning_e{}_K{}_LR{}.png".format(maxEpochs, j, i)
            )
            # plot error
            plotError(
                errorHistory,
                title="Error {} Epochs, {} Learning Rate and {} prototypes".format(maxEpochs, j, i),
                saveToFile=True,
                fileName="output/error_e{}_K{}_LR{}.png".format(maxEpochs, j, i)
            )

def main():
    learningRates = [0.1, 0.07, 0.05, 0.03, 0.01, 0.005, 0.001]
    K = [2, 4]
    # generate plots
    generateVQPlots(
        k=K,
        maxEpochs=100,
        learningRates=learningRates,
        randomizeData=True,
        randomSeed=42
    )
    plt.show()

if __name__ == '__main__':
    main()