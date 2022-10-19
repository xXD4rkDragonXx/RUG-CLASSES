import numpy as np
import matplotlib.pyplot as plt

# import LVQ python file
from lvq import *

def main():
    """Main function."""
    # set seed for repeated results
    np.random.seed(42)
    # Load data
    data = loadCSV('lvqdata.csv')
    # get dim and num of examples
    P, N = data.shape
    # set number of prototypes
    K = 2
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
    newPrototypes, trainingErrors, prototypePositionHistory = lvq('lvq1', dataWithClasses, prototypes, LR, TMAX, stopWhenStable=True, stableMovingAverage=20)
    # plot data with different colors for different classes
    legendInfo.append(scatterPlotData(dataWithClasses))
    # add prototypes
    legendInfo.append(scatterPlotPrototypes(newPrototypes))
    # add prototypes trajectory
    legendInfo.append(scatterPlotPrototypeTrajectory(prototypePositionHistory)[0])
    # set title
    plt.title('LVQ1 with {} prototypes, {} classes and {} learning rate'.format(K, C, LR))
    # save plot
    plt.savefig('output/lvq1_{}_{}_{}.png'.format(K, C, LR))
    # add legend to plot 
    plt.legend(handles=legendInfo)

    # plot new data with different colors for different classes
    plt.figure()
    newData = relabel_data(data, newPrototypes)
    scatterPlotData(newData)
    # add prototypes
    scatterPlotPrototypes(newPrototypes)
    plt.title('LVQ1 with {} prototypes, {} classes and {} learning rate'.format(K, C, LR))
    # save plot
    plt.savefig('output/lvq1_{}_{}_{}_new_labels.png'.format(K, C, LR))
    plt.legend()

    # plot error over epochs
    plotErrorOverEpochs(trainingErrors, errorMovingAverage=10, customTitle='LVQ1 with {} prototypes, {} classes and {} learning rate'.format(K, C, LR))
    # save plot
    plt.savefig('output/lvq1_error_{}_{}_{}.png'.format(K, C, LR))

    # show all plots
    plt.show()

if __name__ == '__main__':
    main()