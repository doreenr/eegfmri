
def create_dataset(subject_id):
    import numpy as np
    import os 
    from nilearn import datasets
    from nilearn.datasets import _get_dataset_dir
    from nilearn.datasets import _get_dataset
    from sklearn.datasets.base import Bunch
    import pylab as pl
    import nibabel as nb
    
    from remove import remove_range, remove

    dataset_name = 'machine_learning'
    runs = 4
    img_data = np.zeros((64,64,33,1))
    lab_data = []
    session_data = []
    for r in range(runs):
        print 'RUN', r
        rv = None
        path = '/gablab/p/eegfmri/analysis/eeg/elists'
        path_all_codes = '/gablab/p/eegfmri/analysis/iaps/all_labels.txt'
        path_names2 = os.path.join(path, 'elist_IAPS_%s_%s_raw.txt' %(subject_id, r+1))
        if subject_id == '009':
            path_names2 = os.path.join(path, 'elist_IAPS_%s_%s.txt' %(subject_id, r+1)) 
        eegcodes = np.genfromtxt(path_all_codes, dtype=int) [:, 0]
        attributes = np.genfromtxt(path_all_codes, dtype=float) [:, 1:4]
        binary = attributes[:, 2]
        run_code = np.genfromtxt(path_names2, dtype=str) [:,3]
        clock = np.genfromtxt(path_names2, dtype=str) [:,4] 
        cl = []
        tp = []
        for i in range(len(clock)):
            if run_code[i] == 'R128':
                timepoint = clock[i].lstrip('0123456789')  
                tp.append(timepoint)            
            if len(tp) > 0:
                clock[i] = clock[i].lstrip('0123456789')
                if clock[i] == tp[0]:
                    cl.append([i])
                    if run_code[i] != 'R128':
                        print i, run_code[i] 
                if clock[i] != tp[0] and run_code[i] == 'R128':
                    print 'TR at index', i, 'removed.'
                    run_code[i] = 'remove'
        print 'Numbers of TR identical timepoints', len(cl)
        tr = []
        for idx,i in enumerate(run_code):
            if i == 'R128':
                tr.append([idx])
        print 'Number of TR counted from elist code', len(tr)
        rv = remove(run_code, 'R')
        rv = remove(rv, 'remove')
        rv = remove(rv, 'boundary')
        rv = remove(rv, 'SyncOn')
        rv = remove(rv, 'Start')
        rv = remove(rv, 'Userdefined')
        rv = remove(rv, 'LowCorrelation')
        rv = remove(rv, 'TSTART')
        rv = remove(rv, 'TPEAK')
        rv = remove(rv, 'TEND')
        for i in range(len(rv)):
            if rv[i] == 'R128':
                rv[i] = '-99'
            rv[i] = rv[i].lstrip('S')
            rv[i] = int(rv[i])
        # remove stimulus codes for responses
        rv = remove_range(rv, 240)
        for idx, i in enumerate(rv):
            for idx2, i2 in enumerate(eegcodes):
                if i == i2:
                    rv[idx] = binary[idx2]            
        for idx, i in enumerate(rv):
            if i != -99:
                rv[idx-1] = i
                rv[idx] = 0
        # remove last TR as it was apparently not recorded
        rv[-1] = 0
        rv = remove(rv, 0)
        for idx, i in enumerate(rv):
            if i == -99:
                rv[idx] = 0
        unique = sorted(list(set(rv)))
        print 'Unique values in RV', unique  
        
        # until now the list with the negative / neutral labels also contains zeros, which we will want to get rid of. 
        # To do this, we will replace the zeros with the code shown prior
        # First two values will be deleted later
        
        for idx, z in enumerate(rv):
            if idx <= 2 and z == 0:
                rv[idx] = -77
            if idx > 2 and z == 0:
                rv[idx] = rv[idx-1]
        unique = sorted(list(set(rv)))
        print 'Unique values in RV', unique  
        
        t = open('/gablab/p/eegfmri/analysis/iaps/pilot%s/machine_learning/neg-neutr_attributes_run%s.txt' %(subject_id, r), 'w')
        for i in range(len(rv)):
            t.write("%s, %s" %(rv[i], r))
            t.write('\n')  
        t.close()
        print 'Labels Length:', len(rv)
        file_name = ['neg-neutr_attributes_run%s.txt' %(r), 'pilot%s_r0%s_bandpassed.nii.gz' %(subject_id, r)]
        fil = _get_dataset(dataset_name, file_name, data_dir='/gablab/p/eegfmri/analysis/iaps/pilot%s' %(subject_id), folder=None)
        ds_i = Bunch(func=fil[1], conditions_target=fil[0])
        labels_i = np.loadtxt(ds_i.conditions_target, dtype=np.str)
        bold_i = nb.load(ds_i.func)
        fmri_data_i = np.copy(bold_i.get_data())
        print 'fMRI data', fmri_data_i.shape
        affine = bold_i.get_affine()
        mean_img_i = np.mean(fmri_data_i, axis=3)
        session_data = np.append(session_data, labels_i[:,1])
        lab_data = np.append(lab_data, labels_i[:,0])
        img_data = np.concatenate((img_data, fmri_data_i), axis=3)        
        print '__________________________________________________________________________________________________________'
        if r == 3:
            img_data = img_data[...,1:]
            print 'fMRI image', img_data.shape
            print 'Label Vector Length:', len(lab_data), 'Session Vector Length:', len(session_data)
            ni_img = nb.Nifti1Image(img_data, affine=None, header=None)
            nb.save(ni_img, '/gablab/p/eegfmri/analysis/iaps/pilot%s/machine_learning/all_runs.nii' %(subject_id))
            f = open('/gablab/p/eegfmri/analysis/iaps/pilot%s/machine_learning/neg-neutr_attributes_all_runs.txt' %(subject_id), 'w')
            for i in range(len(lab_data)):
                f.write("%s %s" %(lab_data[i], session_data[i]))
                f.write('\n')  
            f.close()
            # set up concatenated dataset in nilearn format
            file_names = ['neg-neutr_attributes_all_runs.txt', 'all_runs.nii']
            files = _get_dataset(dataset_name, file_names, data_dir='/gablab/p/eegfmri/analysis/iaps/pilot%s' %(subject_id), folder=None)
            ds = Bunch(func=files[1], conditions_target=files[0])
            print ds.keys(), ds
            labels = np.loadtxt(ds.conditions_target, dtype=np.str)
            bold = nb.load(ds.func)
            fmri_data = np.copy(bold.get_data())
            print fmri_data.shape
            affine = bold_i.get_affine() # just choose one
            # Compute the mean EPI: we do the mean along the axis 3, which is time
            mean_img = np.mean(fmri_data, axis=3)
    return (ds, labels, bold, fmri_data, affine, mean_img)

ds, labels, bold, fmri_data, affine, mean_img = create_dataset('011')
