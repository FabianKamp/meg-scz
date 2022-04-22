import numpy as np
from utils import *
from func_conn import *
import config
from network_based_stats import calc_nbs

steps = ['nbs']

if __name__ == '__main__':
    # average fc
    if 'average' in steps:
        print('Calculating average')
        for group in config.groups:
            try: 
                avg_fcs = get_group_fcs(group)
                save_avg_fcs(avg_fcs, group)
            except: 
                print(f"Couldn't calculate average functional connectivity for group {group}.")
    # gbc
    if 'gbc' in steps:
        print('Calculating GBC')
        gbc = get_gbc()
        save_gbc(gbc)
    
    # nbs
    if 'nbs' in steps:
        print('Calculating NBS')
        calc_nbs(['HC', 'FEP'])