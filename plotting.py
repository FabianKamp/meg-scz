import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from utils import *
from config import * 

def plot_fcs(subject, group, norm=False): 
    fcs = load_fcs(subject, group, norm)
    num_plots = len(fcs.items())
    n_cols = 3
    n_rows = np.ceil(num_plots/n_cols).astype('int')
    fig, ax = plt.subplots(n_rows, n_cols, 
                        figsize=(9,8), 
                        sharex=True,
                        sharey=True)
    fig.suptitle(f'Subject {subject}')
    for n, (key, val) in enumerate(fcs.items()): 
        cax = ax.ravel()[n].imshow(val)
        ax.ravel()[n].set_title(key)
        fig.colorbar(cax, ax=ax.ravel()[n])
    plt.close()
    return fig

def generate_fcs_pdf(group, norm):
    subjects = get_subjects(group)
    if norm: 
        file = os.path.join(plot_dir, 'FUNCONN', f'norm_fcs_{group}.pdf')
    else:
        file = os.path.join(plot_dir, 'FUNCONN', f'fcs_{group}.pdf')
    with PdfPages(file) as pdf: 
        for sub in subjects: 
            try: 
                fig = plot_fcs(sub, group, norm)
                pdf.savefig(fig)
            except: 
                print(f'Subject {sub}, group {group} not found')
            
for group in config.groups:
    generate_fcs_pdf(group, norm=True)


