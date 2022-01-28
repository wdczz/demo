from select import select
from tkinter import N
import rospy
import numpy as np
from queue import Queue
from sensor_msgs.msg import LaserScan
import time 
import pandas
import multiprocessing as mp
import threading 
import math

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
        self.g=None
        self.g_most=None
        self.can_get_point=False
        self.scan_array=None
        self.can_get_g=False
        self.move=None
        self.map=None
        self.can_get_move=False
        self.now_info=None
    
    def get_scan(self,msg):
        msgrange=msg.ranges
        self.now_info=np.array(msgrange)
        if len(self.scan) == 20:
            time.sleep(0.001)
            self.scan.append(msgrange)
            self.scan.pop(0)
            self.scan_array=np.array(self.scan)
            self.can_get_g=True
        else:
            self.scan.append(msgrange)
            rospy.loginfo(len(self.scan))


    def get_move(self):
        while True:
            if len(self.scan) == 20 and self.can_get_point==True:
                move=self.now_info-self.g_most
                self.move=self.now_info
                for i in range(360):
                    if math.fabs(move[i])<0.05:
                        self.move[i]=0
                self.can_get_move=True
    
      

    def sub_scan(self):
        topic="/"+str(self.obj_name)+"/scan"
        rospy.Subscriber(topic, LaserScan, self.get_scan)
        rospy.spin()


    def print_scan(self):
        while True:
            if len(self.scan)==20:
                rospy.loginfo(self.scan_array)


    def get_g(self):
        while True:
            if len(self.scan)==20 and self.can_get_g==True:
                scan_copy=self.scan_array
                self.g=scan_copy.T
                self.g_most=np.sum(self.g,1)/20
                self.can_get_point=True

    def publish_move(self):
        topic="/"+str(self.obj_name)+"/move"+"_pub"
        pub = rospy.Publisher(topic, LaserScan, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        msg=LaserScan()
        msg.angle_max=3.14199995995
        msg.angle_min=-3.14199995995
        msg.angle_increment=0.0175041779876
        msg.time_increment=0.0
        msg.scan_time=0.0
        msg.range_min=0.300000011921
        msg.range_max=30.0
        msg.header.stamp = rospy.Time().now()
        msg.header.frame_id =str(self.obj_name)+"/laser"
        msg.intensities=[125.0]*360
        while True:
            if self.can_get_move:
                msg.ranges=self.move
                pub.publish(msg)
                rate.sleep()
                
    def publish_point(self):
        topic="/"+str(self.obj_name)+"/scan"+"_pub"
        pub = rospy.Publisher(topic, LaserScan, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        msg=LaserScan()
        msg.angle_max=3.14199995995
        msg.angle_min=-3.14199995995
        msg.angle_increment=0.0175041779876
        msg.time_increment=0.0
        msg.scan_time=0.0
        msg.range_min=0.300000011921
        msg.range_max=30.0
        msg.header.stamp = rospy.Time().now()
        msg.header.frame_id =str(self.obj_name)+"/laser"
        msg.intensities=[0.0]*360
        while True:
            if self.can_get_point:
                msg.ranges=self.g_most
                pub.publish(msg)
                rate.sleep()


    def theard_start(self):
        scan=threading.Thread(target=self.sub_scan)
        g=threading.Thread(target=self.get_g)
        get_move=threading.Thread(target=self.get_move)
        publish=threading.Thread(target=self.publish_move)
        scan.start()
        g.start()
        get_move.start()
        publish.start()
        scan.join()
        get_move.join()
        g.join()
        publish.join()

    def init_ros(self):
        node="LaserScan"+str(self.obj_name)
        rospy.init_node(node, anonymous=True,disable_signals=True)


    
if __name__ == '__main__':
    robot_f=robot1(obj="robot1")
    robot_f.init_ros()
    robot_f.theard_start()

    



