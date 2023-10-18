#!/usr/bin/python3
import rospy
import sys
from enum import Enum
from std_msgs.msg import Float64
from spotmicroai.msg import ServoCommand


def MoveServo(data):
    Verbose=1
    rate = rospy.Rate(100) # 100 Hz
    if Verbose==1:
        print("[ INFO] Moving "+ ServoName+" to "+str(data.Angles[ServoNumber]))

    for i in range (0,50):
        pub.publish(data.Angles[ServoNumber])
        rate.sleep()

            
if __name__ == '__main__':

    #Initialize the node
    rospy.init_node("~name", anonymous=True)

    #Get node name
    LegName = rospy.get_param('~LegName', 'Servo')
    ServoNumber = rospy.get_param('~ServoNumber', 0)
    ServoName = rospy.get_param('~ServoName', 'NULL')
    print("[ INFO] "+ServoName +" node initialized")

    #Create the subscriber for the comands
    rospy.Subscriber('spotmicroai/MoveLegs/'+LegName, ServoCommand, MoveServo)

    #Create the servo publishers
    pub = rospy.Publisher('spotmicroai/'+ServoName+'_position_controller/command', Float64,queue_size=10)

    rospy.spin()