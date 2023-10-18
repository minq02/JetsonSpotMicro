# Ros based control with Gazebo simulation for SpotmicroAI

This repository has all you need for running a complete simulation of SpotMicro in the Gazebo enviroment. It also adds a small ROS workspace as an example of its integration with the simulation.

## Instalation

This proyect has been developed with ubuntu 18.04 and ROS melodic. It should work with other versions but it has not been tested yet.
In order to get the simulation working you need to install ROS with Gazebo into your pc. Please visit the [ROS](https://www.ros.org/) page for more information about installing ROS.

Once you have ROS installed, you only need to clone this repo into the src folder of your catkin workspace (~/catkin_ws/src) and build via catkin_make.

## Running the simulation

To run the simulation you can use the launch file included in the repo:

```
roslaunch spotmicroai_description SpotMicroAi.launch 
```

To can visualize the topics that command the position for the joint controlers via: 

```
rostopic list
```

You can move the joints by publishing in the right topic:
```
rostopic pub  spotmicroai/rear_left_foot_position_controller/command std_msgs/Float64 "data: -0.5"
```

You can also create a publisher node for doing this. An example node is located in the spotmicroai/sripts folder. I have recently added a launcher to create and controll all the nodes. To run it juts open another terminal and run:
```
roslaunch spotmicroai spotmicroai.launch
```


## Credits
You can see the original Gitlab repository of this proyect at https://gitlab.com/custom_robots and find more information in the proyect webpage: https://spotmicroai.readthedocs.io/en/latest/
