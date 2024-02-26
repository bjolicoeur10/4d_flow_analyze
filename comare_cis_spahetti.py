import numpy as np
import matplotlib.pyplot as plt
import os

# Define the base directory and file names
base_directory = '/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR/plots/final/pixelwize/interleaf/ta/individial'
file_name_dl = 'CI_records_dl.txt'
file_name_std = 'CI_records_std.txt'
out_img_name = "Spaghetti_CI_comparison.png"  # Updated output image name for the new plot

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

# Ensure the figure is sized appropriately
plt.figure(figsize=(10, 6))

# Plot each pair of standard and DL values against each other, all in black
for i in range(len(values_std)):
    plt.plot(['Standard', 'DL'], [values_std[i], values_dl[i]], '-o', color='black', alpha=0.7)

# Set plot title and labels with title adjustments
plt.title('Spaghetti Plot: Standard vs DL Measurements', fontsize=14, fontweight='bold')
plt.ylabel('95% LoA[m/s]', fontsize=14)

# Adjust the size of the x-axis labels
plt.tick_params(axis='x', labelsize=14)

# Set the y-axis range from 0 to 0.3
# plt.ylim(0, 0.3)

# Adjust subplot parameters to reduce space, if needed
plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)

plt.tight_layout()  # Adjust layout to make better use of space

# Check if the directory exists, if not, create it
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

# Save the plot
plt.savefig(os.path.join(base_directory, out_img_name))
plt.show()
plt.close()
