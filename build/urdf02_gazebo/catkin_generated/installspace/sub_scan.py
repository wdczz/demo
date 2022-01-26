#!/usr/bin/env python2
import rospy
from sensor_msgs.msg import LaserScan

data1=[]
data2=[]

def listener():
    global data1
    global data2
    rospy.init_node('get_laser')

    while not rospy.is_shutdown():
        rospy.sleep(1)
        data1 = rospy.wait_for_message("robot1/scan", LaserScan, timeout=None)
        data2 = rospy.wait_for_message("robot2/scan", LaserScan, timeout=None)
        rospy.loginfo(data1.ranges)
        # rospy.loginfo(data2.ranges)

if __name__ == '__main__':
    listener()




# robot1_data_ranges=[]

# def callback(s):
#     global robot1_data_ranges
#     #LaserScan的数据结构
#     #std_msgs/Header header
#     #float32 angle_min
#     #float32 angle_max
#     #float32 angle_increment
#     #float32 time_increment
#     #float32 scan_time
#     #float32 range_min
#     #float32 range_max
#     #float32[] ranges
#     #float32[] intensities
#     #rospy.loginfo(s.ranges)
#     robot1_data_ranges=s.ranges



# def listener():

#         rospy.init_node('lasr_listener', anonymous=False)
#         rospy.Subscriber('robot1/scan', LaserScan,callback)
#         rospy.spin()




    
# class ranges():
#     def __init__(self):
#         self.scan_ranges=[]

#     def get_scan_origin(self,s):
#                         #LaserScan的数据结构
#                         #std_msgs/Header header
#                         #float32 angle_min
#                         #float32 angle_max
#                         #float32 angle_increment
#                         #float32 time_increment
#                         #float32 scan_time
#                         #float32 range_min
#                         #float32 range_max
#                         #float32[] ranges
#                         #float32[] intensities
#                             #self.scan_ranges=list(self.ranges)
#         self.scan_ranges=list(s.ranges)
#         #rospy.loginfo(self.scan_ranges)
        
        

#     def listener(self):
#         rospy.init_node('lasr_listener', anonymous=False)
#         rospy.Subscriber('robot1/scan', LaserScan,self.get_scan_origin)
#         rospy.spin()


# if __name__ == '__main__':
#     robot1_data = ranges()
#     robot1_data.listener()
#     rospy.loginfo(robot1_data.scan_ranges)
