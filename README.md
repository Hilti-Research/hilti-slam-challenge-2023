# Hilti-SLAM-Challenge-2023


## Hardware Documentation
### Handheld 🎥
[Visit the documentation for the handheld hardware here](documentation/hardware/Handheld.md)


### Robot 🤖
[Visit the documentation for the robot hardware here](documentation/hardware/Robot.md)

## FAQ General

### If we submit the result, are you going to disclose the name of all the participants?
We disclose the names only after prior approval. Before making the leaderboard public I will send out an email to all participants with their respective rank and the option to withdraw.

### What should a multisession submission look like?
The files struccture should be same as that of SLAM Challenge 2022, with individual trajectories in TUM format in a .zip file, with each trajectory's name matching the bag file name with a .txt extension instead of a .bag.
Simply transform all trajectories into the reference frame of the *_1 dataset of that site/location.

### Can I submit a mulltisession SLAM traajectory set as a single session SLAM entry?
Yes, our system compensates for the same :)

### How are results scored?
The submission will be ranked based on the completeness of the trajectory as well as on the position accuracy (ATE). The score is based on the ATE of individual points on the trajectory. Depending on the error between 10 and 0 points are added to your final score. This way also incomplete trajectories can be included in the evaluation. You always can submit your current results and receive an accuracy report using our submission system.

