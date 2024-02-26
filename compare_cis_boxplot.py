#%%
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the base directory and file names
base_directory = '/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR/plots/tr/individual'
file_name_dl = 'CI_records_dl.txt'
file_name_std = 'CI_records_std.txt'
out_img_name = "Blandaltman_CI_comparison"
# Function to read values from a file into a NumPy array
def read_values_from_file(file_path):
    with open(file_path, 'r') as file:
        values = [float(line.strip()) for line in file if line.strip()]
    return np.array(values)

# Read the values from the files
path_dl = os.path.join(base_directory, file_name_dl)
path_std = os.path.join(base_directory, file_name_std)
values_dl = read_values_from_file(path_dl)
values_std = read_values_from_file(path_std)

plt.figure(figsize=(6, 4))  # Adjust figure size as needed

# Create box plots with "Standard" on the left and "DL" on the right and capture the returned dictionary
box = plt.boxplot([values_std, values_dl], labels=['Standard', 'DL'], widths=0.6)

# Set plot title and labels with title adjustments
plt.title('Time Resolved: Single-Subject LoA Comparison', fontsize=14, fontweight='bold')
plt.ylabel('95% LoA[m/s]', fontsize=14)

# Increase the size of the x-axis labels
plt.tick_params(axis='x', labelsize=14)

# Change the median line color to dark purple without changing the box color
for median in box['medians']:
    median.set_color('purple')  # Use 'purple' or a specific hex code for dark purple

# Thicken the plot border
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

# Adjust subplot parameters to reduce space, if needed
plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)

plt.tight_layout()  # Adjust layout to make better use of space


if not os.path.exists(base_directory):
    os.makedirs(base_directory)
plt.savefig(os.path.join(base_directory, out_img_name))
plt.show()
plt.close()
                    

# %%
