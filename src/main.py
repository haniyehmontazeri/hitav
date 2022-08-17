#!/usr/bin/env python3
from multiprocessing.connection import wait
from info import info
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import NavSatFix
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
import cv2
from drive import drive
import time
import numpy as np
from preimage import perspectiveTransfrom
from preimage import raceModeImg
from sensor_msgs.msg import LaserScan
import config

bridge = CvBridge()
stopped = False
stoped = False

Config = config.config()

lat = None
long = None
d_lat = 0
d_long = 0
def driveToRoss(speed,angle):
    velocity_publisher = rospy.Publisher('/catvehicle/cmd_vel_safe', Twist, queue_size=10)
    vel_msg = Twist()
    isForward = True

    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    
    vel_msg.angular.z = angle
    vel_msg.angular.y = 1
    vel_msg.linear.x = abs(speed)

    velocity_publisher.publish(vel_msg)

def translate(value, l_min, l_max, r_min, r_max):
    return (value - l_min) * (r_max - r_min) / (l_max - l_min) + r_min

def callback(data):
    global stoped
    global d_long
    global d_lat

    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    frame = raceModeImg(frame)
    
    Config.ENABLE_VISUALIZATIONS and cv2.imshow('image',frame)

    frame = cv2.resize(frame, (210,210))
    cv2.waitKey(1)
 
    dt = time.time() - start
    k = cv2.waitKey(10)
   
    if(k == 97):
        print('Reccord : {}'.format(dt))
    elif(k == 112):
        print('Location : {}, {}'.format(lat, long))
        print('_Location : {}, {}'.format(d_lat, d_long))

        d_lat = lat
        d_long = long

    if(not stoped):
        time.sleep(2)
        stoped=True
    if(not frame is None):
                speed , steering = drive(frame)
                
                steering = -translate(steering[0]*1.0,-100.0,100.0,-1.0,1.0) * 0.9
                speed = translate(speed*1.0, 0.0, 100.0, 0.0, Config.MAX_SPEED)
               
                if(info.deg <= steering):
                    while(info.deg<=steering):
                        driveToRoss(speed,info.deg)
                        info.deg+=0.5
                    info.deg=steering
                else:
                    while(info.deg>=steering):
                        driveToRoss(speed,info.deg)
                        info.deg-=0.5
                    info.deg=steering

def sensorCallback(data):
    info.sensors=list(data.ranges)
   
def gpsCallback(data):
    global lat
    global long
    lat = data.latitude
    long = data.longitude

def receiveImage():
    rospy.init_node("test" , anonymous=True)
    rospy.Subscriber("/catvehicle/front_laser_points", LaserScan, sensorCallback)
    rospy.Subscriber("/catvehicle/camera_front/image_raw_front", Image, callback)
    rospy.Subscriber("/vehicle/gps/fix", NavSatFix, gpsCallback)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node("test" , anonymous=True)
    start = time.time()

    if(not stopped):
        time.sleep(2)
    try:
        receiveImage()
    except rospy.ROSInterruptException: pass
    