
session = labels[:,1]
# final matrix should match length of label/session vector
print X.shape, len(labels[:,0])

# current shape: first axis = 582, second axis = XYZ voxels TR_n
# needed shape: first axis = 58*, second axis = XYZ voxels TR_n-2 + XYZ voxels TR_n-1 + XYZ voxels TR_n
# the window needs to take the four different runs into account and not overlap TRs from different runs

def window_3TR(X, session, runs):
    W = np.zeros((1, X.shape[1]*3))
    for r in range(runs):
        r = str(r)
        w1 = None
        w2 = None
        w3 = None
        w4 = None
        W_i = np.zeros((1, X.shape[1]*3))
        for idx2, i2 in enumerate(session):
            if i2 == r:
                w1 = X[idx2-2]
                w2 = X[idx2-1]
                w3 = X[idx2]
                w4 = np.hstack((w1, w2, w3))
                W_i = np.vstack((W_i, w4))
        print 'w_i', W_i.shape
        W_i = W_i[1:,:]
        W = np.vstack((W, W_i))
    W = W[1:,:]
    print 'W final', W.shape
        
window_3TR(X, session, 4)
