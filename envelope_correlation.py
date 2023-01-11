import numpy as np
from mne.filter import next_fast_len, filter_data


def envelope_correlation(data,
                         log=False, absolute=True,
                         lowpass_freq=None, fsample=None):
    """Compute the envelope correlation.

    Parameters
    ----------
    data : array-like, shape=(n_signals, n_times) 
        The data from which to compute connectivity.
    names : list | array-like | None
        A list of names associated with the signals in ``data``.
        If None, will be a list of indices of the number of nodes.
    log : bool
        If True (default False), square and take the log before orthonalizing
        envelopes or computing correlations.
    absolute : bool
        If True (default), then take the absolute value of correlation
        coefficients before making each epoch's correlation matrix
        symmetric (and thus before combining matrices across epochs).

    Returns
    -------
    corr : instance of EpochConnectivity
        The pairwise orthogonal envelope correlations.
        This matrix is symmetric.
    """ 
    from scipy.signal import hilbert

    n_nodes = None

    # Note: This is embarassingly parallel, but the overhead of sending
    # the data to different workers is roughly the same as the gain of
    # using multiple CPUs. And we require too much GIL for prefer='threading'
    # to help.

    if data.ndim != 2:
        raise ValueError('Each entry in data must be 2D, got shape %s'
                            % (data.shape,))
    n_nodes, n_times = data.shape

    # Get the complex envelope (allowing complex inputs allows people
    # to do raw.apply_hilbert if they want)
    if np.issubdtype(data.dtype, np.floating):
        n_fft = next_fast_len(n_times)
        data = hilbert(data, N=n_fft, axis=-1)[..., :n_times]
    
    pad = 250
    data = data[:,pad:-pad]

    if not np.iscomplexobj(data):
        raise ValueError('data.dtype must be float or complex, got %s'
                            % (data.dtype,))
    data_mag = np.abs(data)
    data_conj_scaled = data.conj()
    data_conj_scaled /= data_mag
    if log:
        data_mag *= data_mag
        np.log(data_mag, out=data_mag)
    
    # lowpass
    if lowpass_freq is not None:
        data_mag = filter_data(data_mag, fsample, 0, lowpass_freq, fir_window='hamming', verbose=False)
    
    # subtract means
    data_mag_nomean = data_mag - np.mean(data_mag, axis=-1, keepdims=True)

    # compute variances using linalg.norm (square, sum, sqrt) since mean=0
    data_mag_std = np.linalg.norm(data_mag_nomean, axis=-1)
    data_mag_std[data_mag_std == 0] = 1
    corr = np.empty((n_nodes, n_nodes))

    # loop over each signal in this specific epoch
    # which is now (n_signals, n_times) and compute envelope
    for li, label_data in enumerate(data):
        label_data_orth = (label_data * data_conj_scaled).imag
        np.abs(label_data_orth, out=label_data_orth)
        
        # lowpass
        if lowpass_freq is not None:
            label_data_orth = filter_data(label_data_orth, fsample, 0, lowpass_freq, fir_window='hamming', verbose=False)

        # protect against invalid value -- this will be zero
        # after (log and) mean subtraction
        label_data_orth[li] = 1.
        if log:
            label_data_orth *= label_data_orth
            np.log(label_data_orth, out=label_data_orth)
        label_data_orth -= np.mean(label_data_orth, axis=-1,
                                    keepdims=True)
        label_data_orth_std = np.linalg.norm(label_data_orth, axis=-1)
        label_data_orth_std[label_data_orth_std == 0] = 1

        # correlation is dot product divided by variances
        corr[li] = np.sum(label_data_orth * data_mag_nomean, axis=1)
        corr[li] /= data_mag_std
        corr[li] /= label_data_orth_std

    # Make it symmetric (it isn't at this point)
    if absolute:
        corr = np.abs(corr)
    corr = (corr.T + corr) / 2.

    return corr