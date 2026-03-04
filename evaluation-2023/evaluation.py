#!/usr/bin/env python3

# Created by Beda Berner
# beda.berner@hilti.com

import collections
import typing

from evo.core import metrics
from evo.core import lie_algebra as lie
from evo.tools.plot import *
import numpy as np

from evo.tools import plot
import matplotlib.pyplot as plt
import sys
from evo.tools.settings import SETTINGS

SETTINGS.plot_usetex = False
from evo.core import sync
from evo.tools import file_interface
import copy
from scipy.spatial.transform import Rotation as R
from evo.core.trajectory import PoseTrajectory3D

import yaml

import os


def error_array_custom(ax: plt.Axes, err_array: ListOrArray,
                       x_array: typing.Optional[ListOrArray] = None,
                       statistics: typing.Optional[typing.Dict[str, float]] = None,
                       threshold: float = None, cumulative: bool = False,
                       color: str = 'grey', name: str = "error", title: str = "",
                       xlabel: str = "index", ylabel: typing.Optional[str] = None,
                       subplot_arg: int = 111, linestyle: str = "-",
                       marker: typing.Optional[str] = None):
    """
    high-level function for plotting raw error values of a metric
    :param fig: matplotlib axes
    :param err_array: an nx1 array of values
    :param x_array: an nx1 array of x-axis values
    :param statistics: optional dictionary of {metrics.StatisticsType.value: value}
    :param threshold: optional value for horizontal threshold line
    :param cumulative: set to True for cumulative plot
    :param name: optional name of the value array
    :param title: optional plot title
    :param xlabel: optional x-axis label
    :param ylabel: optional y-axis label
    :param subplot_arg: optional matplotlib subplot ID if used as subplot
    :param linestyle: matplotlib linestyle
    :param marker: optional matplotlib marker style for points
    """
    if cumulative:
        if x_array is not None:
            ax.plot(x_array, np.cumsum(err_array), linestyle=linestyle,
                    marker=marker, color=color, label=name)
        else:
            ax.plot(np.cumsum(err_array), linestyle=linestyle, marker=marker,
                    color=color, label=name)
    else:
        if x_array is not None:
            ax.plot(x_array, err_array, linestyle=linestyle, marker=marker,
                    color=color, label=name)
        else:
            ax.plot(err_array, linestyle=linestyle, marker=marker, color=color,
                    label=name)
                
    if statistics is not None:
        for stat_name, value in statistics.items():
            color = next(ax._get_lines.prop_cycler)['color']
            if stat_name == "std" and "mean" in statistics:
                mean, std = statistics["mean"], statistics["std"]
                ax.axhspan(mean - std / 2, mean + std / 2, color=color,
                           alpha=0.5, label=stat_name)
            else:
                ax.axhline(y=value, color=color, linewidth=2.0,
                           label=stat_name)
    if threshold is not None:
        ax.axhline(y=threshold, color='red', linestyle='dashed', linewidth=2.0,
                   label="threshold")
    
    ax.ticklabel_format(style='plain')
    ax.set_ylabel(ylabel if ylabel else name)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend(frameon=True)


def prepare_axis_custom(fig: plt.Figure, plot_mode: PlotMode = PlotMode.xy,
                        subplot_arg: int = 111) -> plt.Axes:
    """
    prepares an axis according to the plot mode (for trajectory plotting)
    :param fig: matplotlib figure object
    :param plot_mode: PlotMode
    :param subplot_arg: optional if using subplots - the subplot id (e.g. '122')
    :return: the matplotlib axis
    """
    if plot_mode == PlotMode.xyz:
        ax = fig.add_subplot(subplot_arg, projection="3d")
    else:
        ax = fig.add_subplot(subplot_arg)
        ax.axis("equal")
    if plot_mode in {PlotMode.xy, PlotMode.xz, PlotMode.xyz}:
        xlabel = "$x$ (m)"
    elif plot_mode in {PlotMode.yz, PlotMode.yx}:
        xlabel = "$y$ (m)"
    else:
        xlabel = "$z$ (m)"
    if plot_mode in {PlotMode.xy, PlotMode.zy, PlotMode.xyz}:
        ylabel = "$y$ (m)"
    elif plot_mode in {PlotMode.zx, PlotMode.yx}:
        ylabel = "$x$ (m)"
    else:
        ylabel = "$z$ (m)"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if plot_mode == PlotMode.xyz:
        ax.set_zlabel('$z$ (m)')
    if SETTINGS.plot_invert_xaxis:
        plt.gca().invert_xaxis()
    if SETTINGS.plot_invert_yaxis:
        plt.gca().invert_yaxis()
    return ax


def traj_custom(ax: plt.Axes, plot_mode: PlotMode, traj: trajectory.PosePath3D,
                style: str = '-', color: str = 'black', label: str = "",
                alpha: float = 1.0, markers: str = 'None') -> None:
    """
    plot a path/trajectory based on xyz coordinates into an axis
    :param ax: the matplotlib axis
    :param plot_mode: PlotMode
    :param traj: trajectory.PosePath3D or trajectory.PoseTrajectory3D object
    :param style: matplotlib line style
    :param color: matplotlib color
    :param label: label (for legend)
    :param alpha: alpha value for transparency
    """
    x_idx, y_idx, z_idx = plot_mode_to_idx(plot_mode)
    x = traj.positions_xyz[:, x_idx]
    y = traj.positions_xyz[:, y_idx]
    if plot_mode == PlotMode.xyz:
        z = traj.positions_xyz[:, z_idx]
        ax.plot(x, y, z, linestyle=style, color=color, label=label, alpha=alpha, marker=markers)
    elif "custom eval" in label:
        ax.scatter(x,y, s=0.5, label = label)
    else:
        ax.plot(x, y, linestyle=style, color=color, label=label, alpha=alpha, marker=markers)
    if label:
        ax.legend(frameon=True)


def trajectories_custom(fig: plt.Figure, trajectories: typing.Union[
    trajectory.PosePath3D, typing.Sequence[trajectory.PosePath3D],
    typing.Dict[str, trajectory.PosePath3D]], plot_mode=PlotMode.xy,
                        title: str = "", subplot_arg: int = 111) -> None:
    """
    high-level function for plotting multiple trajectories
    :param fig: matplotlib figure
    :param trajectories: instance or container of PosePath3D or derived
    - if it's a dictionary, the keys (names) will be used as labels
    :param plot_mode: e.g. plot.PlotMode.xy
    :param title: optional plot title
    :param subplot_arg: optional matplotlib subplot ID if used as subplot
    """
    ax = prepare_axis_custom(fig, plot_mode, subplot_arg)
    cmap_colors = None
    if SETTINGS.plot_multi_cmap.lower() != "none" and isinstance(
            trajectories, collections.Iterable):
        cmap = getattr(cm, SETTINGS.plot_multi_cmap)
        cmap_colors = iter(cmap(np.linspace(0, 1, len(trajectories))))

    # helper function
    def draw(t, name=""):
        if cmap_colors is None:
            color = next(ax._get_lines.prop_cycler)['color']
        else:
            color = next(cmap_colors)
        if SETTINGS.plot_usetex:
            name = name.replace("_", "\\_")
        if name != "evaluated estimate points" and not "custom eval" in name:
            traj_custom(ax, plot_mode, t, '-', color, name)
        elif "custom eval" in name:
            traj_custom(ax, plot_mode, t, 'dotted', color, name)
        else:
            traj_custom(ax, plot_mode, t, 'dotted', color, name, markers='o')

    if isinstance(trajectories, trajectory.PosePath3D):
        draw(trajectories)
    elif isinstance(trajectories, dict):
        for name, t in trajectories.items():
            draw(t, name)
    else:
        for t in trajectories:
            draw(t)


def evaluate(est_file, ref_file, output_path, T_lidar_imu, create_plots=True):
    """
    evaluates a dataset based on a estimate and a reference and stores a .png of the evaluation under the name of the dataset
    :param est_file: estimate in tum format
    :param ref_file: reference in tum format
    :return: ape_stats: stats of the evaluation, dense_trajectory: is the reference a dense trajectory?, traj_est_aligned: aligned estimate trajectory, traj_ref_sync: aligned reference trajectory.
    """
    np.set_printoptions(suppress=True)
    traj_ref = file_interface.read_tum_trajectory_file(ref_file)
    if 'robot' in ref_file:
        lidar_file = ref_file
        lidar_file = lidar_file.replace(".txt", "_lidar.txt")
        lidar_ref = file_interface.read_tum_trajectory_file(lidar_file)


    apply_pole_tip_calibration = True
    # apply poletip calibration
    if apply_pole_tip_calibration == True and not 'robot' in est_file:
        calibration_type = ref_file.split('_')[-1].lower()
        if calibration_type == 'imu.txt':
            T_imu_ref = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1.0]])
        else:
            T_imu_ref = np.array([[1, 0, 0, 0.059],
                                  [0, 1, 0, -0.00855],
                                  [0, 0, 1, 0.1964],
                                  [0, 0, 0, 1.0]])

        data = np.genfromtxt(est_file, delimiter=' ', skip_header=False)

        for i in range(data.shape[0]):
            rot_mat = R.from_quat([data[i, 4:8]]).as_matrix().reshape([3, 3])  # from_quat(), xyzw
            transl = data[i, 1:4].reshape([3, 1])
            homogeneous_transform = np.vstack([np.hstack([rot_mat, transl]), np.array([0, 0, 0, 1])])
            result = homogeneous_transform @ T_imu_ref
            data[i, 1:4] = result[0:3, 3].reshape([1, 3])
            data[i, 4:] = R.from_matrix(result[0:3, 0:3]).as_quat()

        stamps = data[:, 0]  # n x 1
        xyz = data[:, 1:4]  # n x 3
        quat_wxyz = data[:, [7, 4, 5, 6]]  # n x 4
        traj_est = PoseTrajectory3D(xyz, quat_wxyz, stamps)  # PoseTrajectory3D(), wxyz

    else:
        traj_est = file_interface.read_tum_trajectory_file(est_file)

    lidar_transforms = {}
    if 'robot' in est_file:
        T_imu_lidar = np.linalg.inv(T_lidar_imu)
        data = np.genfromtxt(est_file, delimiter=' ', skip_header=False)
        for i in range(data.shape[0]):
            rot_mat = R.from_quat([data[i, 4:8]]).as_matrix().reshape([3, 3])  # from_quat(), xyzw
            transl = data[i, 1:4].reshape([3, 1])
            homogeneous_transform = np.vstack([np.hstack([rot_mat, transl]), np.array([0, 0, 0, 1])])
            result = homogeneous_transform @ T_imu_lidar
            lidar_transforms[data[i,0]] = result

    # determine if a dense or sparse reference file is used
    if traj_ref.num_poses > 100:
        dense_trajectory = True
    else:
        dense_trajectory = False

    # timesync the reference and estimate trajectories
    max_diff = 2
    traj_ref_sync, traj_est_sync = sync.associate_trajectories(traj_ref, traj_est, max_diff)

    # transform trajectory to the lidar coordinate frame for evaluating gcps
    if 'robot' in est_file:
        lidar_ref_sync, _traj_est_sync = sync.associate_trajectories(lidar_ref, traj_est, max_diff)

        for i in range(0,len(lidar_ref_sync.timestamps)):
            T_odom_lidar = lidar_transforms[traj_est_sync.timestamps[i]]
            gcp_lidar = lidar_ref_sync.positions_xyz[i]
            rot = T_odom_lidar[0:3,0:3]
            transl = T_odom_lidar[0:3,3:4]
            transformed_gcp = rot @ gcp_lidar + transl.T
            traj_est_sync.positions_xyz[i] = transformed_gcp[0]
            
    # align the trajectories
    traj_est_aligned = copy.deepcopy(traj_est_sync)
    umeyama_parameters = traj_est_aligned.align(traj_ref_sync, correct_scale=False, correct_only_scale=False)
    traj_est_aligned_complete = copy.deepcopy(traj_est)
    traj_est_aligned_complete.scale(umeyama_parameters[2])
    traj_est_aligned_complete.transform(lie.se3(umeyama_parameters[0], umeyama_parameters[1]))

    # calculate the metrics
    data = (traj_ref_sync, traj_est_aligned)
    ape_metric = metrics.APE(metrics.PoseRelation.translation_part)
    ape_metric.process_data(data)

    ape_stats = ape_metric.get_all_statistics()

    # plot the trajectories for allowed sites
    if create_plots == True:
        fig = plt.figure(figsize=(15, 7))
        subplot_size = [1, 2]
        ax = fig.add_subplot(subplot_size[0], subplot_size[1], 2)
        subplot = int(str(subplot_size[0])+ str(subplot_size[1])+ str(1))
        plt.subplots_adjust(left=0.05,
                            bottom=0.1,
                            right=0.95,
                            top=0.9,
                            wspace=0.2,
                            hspace=0.2)
        fig.suptitle(os.path.splitext(os.path.basename(est_file))[0], fontsize=16)

        if dense_trajectory:
            traj_by_label = {
                "estimate": traj_est_aligned,
                "reference": traj_ref_sync
            }
            trajectories(fig, traj_by_label, plot.PlotMode.xy, subplot_arg=subplot)

        else:
            traj_by_label = {
                "estimate": traj_est_aligned_complete,
                "evaluated estimate points": traj_est_aligned,
                "reference": traj_ref_sync
            }
            trajectories_custom(fig, traj_by_label, plot.PlotMode.xy, subplot_arg=subplot)

        seconds_from_start = [t - traj_est.timestamps[0] for t in traj_est_sync.timestamps]
        # plot the error over time
        if dense_trajectory:
            error_array_custom(ax, ape_metric.error, x_array=seconds_from_start,
                            statistics={s: v for s, v in ape_stats.items() if s != "sse"},
                            name="APE", title="APE w.r.t. " + ape_metric.pose_relation.value, xlabel="$t$ (s)")
        else:
            error_array_custom(ax, ape_metric.error, x_array=seconds_from_start,
                            statistics={s: v for s, v in ape_stats.items() if s != "sse"},
                            name="APE", title="APE w.r.t. " + ape_metric.pose_relation.value, xlabel="$t$ (s)",
                            marker='o',
                            linestyle='dotted')
        plt.ticklabel_format(style='plain') 
        plt.savefig(output_path+"/"+os.path.basename(os.path.splitext(est_file)[0]) + ".png")
        plt.close('all')

    return [ape_stats, dense_trajectory, traj_est_aligned, traj_ref_sync]


if __name__ == "__main__":
    # check if files where provided in the command line argument
    if len(sys.argv) > 1:
        est_file = sys.argv[1]
        ref_file = sys.argv[2]
    else:
        # uncomment if hardcoded filepaths should be used
        # ref_file =
        # est_file =

        # comment if hardcoded filepaths should be used
        print('use: ./evaluation.py tum_est_file tum_ref_file')
        exit()

    fig = plt.figure(figsize=(15, 7))
    subplot_size = [1, 2]
    ax = fig.add_subplot(subplot_size[0], subplot_size[1], 2)
    subplot = [subplot_size[0], subplot_size[1], 1]
    plt.subplots_adjust(left=0.05,
                        bottom=0.1,
                        right=0.95,
                        top=0.9,
                        wspace=0.2,
                        hspace=0.2)
    fig.suptitle("test", fontsize=16)
    # print(evaluate(est_file, ref_file,fig,subplot,ax))
    extrinsics_robot_path = os.path.join("../groundtruth_2023", "extrinsics_robot.yaml")

    with open(extrinsics_robot_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    
    T_lidar_imu_robot = np.array(data_loaded['lidar0']['T_here_imu0'])
    print(evaluate(est_file, ref_file, "path_to_output_folder", T_lidar_imu_robot))
    plt.show()
    plt.savefig("test.png")
