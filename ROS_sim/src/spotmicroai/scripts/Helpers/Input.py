#!/usr/bin/python3
import rospy
import os
from std_msgs.msg import String

class Input():

    def __init__(self):
        rospy.Subscriber("pushed", String, self.callback)
        self.pub = rospy.Publisher('JoyStick', String, queue_size=10)

    def callback(self,data):
        key=data.data
        if key == "up1":
            self.pub.publish("up")
        elif key == "down1":
            self.pub.publish("down")
        elif key == "right1":
            self.pub.publish("right")
        elif key == "left1":
            self.pub.publish("left")
        elif key == "up2":
            self.pub.publish("stop")
        elif key == "down2":
            self.pub.publish("stop")
        elif key == "right2":
            self.pub.publish("stop")
        elif key == "left2":
            self.pub.publish("stop")