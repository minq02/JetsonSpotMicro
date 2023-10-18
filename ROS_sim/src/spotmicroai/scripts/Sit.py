#!/usr/bin/python3
import rospy
from std_msgs.msg import Float64, String
import time
from Helpers.kinematics import Kinematic
from Helpers.Input import Input
from spotmicroai.msg import LegCommand
from enum import Enum

#TODO: global sucks
global key

#Classes definitions
class Positions():
    Agachado=[-55,-100,20]
    Arriba=[-55,-190,20]
    SitFront=[-55,-260,20]
    SitBack=[-55,-160,20]
    Test=[0,0,0]

class movements:

    def __init__(self):
        self.k=Kinematic()
        self.posiciones=Positions()

        #Initialize publishers
        self.MoveLegs=rospy.Publisher('spotmicroai/MoveLegs', LegCommand,queue_size=10)

        #Initialize Ros node
        rospy.init_node('Movimiento', anonymous=True)

    def Move(self, Legs, Posicion):
        
        #Get angles
        angles=self.k.legIK(Posicion)     

        #Prepare data for the msg
        msg=LegCommand()
        msg.Angles[0]=angles[0]
        msg.Angles[1]=angles[1]
        msg.Angles[2]=angles[2]

        msg.Legs=Legs
        #publish the msg
        self.MoveLegs.publish(msg)


#function definitions
def JoyStick_callback(data):
    global key
    key=data.data


#TEST!
movimiento = movements()
Posiciones=Positions()
Inputs=Input()

global key

key=" "
last=key
rospy.Subscriber("JoyStick", String, JoyStick_callback)
rospy.sleep(1)
while not rospy.is_shutdown():

    if key!=last and key !="stop":
        print(key)
        if key=="right":
            Legs=[0,0,1,1]
            movimiento.Move(Legs,Posiciones.SitBack)
            Legs=[1,1,0,0]
            movimiento.Move(Legs,Posiciones.SitFront)
        elif key=="up":
            Legs=[1,1,1,1]
            movimiento.Move(Legs,Posiciones.Arriba)
        elif key=="down":
            Legs=[1,1,1,1]
            movimiento.Move(Legs,Posiciones.Agachado)
        last=key
    

