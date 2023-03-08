# Submission Format

Submissions can be handed in by uploading a `.zip` file with a list of text files named after the rosbag files, containing the trajectories

    submission.zip
        site1_handheld_1.txt
        site1_handheld_2.txt
        site1_handheld_3.txt
        site1_handheld_4.txt
        site1_handheld_5.txt
        site2_robot_1.txt
        site2_robot_2.txt
        site2_robot_3.txt

## Trajectory Format
The text files should have the trajectory of the IMU expressed in your map frame in the following format:

    # timestamp_s tx ty tz qx qy qz qw
    1674210305.3000805 0.0 0.0 0.0 0.0 0.0 0.0 1.0
    ...

For participating in the multisession category, all trajectories of a site location must be expressed in the same map frame.

## Extrinsic Format
In case that you run your own calibration (offline or online), it is highly recommended to provide the custom extrinsics inside the `.zip` file. You can do that by adding the files `extrinsics_robot.yaml` and `extrinsics_handheld.yaml` to the `.zip` file with the same format as the output of [MultiCal](https://github.com/zhixy/multical). If no such file is provided, the evaluation uses the default calibration.

Specifically, as the ground control points are measured in LiDAR frame but your trajectory is submitted in IMU frame, we need to know the **transform between IMU and LiDAR** to properly evaluate your results. An example for such a calibration [can be found here](examples/extrinsics_robot.yaml). In the example, you see that we need the transform of the IMU expressed in LiDAR frame, called `T_here_imu0` in the `yaml` file.

Given that you add custom LiDAR-IMU extrinsics to your submission, the `.zip` file would look like

    submission.zip
        site1_handheld_1.txt
        site1_handheld_2.txt
        site1_handheld_3.txt
        site1_handheld_4.txt
        site1_handheld_5.txt
        site2_robot_1.txt
        site2_robot_2.txt
        site2_robot_3.txt
        extrinsics_handheld.yaml
        extrinsics_robot.yaml
