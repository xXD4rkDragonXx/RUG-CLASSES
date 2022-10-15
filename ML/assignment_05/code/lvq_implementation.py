import numpy as np
import matplotlib.pyplot as plt

# Load csv data
def load_csv(filename):
    data = np.loadtxt(filename, delimiter=',')
    return data

# Divide data into classes by adding column with class number
def divideIntoClasses(data, numClasses):
    data = np.insert(data, 2, 0, axis=1)
    for i in range(numClasses):
        data[i*(100//numClasses):(i+1)*(100//numClasses), 2] = i
    return data

# plot data
def plot_data(data):
    plt.scatter(data[:,0], data[:,1], c=data[:,2], cmap='rainbow')
    plt.show()

# plot data
def main():
    # Load data
    data = load_csv('lvqdata.csv')
    data = divideIntoClasses(data, 2)
    plot_data(data)

if __name__ == '__main__':
    main()