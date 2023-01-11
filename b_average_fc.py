import numpy as np
from utils import *
from func_conn import *
import config

if __name__ == '__main__':
    for group in config.groups:
        try: 
            avg_fcs = get_group_fcs(group)
            save_avg_fcs(avg_fcs, group)
        except: 
            print(f"Couldn't calculate average functional connectivity for group {group}")