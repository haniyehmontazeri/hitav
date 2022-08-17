import math
from imageProccess import *
import cv2
import numpy as np
import config

Config = config.config()

def current(image):
    image_processed_outline = image_processed_outline_getter(np.copy(image))
    image_processed_middle = image_processed_middle_getter(np.copy(image))
    image_processed_middle_line = image_processed_middle_line_getter(np.copy(image))
    line = current_line(image_processed_middle_line , image)

    return {'image' : image ,
      'carSpeed': 0,
      'line' : line,
      'image_processed_outline' : image_processed_outline,
      'image_processed_middle': image_processed_middle,
      'image_processed_middle_line' : image_processed_middle_line}

def current_line(image_processed_middle,image_processed_outline):
    image_processed_middle = croppImg(image_processed_middle , yellowLineMask(image_processed_middle))
    current_line_by_middle = current_line_by_middle_line(image_processed_middle)
    current_line_by_out = current_line_by_out_line(image_processed_outline)
    
    if(current_line_by_middle != 0):
        return [current_line_by_middle[0] , current_line_by_middle[1] , current_line_by_out[1] if current_line_by_out!=0 else -1]
    
    if(current_line_by_out != 0):
        return [current_line_by_out[0] ,-1 , current_line_by_out[1]]
    
    return ['R' , -1 , -1]
    
def current_line_by_middle_line(image):
    spot = np.where(image == 255)
    spots = (image[spot])
    if(spots.size>50):
        spot_x = sum(spot[1])/len(spot[1])
        return( ['L' , spot_x] if  spot_x > 130 else ['R' , spot_x] )
    else:
        return 0

def current_line_by_out_line(image):
    coloredImg = changeColor(image , [45, 255, 255] , [22, 93, 0] )
    gradient = prepareGradient(coloredImg)
    line_image = houghLines(gradient)
    result = croppImg(line_image , outLineMask(line_image))
    spot = np.where(result == 255)
    spots = (result[spot])
    if(spots.size>0):
        spot_x = sum(spot[1])/len(spot[1])
        return( ['R',spot_x] if  spot_x > 130 else ['L',spot_x])
    else:
        return 0

def image_processed_outline_getter(image):
    coloredImg = changeColor(image , [45, 255, 255] , [22, 93, 0] )
    ret, thresh = cv2.threshold(gray(coloredImg), 140, 255, 0)
    crop_road = croppImg(thresh , roadMask(thresh))
    crop_car = croppImg(crop_road , carMask(crop_road))

    Config.ENABLE_VISUALIZATIONS and cv2.imshow("test",crop_car)

    return crop_car

def image_processed_middle_getter(image):
    yellowMask = colorMask(image , [45, 255, 255] , [22, 93, 0] )
    ret, thresh = cv2.threshold((yellowMask), 140, 255, 0)
    crop_car = croppImg(thresh , carMask(thresh))
    return crop_car

def image_processed_middle_line_getter(image):
    yellowMask = colorMask(image , [45, 255, 255] , [22, 93, 0] )
    ret, thresh = cv2.threshold((yellowMask), 140, 255, 0)

    return thresh
    