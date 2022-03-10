import numpy as np
import os
import mat73

# data_dir = "/mnt/raid/data/SFB1315/Uhlhaas_MEG/VIRTCHAN/DATA"
data_dir = "C:\\Users\\Kamp\\Documents\\scz\\data"
# result_dir = "/mnt/raid/data/SFB1315/Uhlhaas_MEG/RESULTS/FUNCONN"
result_dir = "C:\\Users\\Kamp\\Documents\\scz\\results"

def load_mat(subject, group):
    file_name = subject + "_AAL94_norm_new.mat"
    file_path = os.path.join(data_dir, group, file_name)
    data = mat73.loadmat(file_path)
    fsample = int(data['AAL94_norm']['fsample'])
    signal = data['AAL94_norm']['trial'][0] 
    return signal, fsample

def save_fcs(fcs, subject, group):
    result_dir = os.path.join(result_dir, "FUNCONN")
    group_dir = os.path.join(result_dir, group)
    if not os.path.isdir(group_dir): 
        os.mkdir(group_dir)
    file_name = subject + "_func_conn.npz"
    file_path = os.path.join(result_dir, group, file_name)
    np.savez(file_path, **fcs)

def save_norm_fcs(fcs, subject, group):
    result_dir = os.path.join(result_dir, "NORM_FUNCONN")
    group_dir = os.path.join(result_dir, group)
    if not os.path.isdir(group_dir): 
        os.mkdir(group_dir)
    file_name = subject + "_norm_func_conn.npz"
    file_path = os.path.join(result_dir, group, file_name)
    np.savez(file_path, **fcs)

def get_subjects(group): 
    group_dir = os.path.join(data_dir, group)
    file_names = os.listdir(group_dir)
    subjects = [file_name.split("_")[0] for file_name in file_names]
    return subjects
        