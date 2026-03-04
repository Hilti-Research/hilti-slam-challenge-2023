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

from evaluation import *

def compare_trajectories(traj_files):
    trajs = []

    for f in traj_files:
        tum_traj = file_interface.read_tum_trajectory_file(f)
        trajs.append(tum_traj)

    # timesync the reference and estimate trajectories
    max_diff = 2
    traj_ref_sync, traj_est_sync = trajs #sync.associate_trajectories(trajs[0], trajs[1], max_diff)

    # calculate the metrics
    data = (traj_ref_sync, traj_est_sync)
    ape_metric = metrics.APE(metrics.PoseRelation.translation_part)
    ape_metric.process_data(data)

    ape_stats = ape_metric.get_all_statistics()

    # plot the trajectories
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
    fig.suptitle(os.path.splitext(os.path.basename(traj_files[0]))[0], fontsize=16)

    traj_by_label = {
                "custom eval worse trajectory": traj_ref_sync,
                "custom eval better trajectory": traj_est_sync
            }
    seconds_from_start = [t - traj_est_sync.timestamps[0] for t in traj_ref_sync.timestamps]        

    trajectories_custom(fig, traj_by_label, plot.PlotMode.xy, subplot_arg=subplot)
    error_array_custom(ax, ape_metric.error, x_array=seconds_from_start,
                            statistics={s: v for s, v in ape_stats.items() if s != "sse"},
                            name="APE", title="APE w.r.t. " + ape_metric.pose_relation.value, xlabel="$t$ (s)",
                            marker='.',
                            linestyle='dotted')
    plt.ticklabel_format(style='plain') 
    # recompute the ax.dataLim
    #ax.relim()
    # update ax.viewLim using the new dataLim
    #ax.autoscale_view()
    plt.show()

    return 0



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f'Usage: ./track_trajectories.py trajectory_1 trajectory_2', file=sys.stderr)
    else:
        trajs = [sys.argv[1], sys.argv[2]]
        compare_trajectories(trajs)

