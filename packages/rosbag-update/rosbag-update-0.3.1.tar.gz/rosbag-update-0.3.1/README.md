# Rosbag update
Updates topic data types on ROS bags, solves checksum errors.
Doesn't need any migration file.


# Requirements
Requires the new ros message to be imported and following the structure of `{package}/msg/{messagename}.msg` for example you should be able to import message in python with `from mypackage.msg import MyMessage`

# Installation
```
pip install rosbag-update
```
OR
```
pip3 install rosbag-update
```

# Run
```
rosbag_update -b [bag-path]
```

# Notes
- Please ignore the error message `Failed to load Python extension for LZ4 support. LZ4 compression will not be available.`
  