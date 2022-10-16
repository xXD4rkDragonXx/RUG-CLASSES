import numpy as np
import matplotlib.pyplot as plt

def load_csv(filename):
    """Load data from csv file."""
    data = np.loadtxt(filename, delimiter=',')
    return data

def divideIntoClasses(data, numClasses, dim):
    """Divide data into classes by adding column with class number."""
    data = np.insert(data, dim, 0, axis=1)
    for i in range(numClasses):
        data[i*(100//numClasses):(i+1)*(100//numClasses), dim] = i
    return data

def initPrototypes(data, numExamples, numPrototypes, dim):
    """
    Initialize prototypes.
    Requires labaled data.
    """
    # sort data by class
    dataSorted = data[data[:,dim].argsort()]
    # get random data point(s) for each class
    prototypes = np.zeros((numPrototypes, dim+1))
    for i in range(numPrototypes):
        prototypes[i] = dataSorted[np.random.randint(i*(numExamples//numPrototypes), (i+1)*(numExamples//numPrototypes)), :dim+1]
    return prototypes

def scatter_plot_data(data):
    """
    Create scatter plot with different colors for different classes.
    Only works for 2D data.
    """	
    plt.scatter(data[:,0], data[:,1], c=data[:,2], cmap='rainbow')

def main():
    """Main function."""
    # Load data
    data = load_csv('lvqdata.csv')
    # get dim and num of examples
    P, N = data.shape
    # set number of prototypes
    K = 4
    # set number of classes
    C = 2
    # set learning rate
    LR = 0.1
    # set max number of epochs
    TMAX = 100
    # divide data into classes
    dataWithClasses = divideIntoClasses(data, C, N)
    # initialize prototypes
    prototypes = initPrototypes(dataWithClasses, P, K, N)

    # plot data
    scatter_plot_data(dataWithClasses)

if __name__ == '__main__':
    main()