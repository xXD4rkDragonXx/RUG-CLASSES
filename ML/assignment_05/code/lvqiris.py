import numpy as np
import matplotlib.pyplot as plt

# import LVQ python file
from lvq import *

def main():
    """Main function."""
    # set seed for repeated results
    np.random.seed(42)
    # import iris data
    irisData = loadCSV('iris.csv', includesText=True)
    # get dim and num of examples
    P = irisData.shape[0]
    N = irisData.shape[1] - 1
    # convert lable name to number
    newIrisData, lableNames = convertLabelToNumber(irisData)
    # set number of prototypes
    K = 3
    # set learning rate
    LR = 0.005
    # set max number of epochs
    TMAX = 500
    # generate prototypes
    prototypes = initPrototypes(newIrisData, P, K, N)
    # execute learning vector quantization 1
    newPrototypes, trainingErrors, prototypePositionHistory = lvq('lvq1', newIrisData, prototypes, LR, TMAX, stopWhenStable=True, stableMovingAverage=10)
    # plot error over epochs
    plotErrorOverEpochs(trainingErrors, errorMovingAverage=10, customTitle='Iris Data Error, {} dimentions {} prototypes and {} learning rate'.format(N, K, LR))
    # save plot
    plt.savefig('output/lvq1_error_iris_{}_{}.png'.format(K, LR))

    # show all plots
    plt.show()

if __name__ == '__main__':
    main()