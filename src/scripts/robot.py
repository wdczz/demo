from asyncio import sleep
from turtle import radians
from means_shift import *
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
        self.move_zzb=None
        self.move_with_class=np.empty([360,2]) 
        self.means_shift_ok=False
    
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
                    if math.fabs(move[i])<0.1:
                        self.move[i]=0
                self.can_get_move=True

    def get_means_shift(self):
        while True:
            if self.means_shift_ok:
                class_num=0
                for i in range(360):
                    if euclidean_dist([0,0],self.move_zzb[i])[0]>0.1:
                        if i==0:
                            class_num+=1
                            self.move_with_class[i]=(class_num,self.move[i])
                        else :
                            if euclidean_dist(self.move_zzb[i-1],self.move_zzb[i])[0]<=0.5:
                                self.move_with_class[i]=(class_num,self.move[i])
                            else :
                                class_num+=1
                                self.move_with_class[i]=(class_num,self.move[i])
                print("class number is {}".format(class_num))



        
    def get_zjzbx(self):
        while True:
            move_zzb=[]
            if self.can_get_move==True:
                for i in range(360):
                    x=self.move[i]*math.cos(math.radians(i))
                    y=self.move[i]*math.sin(math.radians(i))
                    move_zzb.append((x,y))
                self.move_zzb=np.array(move_zzb)
                self.means_shift_ok=True


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
                self.g_most=np.median(self.g,1)
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
        means_shift=threading.Thread(target=self.get_means_shift)
        get_zjzbx=threading.Thread(target=self.get_zjzbx)
        scan.start()
        g.start()
        get_move.start()
        publish.start()
        means_shift.start()
        get_zjzbx.start()
        scan.join()
        get_move.join()
        g.join()
        publish.join()
        means_shift.join()
        get_zjzbx.join()

    def init_ros(self):
        node="LaserScan"+str(self.obj_name)
        rospy.init_node(node, anonymous=True,disable_signals=True)


    
if __name__ == '__main__':
    robot_f=robot1(obj="robot1")
    robot_f.init_ros()
    robot_f.theard_start()

    



