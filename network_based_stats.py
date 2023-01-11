import config
from utils import *
from bct.nbs import nbs_bct
import pandas as pd
import numpy as np
from multiprocessing import Pool
import os

def calc_nbs(groups):
    """
    Caculates the NBS of Frequency Ranges defined in config FrequencyBands. 
    Before running this the FC matrices of each group have to be stacked.
    Saves p-val, components and null-samples to NetBasedStats. 
    NBS is calculated in parallel over Frequency bands.
    """
    print('Calculating NBS values')
    # Set seed to make results reproducible
    np.random.seed(0)
    thresholds = [3.0, 2.5, 2.0]   
    
    inputs = [(freq_band, threshold, groups) for freq_band in config.freq_bands for threshold in thresholds]
    print(inputs)
    with Pool(20) as p: 
        dfs = p.starmap(_parallel_nbs, inputs)
    p_results = pd.concat(dfs)
    
    # Save results
    file_name = os.path.join(config.result_dir, 'NBS', f'P-Values_{groups[0]}-{groups[1]}.csv')
    p_results.to_csv(file_name)

		
def _parallel_nbs(freq_band, thresh, groups): 
    """
    Calculates nbs for one Frequency band. Is called in calc_nbs. 
    :return dataframe with pvals of 
    """
    print(f'Processing {freq_band}, Thresh: {thresh}')
    
    freq_key = f"{freq_band[0]}-{freq_band[1]}"
    fc_list = []
    # load functional connectivity matrices
    for group in groups:
        subjects = get_subjects(group)
        n_subjects = len(subjects)
        # NxNxP with P being the number of subjects per group
        fcs = np.empty((94,94,n_subjects))
        for n,sub in enumerate(subjects):
            sub_fcs = load_fcs(sub, group, norm=False)
            fcs[:, :, n] = sub_fcs[freq_key]
        fc_list.append(fcs)

    # calculate nbs
    pval, adj, null = nbs_bct(fc_list[0], fc_list[1], thresh=thresh, k=1000)
    print('Adjacency Shape: ', adj.shape)
    
    p_results = []
    for idx, p in enumerate(pval): 
        result = {'frequency':freq_band, 'threshold':thresh, 'p-val':p, 
                  'index':idx + 1}
        p_results.append(result)

    # Save component file and null sample
    component_file = os.path.join(config.result_dir, 'NBS', f'Component-Adj_freq-{freq_band}_thresh-{thresh}.npy')
    np.save(component_file, adj)
    
    null_file = os.path.join(config.result_dir, 'NBS', f'Null-Sample_freq-{freq_band}_thresh-{thresh}.npy')
    np.save(null_file, null)
    
    # Return dataframe 
    df = pd.DataFrame(p_results, index=False)
    return df