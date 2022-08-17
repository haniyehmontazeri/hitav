import time
import numpy as np
from imageProccess import rightCarMask , croppImg
import cv2
from current import current
from arrange import *
from destination import continueSensores, sensores

def rescueLeft(car):
    print("The Correcting Force Horray")
    current_info = current(car)
    info_sensors = current_info["sensors"]
    time_end = time.time()+3
    while(info_sensors[1]<1200 or time_end> time.time()):
        current_info = current(car)
        info_sensors = current_info["sensors"]
        car.setSpeed(-100)
        car.setSteering(0)
    while(True):
        car.setSteering(45)
        car.setSpeed(40)
        info_sensors = current_info["sensors"]
        current_info = current(car)
        out_image = current_info["image_processed_outline"]
        out_image = croppImg(out_image , rightCarMask(out_image))
        out_count = np.count_nonzero(out_image >0)
        if(out_count > 20 and time_end < time.time()):
            break



def change(current_info , destination_info , car):
    print("Start")
    time_end = time.time()+0
    while(True):
        if(destination_info == 'L'):
            Speed=(25)
            return Speed

        elif(destination_info == 'R'):
            Steering=(45)
            return Steering


def goToRight(current_info,destination_info):
    info.data = "right"
    Steering=(35)
    Speed=(85)
    out_image = current_info["image_processed_outline"]
    out_image = croppImg(out_image , rightCarMask(out_image))
    out_count = np.count_nonzero(out_image >10)
    if(continueSensores()!=0):
            info.data = "change"
            info.change_before=False
    if(out_count > 30):
        info.data =""

    return [Speed , [Steering,1]]

def change_cycle(current_info,destination_info):
    info.data="change"
    if(destination_info == 'L'):
        Speed=(70)

        Steering=(-40)
     
        if(continueSensores()==0):
            info.data = ""
    elif(destination_info == 'R'):
        Steering=(40)

        Speed=(70)

        out_image = current_info["image_processed_outline"]
        out_image = croppImg(out_image , rightCarMask(out_image))
        out_count = np.count_nonzero(out_image >0)
        if(out_count > 20):
            info.data =""

    return [Speed , [Steering,1] ]
