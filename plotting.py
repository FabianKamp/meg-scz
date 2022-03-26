import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from utils import *
from config import * 

def plot_fcs(subject, group): 
    fcs = load_fcs(subject, group)
    num_plots = len(fcs.items())
    n_cols = 3
    n_rows = np.ceil(num_plots/n_cols).astype('int')
    fig, ax = plt.subplots(n_rows, n_cols, 
                        figsize=(9,8), 
                        sharex=True,
                        sharey=True)
    for n, (key, val) in enumerate(fcs.items()): 
        cax = ax.ravel()[n].imshow(val)
        ax.ravel()[n].set_title(key)
        fig.colorbar(cax, ax=ax.ravel()[n])
    return fig

def generate_fcs_pdf(group):
    subjects = get_subjects(group)
    file = os.path.join(plot_dir, 'FUNCONN', f'fcs_{group}.pdf')
    with PdfPages(file) as pdf: 
        for sub in subjects: 
            fig = plot_fcs(sub, group)
            pdf.savefig(fig)
            break


