# Hilti SLAM Challenge 2023
[![HSC2023](assets/HSC2023-landscape.jpg?raw=true)](https://hilti-challenge.com/)

Welcome to the the Hilti SLAM Challenge 2023! We look forward to your participation :)

## Hardware Documentation
### Handheld Platform 🎥
[Visit the documentation for the handheld hardware here](documentation/hardware/Handheld.md)


### Robot Platform 🤖
[Visit the documentation for the robot hardware here](documentation/hardware/Robot.md)

## FAQ

### If we submit our results, are you going to disclose the names of all the participants?
We disclose the names only with prior consent. Before making the leaderboard public we will send out an email to all participants with their respective rank and the option to withdraw.

### What should a multisession submission look like?
The files structure should be same as that of SLAM Challenge 2022, with individual trajectories in TUM format in a .zip file, with each trajectory's name matching the bag file name with a .txt extension instead of a .bag.
Simply transform all trajectories into the reference frame of the *_1 dataset of that site/location.

### Can I submit a transformed set of mulltisession SLAM trajectories as a single session SLAM entry?
Yes, our  submission system compensates for the same.

### May I run my own calibration?
Of course! On the [challenge website](https://hilti-challenge.com/), we provide bagfiles for running both intrinsic and extrinsic calibrations. Be aware that in your submission, you should also provide the custom extrinsic so that the adapted transforms can be accounted for in the evaluation. More information about providing custom extrinsics [can be found here](documentation/submissions/Format.md).

### How are trajectory scores calculated?
Our automatic evaluation system compares specific points in submission trajectories with pre-surveyed control points, acquired from a Terrestrial Laser Scanner.
Each point is scored based on it's accuracy, which is in turn based on the Absolute Trajectory Error (ATE) metric:\
<0.5cm → 20 points\
<1cm → 10 points\
<3cm → 6 points\
<6cm → 5 points\
<10cm → 3 points\
<40cm → 1 point\
\>40cm → 0 points\
Then the score for each trajectory (sum of all point scores) is normalized to be in a 0-100 range.
