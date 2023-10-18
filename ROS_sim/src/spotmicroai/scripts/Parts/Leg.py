#!/usr/bin/python3
import rospy
import sys
from enum import Enum
from std_msgs.msg import Float64
from spotmicroai.msg import LegCommand, ServoCommand

#Callback for the subscriber
def MoveLeg(data):
    Verbose=0
    if data.Legs[number]==1:

        rate = rospy.Rate(100) # 100 Hz
        if Verbose==1:
            print("[ INFO] Moving "+ name)
        pub.publish(data.Angles)
        rate.sleep()

if __name__ == '__main__':

    #Initialize the node
    rospy.init_node("~name", anonymous=True)

    #Get node name
    name = rospy.get_param('~name', 'Leg_0')
    number = rospy.get_param('~number', 0)
    print("[ INFO] "+name +" node initialized")

    #Create the Servo publishers
    pub = rospy.Publisher('spotmicroai/MoveLegs/'+name, ServoCommand,queue_size=10)

    #Create the subscriber for the comands
    rospy.Subscriber('spotmicroai/MoveLegs', LegCommand, MoveLeg)

    rospy.spin()