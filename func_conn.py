import numpy as np
from mne.filter import filter_data, next_fast_len
from scipy.signal import hilbert
from scipy.signal import resample
import scipy.stats
from multiprocessing import Pool
from config import *
from utils import get_subjects, load_fcs

def pearson_mat(m1,m2):
    """
    Computes Correlation matrix 
    """
    n = m1.shape[1]

    m1 -= np.mean(m1, axis=-1, keepdims=True)
    std_m1 = np.std(m1, axis=-1, keepdims=True)
    std_m1[np.isclose(std_m1,0)] = 1
    m1 /= std_m1

    m2 -= np.mean(m2, axis=-1, keepdims=True)
    std_m2 = np.std(m2, axis=-1, keepdims=True)
    std_m2[np.isclose(std_m2,0)] = 1
    m2 /= std_m2

    corr = np.matmul(m1,m2.T)/n 
    return corr

def get_freq_band(data, fsample, limits):
    """
    Band pass filters signal from each region
    :param fsample: sampling frequency
    :param limits: int, specifies limits of the frequency band
    :return: filter Signal
    """
    lowerfreq = limits[0]
    upperfreq = limits[1]
    filtered_signal = filter_data(data, fsample, l_freq=lowerfreq, h_freq=upperfreq,
                                fir_window='hamming', verbose=False)
    return filtered_signal

def get_envelope(data, fsample, limits):
    """
    Calculates the envelope of the data in the frequency range
    """
    _, time_points = data.shape
    filtered_signal = get_freq_band(data, fsample, limits)
    n_fft = next_fast_len(time_points)
    complex_signal = hilbert(filtered_signal, N=n_fft, axis=-1)
    filtered_envelope = np.abs(complex_signal)
    return filtered_envelope

def resampleSignal(data, fsample, resample_num=None, target_freq=None):
    """
    Resamples Signal to number of resample points or to target frequency
    """
    if target_freq is not None:
        resampling_factor = target_freq/fsample
        resample_num = int(data.shape[1]*resampling_factor)
    
    # Resample
    re_signal = resample(data, num=resample_num, axis=-1)
    
    return re_signal

def get_env_fc(data, fsample, limits, processes=2, lowpass=None, demean=True):
    """
    Computes the Functional Connectivity Matrix based on the signal envelope
    Takes settings from configuration File. 
    """
    _, time_points = data.shape
    # Filter signal
    filtered_signal = get_freq_band(data, fsample, limits)

    # Get complex signal
    n_fft = next_fast_len(time_points)
    complex_signal = hilbert(filtered_signal, N=n_fft, axis=-1)[:, :time_points]
    
    #pad=100
    #complex_signal = complex_signal[:,pad:-pad]
    
    signal_conj = complex_signal.conj()

    # Get signal envelope
    signal_env = np.abs(complex_signal)
    
    # Precompute the ratio between conj and envelope
    conj_div_env = signal_conj/signal_env 

    # Compute orthogonalization and correlation in parallel		
    with Pool(processes=processes) as p: 
        result = p.starmap(_parallel_orth_corr, [(complex, signal_env, conj_div_env, fsample, lowpass, demean) 
                                                for complex in complex_signal])
    FC = np.array(result)

    # Make the Corr Matrix symmetric
    FC = (FC.T + FC) / 2.
    return FC

def _parallel_orth_corr(complex_signal, signal_env, conj_div_env, fsample, lowpass, demean):
    """
    Computes orthogonalized correlation of the envelope of the complex signal (nx1 dim array) and the signal envelope  (nxm dim array). 
    """
    # Orthogonalize signal
    orth_signal = (complex_signal * conj_div_env).imag
    orth_env = np.abs(orth_signal)

    if demean:
        orth_signal -= np.mean(orth_signal, axis=-1, keepdims=True)
        orth_env -= np.mean(orth_env, axis=-1, keepdims=True)

    # Envelope Correlation
    if lowpass is not None:
        # Low-Pass filter
        orth_env = filter_data(orth_env, fsample, 0, lowpass, fir_window='hamming', verbose=False)
        signal_env = filter_data(signal_env, fsample, 0, lowpass, fir_window='hamming', verbose=False)	
    
    corr_mat = pearson_mat(orth_env, signal_env)	
    corr = np.diag(corr_mat)
    return corr

def normalize_fc(fc): 
    """
    Normalizes the functional connectivity matrix
    """
    normalize_fc = np.zeros_like(fc)
    n = normalize_fc.shape[0]
    triu = np.triu_indices(n, k=1)
    tril = np.tril_indices(n, k=-1)
    normalize_fc[triu] = scipy.stats.zscore(fc[triu])
    normalize_fc[tril] = scipy.stats.zscore(fc[tril])
    return normalize_fc

def get_group_fcs(group): 
    """
    Calculates the mean functional connectivity of the group.
    """
    subjects = get_subjects(group)
    n_subjects = len(subjects)
    avg_fcs = {}
    for limits in freq_bands:
        fcs = np.empty((n_subjects, 94, 94))
        freq_key = f"{limits[0]}-{limits[1]}"
        mask = np.ones(fcs.shape[0], bool)
        for n, sub in enumerate(subjects):  
            try:  
                sub_fcs = load_fcs(sub, group, norm=False)
                fcs[n, :, :] = sub_fcs[freq_key]
            except: 
                print(f'Group {group}, Subject {sub} not found.')
                mask[n] = False
        fcs = fcs[mask, :, :]
        avg_fc = np.mean(fcs, axis=0)
        avg_fcs[freq_key] = avg_fc
    return avg_fcs