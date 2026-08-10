# Hilti SLAM Challenge 2023

[<img src="https://img.shields.io/badge/Home_Page-red" alt="Home Page">](https://hilti-challenge.com/dataset-2023)
[<img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow" alt="Hugging Face Dataset">](https://huggingface.co/datasets/Hilti-Research/hilti-slam-challenge-2023)
[<img src="https://img.shields.io/badge/arXiv-2404.09765-b31b1b" alt="arXiv">](https://arxiv.org/abs/2404.09765)


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

### Why did you release a new dataset this late in the competition timeline?
We have identified a vulnerability in our scoring report (APE plot) that indirectly helps estimate ground truth coordinates, and has enabled some teams to falsify results. While we can and will exclude such submissions from the competition leaderboard, we also wish to avoid incorrectly penalizing teams that perform well legitimately. Hence we release an additional dataset location (Site 3) with 4x sequences from the handheld prototype, which will be evaluated but without publishing analysis plots. We also doubled Site 3's per-trajectory score, with a possible maximum of 200 points each. This brings the single session maximum possible score to 1600, the multi-session maximum score to 400.

### The new dataset location Site 3 has sequences with frame drops / data discontinuities, is it intentional?
Yes it is a realistic corner case which we would like for teams to explore.

### This work is awesome! Do you have a paper for this? How may I cite it in my research publication?
Yes we do, you can find our pre-print [here](https://arxiv.org/abs/2404.09765), and in IEEE RA-L. You can cite it using the following Bibtex citation:

```bibtex
@misc{nair2024hiltislamchallenge2023,
      title={Hilti SLAM Challenge 2023: Benchmarking Single + Multi-session SLAM across Sensor Constellations in Construction}, 
      author={Ashish Devadas Nair and Julien Kindle and Plamen Levchev and Davide Scaramuzza},
      journal={IEEE Robotics and Automation Letters},
      number={8},
      pages={7286–7293},
      year={2024},
      DOI={10.1109/lra.2024.3421791}     
}
```