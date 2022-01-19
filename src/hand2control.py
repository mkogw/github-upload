#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Empty

pub_f = rospy.Publisher('/forward', Empty, queue_size=1)
pub_b = rospy.Publisher('/back', Empty, queue_size=1)
pub_l = rospy.Publisher('/TTL', Empty, queue_size=1)
pub_r = rospy.Publisher('/TTR', Empty, queue_size=1)
pub_s = rospy.Publisher('/stop', Empty, queue_size=1)

# position z >0 

lim_z = 0  # move wheel if z > lim_z
left_up = False; right_up = False

def send_command():
    if left_up and right_up:
        pub_f.publish()
    elif left_up:
        pub_r.publish() # TTR
    elif right_up:
        pub_l.publish() # TTL
    else:
        pub_s.publish()

def cb_left(msg):
    global left_up, right_up
    z = msg.pose.position.z
    if z > lim_z:
        left_up = True
    else:
        left_up = False
    send_command()

def cb_right(msg):
    global left_up, right_up
    z = msg.pose.position.z
    if z > lim_z:
        right_up = True
    else:
        right_up = False

def main():
    rospy.init_node('hand2control')
    rospy.Subscriber('/oculus/left/pose', PoseStamped, cb_left)
    rospy.Subscriber('/oculus/right/pose', PoseStamped, cb_right)

    rate = rospy.Rate(10)

    rospy.spin()
    rate.sleep()

if __name__=='__main__':
    main()