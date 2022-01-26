from asyncio import sleep
from re import S, T
import threading
from tkinter import Y
from tkinter.messagebox import NO

from pip import main
import rospy
import numpy as np
from queue import Queue
from sensor_msgs.msg import LaserScan
import time
import pandas

class robot():
    def __init__(self,obj) -> None:
        self.scan=[]
        self.obj_name=obj

    def get_scan(self) -> None:
        pass

    def sub_scan(self) -> None:
        pass

    def print_scan(self) -> None:
        pass
    
    def ros_spin_start(self):
        rospy.spin()



class robot1(robot):
    def __init__(self,obj) :
        super(robot1).__init__()
        self.scan=[]
        self.obj_name=obj
        self.g=[[0]*20]*360
        self.g_most=[[0]]*360
        self.can_get_g_most=False
        self.can_get_point=False
    
    def get_scan(self,msg):
        msgrange=msg.ranges
        
        if len(self.scan) == 20:
            time.sleep(0.5)
            self.scan.append(msgrange)
            self.scan.pop(0)
            
        else:
            self.scan.append(msgrange)
            rospy.loginfo(len(self.scan))
      

    def sub_scan(self):

        topic="/"+str(self.obj_name)+"/scan"
        rospy.Subscriber(topic, LaserScan, self.get_scan)
        rospy.spin()
    
    def get_g_most(self,n=3): 
        while True:
            if self.can_get_g_most:
                for i in range(360):
                    # g=pandas.DataFrame(self.g[i])
                    # median = g.quantile(0.5)
                    # new_median = ((g - median).abs()).quantile(0.50)
                    # max_range = median + n*new_median
                    # min_range = median - n*new_median
                    gi_sum=0
                    lenth=0
                    for j in range(len(self.g[i])):
                        # if self.g[i][j]<=max_range.values and self.g[i][j]>=min_range.values:
                            gi_sum=gi_sum+self.g[i][j]
                            lenth+=1
                    gi_mean=gi_sum/lenth
                    self.g_most[i]=gi_mean
                    rospy.loginfo(gi_mean)
            self.can_get_point=True


    def print_scan(self):
        while True:
            if len(self.scan)>1:
                time.sleep(5)
                # rospy.loginfo(len(self.scan[0]))
    

    def get_g(self):
        while True:
            if len(self.scan)==20:
                for i in range(360):
                    for j in range(20):
                        # print(self.scan[j][i])
                        self.g[i][j]=self.scan[j][i]
                self.can_get_g_most=True

    def publish_point(self):
        topic="/"+str(self.obj_name)+"/scan"+"_pub"
        pub = rospy.Publisher(topic, LaserScan, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        msg=LaserScan()
        msg.angle_max=3.14199995995
        msg.angle_min=--3.14199995995
        msg.angle_increment=0.0175041779876
        msg.time_increment=0.0
        msg.scan_time=0.0
        msg.range_min=0.300000011921
        msg.range_max=30.0
        msg.header.stamp = rospy.Time().now()
        msg.header.frame_id ="robot1/laser"
        msg.intensities=[0.0]*360
        msg.ranges=self.g_most
        while self.can_get_point:
            pub.publish(msg)
            rate.sleep()


    def theard_start(self):
        scan=threading.Thread(target=self.sub_scan)
        print_scan=threading.Thread(target=self.print_scan)
        g=threading.Thread(target=self.get_g)
        g_most=threading.Thread(target=self.get_g_most)
        publish=threading.Thread(target=self.publish_point)
        scan.start()
        print_scan.start()
        g.start()
        g_most.start()
        publish.start()
        scan.join()
        print_scan.join()
        g.join()
        g_most.join()
        publish.join()

    def init_ros(self):
        node="LaserScan"+str(self.obj_name)
        rospy.init_node(node, anonymous=True,disable_signals=True)


    
if __name__ == '__main__':
    robot_f=robot1(obj="robot1")
    robot_f.init_ros()
    robot_f.theard_start()



