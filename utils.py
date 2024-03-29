import numpy as np
import os
import mat73
import config

def load_mat(subject, group):
    file_name = subject + "_AAL94_norm_new_pca-cleaned.mat"
    file_path = os.path.join(config.data_dir, group, file_name)
    data = mat73.loadmat(file_path)
    fsample = int(data['AAL94_norm']['fsample'])
    signal = data['AAL94_norm']['trial'][0] 
    return signal, fsample

def _load_mat(file_path):
    data = mat73.loadmat(file_path)
    fsample = int(data['AAL94_norm']['fsample'])
    signal = data['AAL94_norm']['trial'][0] 
    return signal, fsample

def save_fcs(fcs, subject, group):
    result_dir = os.path.join(config.result_dir, "FUNCONN")
    group_dir = os.path.join(result_dir, group)
    if not os.path.isdir(group_dir): 
        os.mkdir(group_dir)
    file_name = subject + "_func_conn.npz"
    file_path = os.path.join(result_dir, group, file_name)
    np.savez(file_path, **fcs)

def load_fcs(subject, group, norm=False):
    if norm:
        result_dir = os.path.join(config.result_dir, "NORM_FUNCONN")
        file_name = subject + "_norm_func_conn.npz"
    else: 
        result_dir = os.path.join(config.result_dir, "FUNCONN")
        file_name = subject + "_func_conn.npz"
    file_path = os.path.join(result_dir, group, file_name)
    fcs = np.load(file_path)
    return fcs

def save_norm_fcs(fcs, subject, group):
    result_dir = os.path.join(config.result_dir, "NORM_FUNCONN")
    group_dir = os.path.join(result_dir, group)
    if not os.path.isdir(group_dir): 
        os.mkdir(group_dir)
    file_name = subject + "_norm_func_conn.npz"
    file_path = os.path.join(result_dir, group, file_name)
    np.savez(file_path, **fcs)

def save_avg_fcs(fcs, group):
    result_dir = os.path.join(config.result_dir, "AVG_FUNCONN")
    file_name = group + "_avg_func_conn.npz"
    file_path = os.path.join(result_dir, file_name)
    np.savez(file_path, **fcs)

def get_subjects(group): 
    group_dir = os.path.join(config.data_dir, group)
    file_names = os.listdir(group_dir)
    subjects = set([file_name.split("_")[0] for file_name in file_names])
    return subjects

def get_missing_subjects(group): 
    all_subjects = get_subjects(group)
    result_dir = os.path.join(config.result_dir, 'FUNCONN', group)
    file_names = os.listdir(result_dir)
    processed_subjects = [file_name.split("_")[0] for file_name in file_names]
    missing_subjects = [sub for sub in all_subjects if sub not in processed_subjects]
    return missing_subjects

def save_gbc(df):
    out_file = os.path.join(config.result_dir, 'GBC', 'gbc.csv')
    df.to_csv(out_file, index=False)
