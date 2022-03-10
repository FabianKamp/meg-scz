import numpy as np
import itertools
from utils import *
from func_conn import *

####################################
# Define group and frequency bands #
####################################

group = 'HC'
freq_bands = [[1,3], [4,7], [8,12], [18, 22], [30,46], [64,90]] 
subjects = get_subjects(group)[:1]

if __name__ == '__main__':
    for subject in subjects:
        print(f'Processing Subject: {subject}')
        data, fsample = load_mat(subject, group)        
        fcs = {}
        norm_fcs = {} 
        for limits in freq_bands:
            freq_key = f"{limits[0]}-{limits[1]}"
            # calculate the functional connectivity
            fc = get_env_fc(data, fsample, limits, processes=3)
            # normalize the connectivity
            norm_fc = normalize_fc(fc)

            fcs[freq_key] = fc
            norm_fcs[freq_key] = norm_fc

        save_fcs(fcs, subject, group)
        save_norm_fcs(norm_fcs, subject, group)


    
