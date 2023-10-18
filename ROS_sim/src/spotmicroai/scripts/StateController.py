#!/usr/bin/env python
import rospy
from enum import Enum
from std_msgs.msg import Int32

class States(Enum):
    ABORTED=0
    STARTING=10
    IDLE=20
    EXECUTING=30
    STOPPING=40
    ABORTING=50

class StateHandler():

    def __init__(self):
        self.state=States.ABORTED
        self.State_Publisher= rospy.Publisher('spotmicroai/State', Int32, queue_size=10)
        rospy.init_node('StateController', anonymous=True)
        
    def ChangeStateTO(self, newstate):
        if (newstate!=self.state):
            self.state=newstate
            self.State_Publisher.publish(self.state.value)


State=StateHandler()
State.ChangeStateTO(States.STARTING)