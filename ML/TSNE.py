import matplotlib.pyplot as plt
import scipy.io as sio
from sklearn.manifold import TSNE

# reduce data dimensionality of the data to 40 using t-SNE and plot the results.
# load COIL20 dataset from matlab file
coil20 = sio.loadmat('COIL20.mat')
# extract data and labels
data = coil20['X']
labels = coil20['Y']

# perform t-SNE
tsne = TSNE()
data_tsne = tsne.fit_transform(data)

# plot the data
plt.figure()
plt.title('t-SNE')
plt.scatter(data_tsne[:,0], data_tsne[:,1], c=labels)
plt.show()