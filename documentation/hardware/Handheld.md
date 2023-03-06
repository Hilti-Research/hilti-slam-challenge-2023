# Handheld Hardware


## System Overview
<img src="images/handheld/frames1.png" alt="Trailblazer Frames 1" width="600">

## Synchronization

## Calibration

## Datasets

## FAQ Handheld

### We noticed that the timestamp for every point in a lidar point cloud scan is equal. Is it possible to correct this issue?
The Hesai ros driver stores the timestamp in [this struct](https://github.com/HesaiTechnology/HesaiLidar_General_ROS/blob/master/src/HesaiLidar_General_SDK/src/PandarGeneralRaw/include/pandarGeneral/point_types.h). What happens is the `sensor_msgs/PointCloud2` Message has a "data" member in byte and it stores the `PointXYZIT` defined time, xyz, etc. The "field" member describes what type of info is in "data". In a programme, one would convert the `PointCloud2` msg into `PointXYZIT` msg to access all the element pandar records.

### Is there a URDF model of the sensor setup?
Yes, now there is! You can clone and compile the following ROS packages:
- [`phasma_description`](https://github.com/Hilti-Research/phasma_description.git): this is the main URDF model of the sensor setup.
- [`hesai_description`](https://github.com/Hilti-Research/hesai_description): this is the URDF model of the HESAI. It's a dependency of `phasma_description`.
- [`alphasense_description`](https://github.com/Hilti-Research/alphasense_description): this is the URDF of the Alphasense. It's a dependency of `phasma_description`.

To have them in you system you can just clone and compile them in your catkin workspace, for example:
```
cd ~/catkin_ws/src/
git clone https://github.com/Hilti-Research/phasma_description.git
git clone https://github.com/Hilti-Research/hesai_description.git
git clone https://github.com/Hilti-Research/alphasense_description.git
cd ..
catkin build phasma_description
```