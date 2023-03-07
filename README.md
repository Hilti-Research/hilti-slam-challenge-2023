# Hilti-SLAM-Challenge-2023
Welcome to the the Hilti SLAM Challenge 2023!
This repository contains a collection of information + links pertaining to competition specifics. 
We look forward to your participation :)

## Hardware Documentation
### Handheld Platform 🎥
[Visit the documentation for the handheld hardware here](documentation/hardware/Handheld.md)


### Robot Platform 🤖
[Visit the documentation for the robot hardware here](documentation/hardware/Robot.md)

## FAQ

### If we submit the result, are you going to disclose the names of all the participants?
We disclose the names only with prior consent. Before making the leaderboard public we will send out an email to all participants with their respective rank and the option to withdraw.

### What should a multisession submission look like?
The files struccture should be same as that of SLAM Challenge 2022, with individual trajectories in TUM format in a .zip file, with each trajectory's name matching the bag file name with a .txt extension instead of a .bag.
Simply transform all trajectories into the reference frame of the *_1 dataset of that site/location.

### Can I submit a transformed set of mulltisession SLAM trajectories as a single session SLAM entry?
Yes, our  submission system compensates for the same.



