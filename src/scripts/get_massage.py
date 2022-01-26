#!/home/wdc/anaconda3/envs/pytorch38/bin/python

import rospy
from sensor_msgs.msg import LaserScan
import numpy

def scanCallback(msg):
    rospy.loginfo("LaserScan_msg"+str(msg.ranges))

    

def pose_subscribe():
    rospy.init_node("Lasersacn_robot1", anonymous=True)
    rospy.Subscriber("/robot1/scan", LaserScan, scanCallback)
    rospy.spin()


if __name__ == '__main__':
    g=[[0.0]*20]*360
    g[0][0]=1
    print(g[0])