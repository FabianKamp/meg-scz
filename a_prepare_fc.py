import numpy as np
from utils import *
from func_conn import *
from config import *


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


    
