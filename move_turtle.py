#!/usr/bin/env python
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import rospy
import sys
initialtheta = 0
current = 0
count = 0
flag = 0
def callback(tpose):
    pos = tpose
    global count
    global flag
    if (count == 0):
        global initialtheta
        initialtheta = pos.theta
        count += 1
    else:
        global current
        current = pos.theta
    rospy.loginfo('initial: %f; current: %f', initialtheta, current)
    if(abs(current - 3.14) <0.1):
        flag = 1
def move_turtle():
    global count
    rospy.init_node('move_turtle', anonymous = True)
    rospy.Subscriber("/turtle1/pose", Pose, callback)
    vel = Twist()
    global lin_vel
    global ang_vel
    vel.linear.y = 0
    vel.linear.z = 0
    vel.linear.x = lin_vel
    vel.angular.z = ang_vel

    vel.angular.x = 0
    vel.angular.y = 0
    while not rospy.is_shutdown():
        if(flag == 1 and abs(round(current,3) - initialtheta) < 0.1):
            vel.linear.x = 0
            vel.angular.z = 0
            pub.publish(vel)
            rospy.loginfo('reached!')
            break
        rate = rospy.Rate(200)
        pub.publish(vel)
        vel.linear.x = lin_vel
        vel.angular.z = ang_vel
        rospy.loginfo('Linear vel =  %f ; Angular vel = %f', lin_vel, ang_vel)
        rate.sleep()
if __name__ == "__main__":
    try:
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
        lin_vel = float(raw_input('Enter linear velocity: '))
        ang_vel = float(raw_input('Enter angular velocity: '))
        move_turtle()
    except rospy.ROSInterruptException:
        pass
