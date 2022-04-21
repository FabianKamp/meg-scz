import numpy as np
from utils import *
from func_conn import *
import config

# subjects = get_missing_subjects(config.group)
subjects = get_subjects(config.group)
print(subjects)

if __name__ == '__main__':
    for subject in subjects:
        print(f'Processing Subject: {subject}')
        data, fsample = load_mat(subject, config.group)        
        fcs = {}
        norm_fcs = {} 
        for limits in config.freq_bands:
            freq_key = f"{limits[0]}-{limits[1]}"
            # calculate the functional connectivity
            fc = get_env_fc(data, fsample, limits, processes=10)
            # normalize the connectivity
            norm_fc = normalize_fc(fc)

            fcs[freq_key] = fc
            norm_fcs[freq_key] = norm_fc

        save_fcs(fcs, subject, config.group)
        save_norm_fcs(norm_fcs, subject, config.group)


    
