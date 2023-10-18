#!/usr/bin/python3


# Type keyboard inputs into the terminal where spotmicroai.launch is run

from __future__ import print_function

import threading

import roslib; # roslib.load_manifest('teleop_twist_keyboard')
import rospy

# from geometry_msgs.msg import Twist
# from geometry_msgs.msg import TwistStamped
from std_msgs.msg import String

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


# TwistMsg = Twist
StrMsg = String

msg = """
Reading from the keyboard  and Publishing to String!
---------------------------
Moving around:
       w
    a  s  d

w: up
s: down
d: right
a: left

anything else : stop

CTRL-C to quit
"""
moveBindings = {
        'w': 'up1',
        's': 'down1',
        'd': 'right1',
        'a': 'left1',
        'j': 'up2',
        'k': 'down2',
        'l': 'right2',
        ';': 'left2'
    }

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('pushed', StrMsg, queue_size = 10)
        self.in_letter = ''
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, letter):
        self.condition.acquire()
        self.in_letter = letter
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update('')
        self.join()

    def run(self):
        str_msg = StrMsg()
        string = str_msg
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into string message.
            string.data = self.in_letter
            self.condition.release()

            # Publish.
            self.publisher.publish(str_msg)

        # Publish stop message when thread exits.
        string.data = ''
        self.publisher.publish(str_msg)


def getKey(settings, timeout):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__=="__main__":
    settings = saveTerminalSettings()

    rospy.init_node('string_keyboard')

    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.5)
    pub_thread = PublishThread(repeat)

    input_str = ''

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update('')

        print(msg)
        while(1):
            key = getKey(settings, key_timeout)
            if key in moveBindings.keys():
                input_str = moveBindings[key]
                print("received: ", input_str)
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and input_str == '':
                    continue
                input_str = ''
                if (key == '\x03'):
                    break

            pub_thread.update(input_str)

    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        restoreTerminalSettings(settings)