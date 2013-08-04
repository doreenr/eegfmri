
print X.shape

# current shape: first axis = 582, second axis = XYZ voxels TR_n
# needed shape: first axis = 582, second axis = XYZ voxels TR_n-2 + XYZ voxels TR_n-1 + XYZ voxels TR_n

def window_3TR(X):
    W = np.zeros((1, X.shape[1]*3))
    for idx, i in enumerate(X):
        if idx > 1:
            w1 = X[idx-2]
            w2 = X[idx-1]
            w3 = X[idx]
            w4 = np.hstack((w1, w2, w3))
            W = np.vstack((W, w4))
    W = W[1:,:]
    print W.shape
        
window_3TR(X)