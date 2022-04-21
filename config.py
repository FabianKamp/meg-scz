####################################
# Define group and frequency bands #
####################################

groups = ['CHR', 'HC', 'FEP', 'CLR']
group = 'CHR'
freq_bands = [[1,3.9], 
              [4,7.9], 
              [8,12.9], 
              [13, 29.9], 
              [30,46], 
              [64, 68], 
              [74, 78], 
              [84, 88],
              [64,90]]

######################################
# Define data and result directories #
######################################

data_dir = "/mnt/raid/data/SFB1315/Uhlhaas_MEG/VIRTCHAN/DATA"
# data_dir = "C:\\Users\\Kamp\\Documents\\scz\\data"
result_dir = "/mnt/raid/data/SFB1315/Uhlhaas_MEG/RESULTS"
# result_dir = "C:\\Users\\Kamp\\Documents\\scz\\results"
plot_dir = "/mnt/raid/data/SFB1315/Uhlhaas_MEG/RESULTS/PLOTS"