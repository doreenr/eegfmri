
# Get subjectinfo for first_level_ev

def get_subjectinfo(subject_id):
    runs = 4
    for r in range(runs):            
        path = '/gablab/p/eegfmri/analysis/eeg/elists'
        path_names = os.path.join(path, 'elist_IAPS_%s_%s_raw.txt' %(subject_id, r+1))
        if subject_id == '005' and r == 1:
            path_names = os.path.join(path, 'elist_IAPS_%s_%s_2_raw.txt' %(subject_id, r+1))
        if subject_id == '009':
            path_names = os.path.join(path, 'elist_IAPS_%s_%s.txt' %(subject_id, r+1))            
        run_code = np.genfromtxt(path_names, dtype=str) [:,3]
        unique = sorted(list(set(run_code)))
        clock = np.genfromtxt(path_names, dtype=str) [:,4] 
        f = open('/gablab/p/eegfmri/analysis/iaps/pilot%s/cond_neg_run%s.txt' %(subject_id, r), 'w')
        for idx2, i2 in enumerate(run_code):
            if i2.startswith('S') and i2 != 'SyncOn' and i2 != 'Start':
                i2 = int(i2.lstrip('S'))
                if i2 < 121:
                    f.write("%s, 2, 1" %(clock[idx2]))
                    f.write('\n') 
        f.close()
        t = open('/gablab/p/eegfmri/analysis/iaps/pilot%s/cond_neut_run%s.txt' %(subject_id, r), 'w')
        for idx2, i2 in enumerate(run_code):
            if i2.startswith('S') and i2 != 'SyncOn' and i2 != 'Start':
                i2 = int(i2.lstrip('S'))
                if i2 >= 121:
                    t.write("%s, 2, 1" %(clock[idx2]))
                    t.write('\n')
        t.close()
        
a = get_subjectinfo('004')
b = get_subjectinfo('005')        
c = get_subjectinfo('006')        
d = get_subjectinfo('007')        
e = get_subjectinfo('008')        
f = get_subjectinfo('009')        
g = get_subjectinfo('011')        
h = get_subjectinfo('012')        
i = get_subjectinfo('013')        