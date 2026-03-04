#!/usr/bin/env python3


import glob
from os.path import isfile
from tqdm import tqdm
from evaluation import evaluate
import pandas as pd
import os
import numpy as np
import dataframe_image as dfi
from PIL import Image, ImageDraw, ImageFont
import sys
import re
from evo.tools import file_interface
import yaml

SESS_OPT_SINGLE = 0
SESS_OPT_MULTI = 1
SESS_OPT_COMBINED = 2

multisess_base = []

def evaluate_submission(submission_directory, reference_directory, sess_option, verbose=False):
    """
    evaluates a submission, the results are stored in result.csv, a png for every dataset and a final calculated score (returned and stored in score.png)
    :param submission_directory:
    :param reference_directory:
    :return: total calculated score
    """
    datasets_to_check = [
        # new format
        #"exp01_catacombs.txt",
        #"exp01_catacombs_1.txt",
        #"exp01_catacombs_2.txt",
        #"exp01_catacombs_3.txt",
        #"exp01_catacombs_4.txt",
        #"exp01_catacombs_5.txt",
        "site1_handheld_1.txt",
        "site1_handheld_2.txt",
        "site1_handheld_3.txt",
        "site1_handheld_4.txt",
        "site1_handheld_5.txt",
        "site1_handheld.txt",
        "site2_robot_1.txt",
        "site2_robot_2.txt",
        "site2_robot_3.txt",
        "site2_robot.txt",
        "site3_handheld_1.txt",
        "site3_handheld_2.txt",
        "site3_handheld_3.txt",
        "site3_handheld_4.txt",
        "site3_handheld.txt"
    ]

    datasets_exclude_score=[
        "exp04_construction_upper_level.txt",
        "exp05_construction_upper_level_2.txt",
        "exp06_construction_upper_level_3.txt"

    ]

    multisess_order = {
        "site1_handheld.txt" : ["site1_handheld_1.txt",
                                "site1_handheld_2.txt",
                                "site1_handheld_3.txt",
                                "site1_handheld_4.txt",
                                "site1_handheld_5.txt"],

        "site2_robot.txt" : ["site2_robot_1.txt",
                             "site2_robot_2.txt",
                             "site2_robot_3.txt"],

        "site3_handheld.txt" : ["site3_handheld_1.txt",
                                "site3_handheld_2.txt",
                                "site3_handheld_3.txt",
                                "site3_handheld_4.txt"]

        #"exp01_catacombs.txt" : ["exp01_catacombs_1.txt",
        #                         "exp01_catacombs_2.txt",
        #                         "exp01_catacombs_3.txt",
        #                         "exp01_catacombs_4.txt",
        #                         "exp01_catacombs_5.txt"]
    }

    if sess_option == SESS_OPT_SINGLE:
        tmp_datasets = []
        for ds in datasets_to_check:
            if not ds in multisess_order.keys():
                tmp_datasets.append(ds)
        datasets_to_check = tmp_datasets

        

    elif sess_option == SESS_OPT_MULTI:
        tmp_datasets = []
        for ms in multisess_order.keys():
            tmp_datasets.append(ms)
        datasets_to_check = tmp_datasets

    global multisess_base
    multisess_base = [s.replace(".txt", "") for s in multisess_order.keys()]
    multisess_submitted = {}

    for m in multisess_base:
        multisess_submitted[m] = False

    submission_folder_name = os.path.basename(os.path.normpath(submission_directory))
    results_file_single = os.path.join(submission_directory, "results_single.csv")
    results_file_multi = os.path.join(submission_directory, "results_multi.csv")
    submission_files = glob.glob(submission_directory + '/**/*.txt', recursive=True)
    extrinsics_files = glob.glob(submission_directory + '/**/extrinsics_robot.yaml', recursive=True)

    custom_extrinsics_robot_path = os.path.join(submission_directory, "extrinsics_robot.yaml")
    if len(extrinsics_files) > 0:
        custom_extrinsics_robot_path = extrinsics_files[0]

    extrinsics_robot_path = os.path.join(groundtruth_path, "extrinsics_robot.yaml")

    with open(extrinsics_robot_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    
    T_lidar_imu_robot = np.array(data_loaded['lidar0']['T_here_imu0'])

    if os.path.isfile(custom_extrinsics_robot_path):
        with open(custom_extrinsics_robot_path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        
        if "lidar0" in data_loaded.keys():
            if "T_here_imu0" in data_loaded['lidar0'].keys():
                T_lidar_imu_robot = np.array(data_loaded['lidar0']['T_here_imu0'])

    # rename submission files if they are in old format
    for file in submission_files:
        directory = os.path.dirname(file)
        basename = os.path.basename(file)
        if basename == 'exp_04_construction_upper_level_easy_2_2022-03-03-11-48-59.txt':
            new_file = os.path.join(directory, "exp04_construction_upper_level.txt")
            os.rename(file, new_file)
        elif basename == 'exp_05_construction_upper_level_easy_2022-03-03-11-46-10.txt':
            new_file = os.path.join(directory, "exp05_construction_upper_level_2.txt")
            os.rename(file, new_file)
        elif basename == 'exp_06_construction_upper_level_hard_2022-03-03-12-08-37.txt':
            new_file = os.path.join(directory, "exp06_construction_upper_level_3.txt")
            os.rename(file, new_file)

        #for mulses in multisess_base:
        #    if basename.startswith(mulses) and re.findall(r'_\d+.txt', basename):
        #        multi_session_evaluation = True
        #        multisess_submitted[mulses].append(file)
        #        multisess_part.append(file)

    if sess_option == SESS_OPT_MULTI or sess_option == SESS_OPT_COMBINED:
        for ms in multisess_submitted:
            for sf in submission_files:
                if ms in sf and not multisess_submitted[ms]:
                    concat_files(submission_directory, multisess_order[ms+".txt"], os.path.join(submission_directory, ms+".txt"))
                    multisess_submitted[ms] = True
    
    #for mulses in multisess_submitted:
    #    multisess_submitted[mulses].sort()
    #    if len(multisess_submitted[mulses]) > 0:
    #        concat_files(multisess_submitted[mulses], os.path.join(submission_directory, mulses+".txt"))


    submission_files = glob.glob(submission_directory + '/**/*.txt', recursive=True)
    if sess_option == SESS_OPT_SINGLE:
        for sf in submission_files:
            path, filename = os.path.split(sf)
            if filename in multisess_order:
                submission_files.remove(sf)

    if sess_option == SESS_OPT_MULTI:
        tmp_submission_files = []
        for sf in submission_files:
            path, filename = os.path.split(sf)
            if filename in multisess_order.keys():
                tmp_submission_files.append(sf)
        submission_files = tmp_submission_files

    submission_files.sort()
    
    if len(submission_files) == 0:
        raise Exception('No .txt files to evaluate in submission')

    # tmp = tmp +1
    # if tmp > 3:
    #     break

    dataset = []
    rmse = []
    mean = []
    median = []
    std = []
    minimum = []
    maximum = []
    sse = []
    points_estimate = []
    points_reference = []
    completeness = []
    is_multisess = []
    ss_scores = np.zeros((len(datasets_to_check), 8), float)
    ms_scores = np.zeros((len(datasets_to_check), 8), float)

    all_errors = np.empty((1), float)

    for idx, reference in enumerate(tqdm(datasets_to_check, 'datasets', leave=False, disable=not verbose)):
        ms_flag = False
        submission_name = reference
        submission_file = ''
        for file in submission_files:
            path, filename = os.path.split(file)
            #filename = filename[0:-4]  # cut off extension
            #if reference.lower().find(filename.lower()) >= 0:
            if reference.lower() == filename.lower():
                submission_file = file

        if len(submission_file) < 1:
            dataset.append(submission_name)
            rmse.append(None)
            mean.append(None)
            median.append(None)
            std.append(None)
            minimum.append(None)
            maximum.append(None)
            sse.append(None)
            points_estimate.append(None)
            points_reference.append(None)
            completeness.append(0)
            
            if submission_name in multisess_order.keys():
                is_multisess.append(True)
            else:
                is_multisess.append(False)

            if verbose:
                print("\nno fitting file for {} could be found!".format(
                    submission_directory + "/" + submission_name + "*.txt"))
        else:
            est_file = submission_file
            ref_file = os.path.join(reference_directory, reference)
            if submission_name in multisess_order.keys():
                ms_flag = True
            

            try:
                create_plots = True
                # HACK: disable plots for site3
                if 'site3' in est_file:
                    create_plots = False

                ape_stats, dense_trajectory, traj_est_aligned, traj_ref = evaluate(est_file, ref_file, submission_directory, T_lidar_imu_robot, create_plots)
            except Exception as e:
                dataset.append(submission_name)
                rmse.append(None)
                mean.append(None)
                median.append(None)
                std.append(None)
                minimum.append(None)
                maximum.append(None)
                sse.append(None)
                points_estimate.append(None)
                points_reference.append(None)
                completeness.append(0)
                is_multisess.append(False)
                print("\nparsing issue in {}".format(submission_file))
                write_exception(submission_directory, reference, str(e))
                continue
            dataset.append(submission_name)
            rmse.append(ape_stats["rmse"])
            mean.append(ape_stats["mean"])
            median.append(ape_stats["median"])
            std.append(ape_stats["std"])
            minimum.append(ape_stats["min"])
            maximum.append(ape_stats["max"])
            sse.append(ape_stats["sse"])
            points_estimate.append(traj_est_aligned.get_infos()['nr. of poses'])
            if dense_trajectory:
                points_reference.append(int(traj_ref.get_infos()['duration (s)'] * 10))
            else:
                points_reference.append(traj_ref.get_infos()['nr. of poses'])
                # only works with sparse traj.
                all_pts = np.c_[traj_ref.positions_xyz[:traj_est_aligned.positions_xyz.shape[0],
                                :], traj_est_aligned.positions_xyz]
                diff = np.linalg.norm(traj_ref.positions_xyz[:traj_est_aligned.positions_xyz.shape[0],
                                      :] - traj_est_aligned.positions_xyz, axis=1)
                all_errors = np.r_[all_errors, diff]

                # compute score

                # single session scores
                ss_pts_per_bin = [20, 10, 6, 5, 3, 1, 0]
                ss_accuracy_boundaries = [0.5 * 1e-2, 1.0 * 1e-2, 3 * 1e-2, 6 * 1e-2, 10 * 1e-2, 40 * 1e-2, 999999.0 * 1e-2]

                ss_bin_1 = [i for i in diff if i < ss_accuracy_boundaries[0]]
                ss_bin_2 = [i for i in diff if i >= ss_accuracy_boundaries[0] and i < ss_accuracy_boundaries[1]]
                ss_bin_3 = [i for i in diff if i >= ss_accuracy_boundaries[1] and i < ss_accuracy_boundaries[2]]
                ss_bin_4 = [i for i in diff if i >= ss_accuracy_boundaries[2] and i < ss_accuracy_boundaries[3]]
                ss_bin_5 = [i for i in diff if i >= ss_accuracy_boundaries[3] and i < ss_accuracy_boundaries[4]]
                ss_bin_6 = [i for i in diff if i >= ss_accuracy_boundaries[4] and i < ss_accuracy_boundaries[5]]
                ss_bin_7 = [i for i in diff if i >= ss_accuracy_boundaries[5]]

                ss_current_score = len(ss_bin_1) * ss_pts_per_bin[0] + len(ss_bin_2) * ss_pts_per_bin[1] + len(ss_bin_3) * \
                                ss_pts_per_bin[2] + len(ss_bin_4) * ss_pts_per_bin[3] + len(ss_bin_5) * ss_pts_per_bin[4]  \
                                + len(ss_bin_6)*ss_pts_per_bin[5] + len(ss_bin_7)*ss_pts_per_bin[6]
                
                # multisession scores
                ms_pts_per_bin = [20, 10, 6, 5, 3, 1, 0]
                ms_accuracy_boundaries = [0.5 * 1e-2, 1.0 * 1e-2, 3 * 1e-2, 6 * 1e-2, 10 * 1e-2, 40 * 1e-2, 999999.0 * 1e-2]
                ms_bin_1 = [i for i in diff if i < ms_accuracy_boundaries[0]]
                ms_bin_2 = [i for i in diff if i >= ms_accuracy_boundaries[0] and i < ms_accuracy_boundaries[1]]
                ms_bin_3 = [i for i in diff if i >= ms_accuracy_boundaries[1] and i < ms_accuracy_boundaries[2]]
                ms_bin_4 = [i for i in diff if i >= ms_accuracy_boundaries[2] and i < ms_accuracy_boundaries[3]]
                ms_bin_5 = [i for i in diff if i >= ms_accuracy_boundaries[3] and i < ms_accuracy_boundaries[4]]
                ms_bin_6 = [i for i in diff if i >= ms_accuracy_boundaries[4] and i < ms_accuracy_boundaries[5]]
                ms_bin_7 = [i for i in diff if i >= ms_accuracy_boundaries[5]]

                ms_current_score = len(ms_bin_1) * ms_pts_per_bin[0] + len(ms_bin_2) * ms_pts_per_bin[1] + len(ms_bin_3) * \
                                ms_pts_per_bin[2] + len(ms_bin_4) * ms_pts_per_bin[3] + len(ms_bin_5) * ms_pts_per_bin[4] \
                                + len(ms_bin_6)*ms_pts_per_bin[5] + len(ms_bin_7)*ms_pts_per_bin[6]
                # exponential scoring method
                a, c = 12.91549665, 25.58427881
                exponential_score = 0

                for point in diff:
                    exponential_score+=exp_score(point,a,c)
                num_poses=file_interface.read_tum_trajectory_file(ref_file).num_poses

                # normalize score
                # DOUBLE for site 3
                if 'site3' in est_file:
                    ss_current_score=ss_current_score/(num_poses/10)
                    ms_current_score=ms_current_score/(num_poses/10)
                else:
                    ss_current_score=ss_current_score/(num_poses/5)
                    ms_current_score=ms_current_score/(num_poses/5)

                # remove score if it is one of the datasets that have been published before
                # TODO single vs multi
                if reference in datasets_exclude_score:
                    ss_current_score=None
                    ms_current_score=None

                if ms_flag == False:
                    ss_scores[idx, :] = [len(ss_bin_1), len(ss_bin_2), len(ss_bin_3), len(ss_bin_4), len(ss_bin_5), len(ss_bin_6), len(ss_bin_7), ss_current_score]
                else:
                    ms_scores[idx, :] = [len(ms_bin_1), len(ms_bin_2), len(ms_bin_3), len(ms_bin_4), len(ms_bin_5), len(ms_bin_6), len(ms_bin_7), ms_current_score]

            completeness.append(min(points_estimate[-1] / points_reference[-1], 1))

            if submission_name in multisess_order.keys():
                is_multisess.append(True)
            else:
                is_multisess.append(False)

    all_scores_multi = ms_scores[:, 7].tolist()
    all_scores_single = ss_scores[:, 7].tolist()

    if sess_option == SESS_OPT_COMBINED:
        all_scores = [x + y for x, y in zip(all_scores_single, all_scores_multi)]
    elif sess_option == SESS_OPT_SINGLE:
        all_scores = all_scores_single
    else:
        all_scores = all_scores_multi


    data = {'dataset': dataset, "rmse": rmse, "mean": mean, "median": median, "std": std, "min": minimum,
            "max": maximum, "sse": sse, "points_estimate": points_estimate, "points_reference": points_reference,
            "completeness": completeness, "is_multisess": is_multisess, "score": all_scores}
    
    df = pd.DataFrame(data=data)
    columns_to_export = ['dataset','rmse','mean','median','std','min','max',	
                        'sse','points_estimate','points_reference','completeness', 'score']
    

    if sess_option == SESS_OPT_SINGLE or sess_option == SESS_OPT_COMBINED:
        df_single = df[df['is_multisess'] == False]

        df2 = df_single.copy()
        df2.loc['Result'] = df_single.mean(numeric_only=True, axis=0)

        df2.at['Result', 'points_estimate'] = df_single['points_estimate'].sum()
        df2.at['Result', 'points_reference'] = df_single['points_reference'].sum()
        df2.at['Result', 'score'] = df_single['score'].sum()
        df2.to_csv(results_file_single, index=True, columns=columns_to_export)
    
    if sess_option == SESS_OPT_MULTI or sess_option == SESS_OPT_COMBINED:
        df_multi = df[df['is_multisess'] == True]

        df2 = df_multi.copy()
        df2.loc['Result'] = df_multi.mean(numeric_only=True, axis=0)

        df2.at['Result', 'points_estimate'] = df_multi['points_estimate'].sum()
        df2.at['Result', 'points_reference'] = df_multi['points_reference'].sum()
        df2.at['Result', 'score'] = df_multi['score'].sum()
        df2.to_csv(results_file_multi, index=True, columns=columns_to_export)

    # save all errors (only for debug)
    # np.savetxt(os.path.join(submission_folder,submission_folder_name + "_all_errors.csv"), all_errors, delimiter=",")
    single_indices =  [i for i, x in enumerate(is_multisess) if x == False]
    multi_indices =  [i for i, x in enumerate(is_multisess) if x == True]

    scores_single = ss_scores[single_indices, :]
    scores_multi = ms_scores[multi_indices, :]
    
    # generate score images
    if sess_option == SESS_OPT_SINGLE or sess_option == SESS_OPT_COMBINED:
        df_score_single = pd.DataFrame(
            {'< 0.5cm': scores_single[:, 0], '< 1cm': scores_single[:, 1], '< 3cm': scores_single[:, 2], '< 6cm': scores_single[:, 3],
            '< 10cm': scores_single[:, 4], '< 40cm': scores_single[:, 5], '> 40cm': scores_single[:, 6],
            'Score': scores_single[:, 7]})
        # Change the row indexes
        df_score_single.index = [dataset[i] for i in single_indices]
        total = df_score_single.sum()
        total.name = 'Total'
        # Assign sum of all rows of DataFrame as a new Row
        df_score_single = df_score_single.append(total.transpose())
        #df_score_single = df_score_single.sort_index()
        df_score_formated=df_score_single.style.format(precision=2,formatter={('Score'): "{:.2f}"},na_rep="-")
        dfi.export(df_score_formated, os.path.join(submission_directory, "./score_single.png"), table_conversion="matplotlib",fontsize=10)

    if sess_option == SESS_OPT_MULTI or sess_option == SESS_OPT_COMBINED:
        df_score_multi = pd.DataFrame(
            {'< 0.5cm': scores_multi[:, 0], '< 1cm': scores_multi[:, 1], '< 3cm': scores_multi[:, 2], '< 6cm': scores_multi[:, 3],
            '< 10cm': scores_multi[:, 4], '< 40cm': scores_multi[:, 5], '> 40cm': scores_multi[:, 6],
            'Score': scores_multi[:, 7]})
        # Change the row indexes
        df_score_multi.index = [dataset[i] for i in multi_indices]

        total = df_score_multi.sum()
        total.name = 'Total'
        # Assign sum of all rows of DataFrame as a new Row
        #df_score_multi = df_score_multi.append(total.transpose())
        #df_score_multi = df_score_multi.sort_index()
        df_score_formated=df_score_multi.style.format(precision=2,formatter={('Score'): "{:.2f}"},na_rep="-")
        dfi.export(df_score_formated, os.path.join(submission_directory, "./score_multi.png"), table_conversion="matplotlib",fontsize=10)

    return total

def concat_files(submission_directory, files_list, final_file):
    with open(final_file, 'w') as outfile:
        for fname in files_list:
            fpath = os.path.join(submission_directory, fname)
            if os.path.isfile(fpath):
                with open(fpath) as infile:
                    traj = infile.read()
                    if not traj.endswith("\n"):
                        traj += "\n"
                    outfile.write(traj)

def write_exception(submission_directory, traj_file, exception_str):
    err_fpath = os.path.join(submission_directory, "errors.txt")
    with open(err_fpath, 'a') as err_output:
        err_output.write(traj_file + ": " + exception_str + "\n")

def exp_score(x,a, c):
    result= a*np.exp(-c*x)
    if result>10:
        return 10
    else:
        return result

def get_concat_v_blank(im1, im2, color=(255, 255, 255)):
    """
    stacks 2 images vertically while filling empty space with a color (white by default)
    :param im1: first image
    :param im2: second image
    :param color: color for empty space
    :return: stacked image
    """
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    x_origin = int((im2.width - im1.width) / 2)
    dst.paste(im1, (x_origin, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def combine_pictures(path, name, save_image=True):
    """
    takes all .png in a given path and combines them to a resulting image.
    :param path: path of the directory
    :param name: title displayed on the combined image.
    :param save_image: if set to True, will save the resulting image to path + "/combined.png"
    :return: combined image
    """

    single_file = path + "/score_single.png"
    multi_file = path + "/score_multi.png"
    initial_image_single = None
    initial_image_multi = None

    if os.path.isfile(single_file):
        initial_image_single = Image.open(single_file)
    
    if os.path.exists(multi_file):
        initial_image_multi = Image.open(multi_file)
            
    image_paths = set(glob.glob(path + "/*.png")) - set(glob.glob(path + "/*score*")) - set(
        glob.glob(path + "/combine*"))
    image_paths = list(image_paths)
    image_paths.sort()

    output_imgs = [initial_image_single, initial_image_multi]
    output_files = ["score_single.png", "score_multi.png"]

    for i in range(0,len(output_imgs)):
        if output_imgs[i] != None:
            for j in image_paths:
                path,fname = os.path.split(j)
                ds_key = fname.replace(".png", "")
                if i == 0 and not ds_key in multisess_base or i == 1 and ds_key in multisess_base:
                    image = Image.open(j)
                    output_imgs[i] = get_concat_v_blank(output_imgs[i], image)
            W, H = 1400, 200
            Title_image = Image.new('RGB', (W, H), color=(255, 255, 255))
            font = ImageFont.truetype("fonts/calibri.ttf", 100)
            draw = ImageDraw.Draw(Title_image)
            w, h = font.getsize(name)
            draw.text(((W - w) / 2, (H - h) / 2), name, (0, 0, 0), font=font)
            output_imgs[i] = get_concat_v_blank(Title_image, output_imgs[i])

            if save_image:
                if output_imgs[i] != None:
                    output_imgs[i].save(path + "/" + output_files[i])

    #return initial_image


if __name__ == "__main__":
    if len(sys.argv) not in [4,5]:
        print(f'Usage: ./batch_evaluation.py submission_path output_path groundtruth_path option', file=sys.stderr)

        # exit(1)
        # debugging

        submission_path = "path_to_submission_folder"
        output_path = "path_to_output_folder"
        groundtruth_path = "path_to_groundtruth_folder"
        sess_option = SESS_OPT_COMBINED

    else:
        submission_path = sys.argv[1]
        output_path = sys.argv[2]
        groundtruth_path = sys.argv[3]
        sess_option = SESS_OPT_COMBINED
        if len(sys.argv) == 5:
            sess_option = int(sys.argv[4])
        if not sess_option in [SESS_OPT_SINGLE,SESS_OPT_MULTI,SESS_OPT_COMBINED]:
            sess_option = SESS_OPT_COMBINED

    for d in [submission_path, output_path, groundtruth_path]:
        if not os.path.isdir(d):
            print(f'No such directory: {d}', file=sys.stderr)
            exit(1)

    evaluate_submission(submission_path, groundtruth_path, sess_option)
    combine_pictures(submission_path, os.path.basename(submission_path))

    # move output file to output directory
    pngs = glob.glob(submission_path + "/*.png")
    csvs = glob.glob(submission_path + "/*.csv")
    errors = [os.path.join(submission_path, "errors.txt")]

    for f in pngs + csvs + errors:
        if os.path.isfile(f):
            os.rename(f, f'{output_path}/{os.path.basename(f)}')
