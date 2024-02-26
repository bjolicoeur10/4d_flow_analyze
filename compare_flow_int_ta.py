#%%
import os
import h5py as h5
import numpy as np
from statsmodels.api import OLS
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib as mpl

folder4 = r'/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR/plots/ta'
base_directory = "/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR"
volu = 0
CI_records_std = []
CI_records_dl = []

for main_folder_name in os.listdir(base_directory):
    main_folder_path = os.path.join(base_directory, main_folder_name)


    if os.path.isdir(main_folder_path) and main_folder_name.startswith("trtstudyvol"):
        # print(f"Processing main folder: {main_folder_path}")


        subfolder_names = os.listdir(main_folder_path)
        subfolder_names.sort()


        for subfolder_name in subfolder_names:
            subfolder_path = os.path.join(main_folder_path, subfolder_name)


            if os.path.isdir(subfolder_path) and ("flow_int" in subfolder_name):
                raw_data_path0 = os.path.join(subfolder_path, "interleaf0")
                raw_data_path1 = os.path.join(subfolder_path, "interleaf1")
                print(raw_data_path0)
                print(raw_data_path1)
                volu = volu + 1

                # Set plot parameters
                mpl.rcParams['lines.linewidth'] = 4
                mpl.rcParams['axes.titlesize'] = 2
                mpl.rcParams['axes.labelsize'] = 24
                mpl.rcParams['axes.linewidth'] = 4
                mpl.rcParams['xtick.labelsize'] = 18
                mpl.rcParams['ytick.labelsize'] = 18
                mpl.rcParams['legend.fontsize'] = 24

                # Create a function to generate and save Bland-Altman plots
                def bland_altman_plot(data1, data2, folder, filename, tytle, scale_factor=1000, M=1, s=0.25):
                    mean = 0.5 * (data1 / scale_factor + data2 / scale_factor)
                    diff = (data1 / scale_factor - data2 / scale_factor)
                    md = np.mean(diff)  # Mean of the difference
                    sd = np.std(diff, axis=0)  # Standard deviation of the difference
                    CI_low = md - 1.96 * sd
                    CI_high = md + 1.96 * sd
                    CI_record = CI_high - CI_low
                    fig = plt.figure(figsize=(10, 5))
                    plt.axhline(md, color='gray', linestyle='--')
                    plt.axhline(md + 1.96 * sd, color='gray', linestyle='--')
                    plt.axhline(md - 1.96 * sd, color='gray', linestyle='--')
                    plt.hexbin(mean, diff, gridsize=200, extent=[-M, M, -s * M, s * M], mincnt=4, vmax=100)

                    plt.xlim([-M, M])
                    plt.ylim([-s * M, s * M])
                    plt.xticks([-M, M])
                    plt.yticks([-s * M, s * M])
                    plt.xlabel('$V_{mean} [m/s]$', labelpad=0)
                    plt.ylabel('$\Delta V [m/s]$', labelpad=0)
                    xOutPlot = M * 1.19
                    adj_factor = M * 0.07

                    plt.text(xOutPlot, (md - 1.96 * sd) - adj_factor,
                            r'-1.96SD:' +"\n"+"%.4f" % CI_low,   #r'-1.96SD:' + "%.4f" % CI_low,
                            ha="center",
                            va="center",
                            fontsize=16  # Adjust the font size here
                            )

                    plt.text(xOutPlot, (md + 1.96 * sd) + adj_factor,
                            r'1.96SD:' +"\n"+ "%.4f" % CI_high,
                            ha="center",
                            va="center",
                            fontsize=16  # Adjust the font size here
                            )

                    plt.text(xOutPlot, md,
                            r'Mean:' +"\n"+ "%.4f" % md,
                            ha="center",
                            va="center",
                            fontsize=16  # Adjust the font size here
                            )
                    plt.title(tytle,fontsize = 22,fontweight='bold')
                    plt.tight_layout()
                    plt.subplots_adjust(right=0.85)

                    # Save the plot
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    plt.savefig(os.path.join(folder, filename))
                    plt.close()
                    return CI_record


                folder4 = r'/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR/plots/ta'

                # Your existing code for processing the data goes here...
                # For demonstration, I'm using random data to replicate the process.
                v2_dl_all = []
                v3_dl_all = []

                v2_std_all = []
                v3_std_all = []


                # folder2 = r'/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR/trtstudyvol3_00822_2023-08-29/00822_00004_pcvpir_flow_int/interleaf0'
                # folder3 = r'/data/data_mrcv/45_DATA_HUMANS/HEAD_NECK/TEST_RETEST_PCVIPR/trtstudyvol3_00822_2023-08-29/00822_00004_pcvpir_flow_int/interleaf1'

                folder2 = raw_data_path0
                folder3 = raw_data_path1
                for sub in range(1):


                    print(f'Working on {folder2}')
                    with h5.File(os.path.join(folder2, 'FlowE_r.h5'), 'r') as hf:
                        vx = np.array(hf['Data']['comp_vd_1']).flatten()
                        vy = np.array(hf['Data']['comp_vd_2']).flatten()
                        vz = np.array(hf['Data']['comp_vd_3']).flatten()
                        v2_e = np.stack([vx, vy, vz], axis=0)
                        angio2_e = np.array(hf['Data']['CD']).flatten()
                        # mag2_e = np.array(hf['Data']['MAG']).flatten()

                    with h5.File(os.path.join(folder2, 'FlowS_r.h5'), 'r') as hf:
                        vx = np.array(hf['Data']['comp_vd_1']).flatten()
                        vy = np.array(hf['Data']['comp_vd_2']).flatten()
                        vz = np.array(hf['Data']['comp_vd_3']).flatten()
                        v2_s = np.stack([vx, vy, vz], axis=0)
                        angio2_s = np.array(hf['Data']['CD']).flatten()
                        # mag2_s = np.array(hf['Data']['MAG']).flatten()

                    print(f'Working on {folder3}')
                    with h5.File(os.path.join(folder3, 'FlowE_r.h5'), 'r') as hf:
                        vx = np.array(hf['Data']['comp_vd_1']).flatten()
                        vy = np.array(hf['Data']['comp_vd_2']).flatten()
                        vz = np.array(hf['Data']['comp_vd_3']).flatten()
                        v3_e = np.stack([vx, vy, vz], axis=0)
                        angio3_e = np.array(hf['Data']['CD']).flatten()
                        # mag3_e = np.array(hf['Data']['MAG']).flatten()

                    with h5.File(os.path.join(folder3, 'FlowS_r.h5'), 'r') as hf:
                        vx = np.array(hf['Data']['comp_vd_1']).flatten()
                        vy = np.array(hf['Data']['comp_vd_2']).flatten()
                        vz = np.array(hf['Data']['comp_vd_3']).flatten()
                        v3_s = np.stack([vx, vy, vz], axis=0)
                        angio3_s = np.array(hf['Data']['CD']).flatten()
                        # mag3_s = np.array(hf['Data']['MAG']).flatten()

                    #temp
                    temparr = np.array([25, 20, 40, 12, 5, 9, 19])
                    print(temparr)
                    tempidx = np.argsort(temparr)
                    print(tempidx)
                    final = []
                    final.append(temparr[tempidx])
                    print(final)

                    vxtemp = np.array([25, 20, 40, 12, 5, 9, 19])
                    vytemp = np.array([250, 200, 400, 120, 50, 90, 190])
                    vztemp = np.array([2500, 2000, 4000, 1200, 500, 900, 1900])
                    v3_temp = np.stack([vxtemp,vytemp,vztemp], axis=0)

                    temp_all =[]
                    temp_all.append(v3_temp[0])
                    temp_all.append(v3_temp[1])
                    temp_all.append(v3_temp[2])
                    print("bob!")
                    print(temp_all)
                    temp_all = np.concatenate(temp_all)
                    print(temp_all)

                    print(v3_temp)
                    print(v3_temp[0])
                    # Sort the array by summed values  
                    idx = np.argsort(-angio2_e-angio3_s)
                    idxE = idx[:20000]
                    idxS = idxE
                    print(idxE)

                    # Account for global flow change between two scans
                    X = v2_s[2][idxS]
                    X = sm.add_constant(X)
                    Y = v3_s[2][idxS]
                    result = OLS(Y, X).fit()
                    print(result.summary())
                    scale = result.params[-1]
                    scale = 1
                    v2_std_all.append(v2_s[0][idxS]*scale)
                    v2_std_all.append(v2_s[1][idxS]*scale)
                    v2_std_all.append(v2_s[2][idxS]*scale)

                    v3_std_all.append(v3_s[0][idxS])
                    v3_std_all.append(v3_s[1][idxS])
                    v3_std_all.append(v3_s[2][idxS])

                    v2_dl_all.append(v2_e[0][idxE]*scale)
                    v2_dl_all.append(v2_e[1][idxE]*scale)
                    v2_dl_all.append(v2_e[2][idxE]*scale)

                    v3_dl_all.append(v3_e[0][idxE])
                    v3_dl_all.append(v3_e[1][idxE])
                    v3_dl_all.append(v3_e[2][idxE])



                v2_std_all = np.concatenate(v2_std_all)
                v3_std_all = np.concatenate(v3_std_all)
                v2_dl_all = np.concatenate(v2_dl_all)
                v3_dl_all = np.concatenate(v3_dl_all)

                img_name_std = f"Interleaf: Volunteer {volu}"
                img_name_dl = f"Interleaf + DL: Volunteer{volu}"
                CI_value = bland_altman_plot(v2_std_all, v3_std_all, folder4,img_name_std,img_name_std)
                CI_records_std.append(CI_value)
                CI_value = bland_altman_plot(v2_dl_all, v3_dl_all, folder4,img_name_dl,img_name_dl)
                CI_records_dl.append(CI_value)
                # Generate and save Bland-Altman plots
                bland_altman_plot(v2_std_all, v3_std_all, folder4,img_name_std,img_name_std)
                bland_altman_plot(v2_dl_all, v3_dl_all, folder4,img_name_dl,img_name_dl)

            output_file_path_dl = os.path.join(folder4, 'CI_records_dl.txt')

            # Write CI_records to the file
            with open(output_file_path_dl, 'w') as file:
                for record in CI_records_dl:
                    file.write(f"{record}\n")

            output_file_path_std = os.path.join(folder4, 'CI_records_std.txt')

            # Write CI_records to the file
            with open(output_file_path_std, 'w') as file:
                for record in CI_records_std:
                    file.write(f"{record}\n")
