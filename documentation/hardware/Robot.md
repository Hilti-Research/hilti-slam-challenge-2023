# Robot Hardware

In this year's SLAM challenge, for the first time, we provide a dataset which was recorded with a robot. In the following, you find an overview about the system.

## System Overview

The robot used to record the datasets is a minimalistic version of the [Hilti JaiBot](https://www.hilti.group/content/hilti/CP/XX/en/company/media-relations/media-releases/Jaibot.html). We have equipped the system with a [XSens MTi-600](https://www.xsens.com/hubfs/Downloads/Leaflets/MTi%20600-series%20Datasheet.pdf) IMU, a [Robosense Bpearl](https://www.robosense.ai/en/rslidar/RS-Bpearl) LiDAR and four [OAK-D Pro PoE](https://docs.luxonis.com/projects/hardware/en/latest/pages/NG9097prow.html) cameras. An overview of the coordinate systems can be seen in the following image:

**TODO ADD IMAGE**


## Synchronization

All sensors (except for track odometry) are hardware synchronized. A PTP master is running on the NIC of the main PC. The LiDAR sensor is synchronized directly to the master via PTP. The clock of the IMU is synchronized via a PTP-to-trigger conversion board. The same board also triggers the cameras start-of-exposure. All cameras start their exposure simultaneously, but every stereo camera pair runs its own auto-exposure algorithm. Each stereo camera pair uses the same exposure.

The clocks of the IMU and the LiDAR are expected to be synchronized within 1ms accuracy. The clocks of the IMU and the cameras are expected to be synchronized within 2ms accuracy.

## Calibration

## Datasets

### Topics

### Dataset Descriptions

## FAQ Robot