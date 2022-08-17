import cv2
import numpy as np

def displayLines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image

def houghLines(image):
    lines=cv2.HoughLinesP(image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
    result = displayLines(image,lines)
    return result

def croppImg(image , mask):
    return cv2.bitwise_and(image,mask)

def rightCarMask(image):
	polygons =np.array([
	[(130,250),(130,140),(220 , 140)]
	])

	polygons2 =np.array([
	[(130,250),(220,140),(220,250)]
	])
	mask =np.zeros_like(image)
	mask2 =np.zeros_like(image)
	cv2.fillPoly(mask,polygons,255)
	cv2.fillPoly(mask2,polygons2,255)
	main_mask = cv2.bitwise_or(mask2,mask)
	return main_mask

def colorMask(image , high , low):
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, np.array(low), np.array(high))
    return mask

def changeColor(image , high , low):
    mask = colorMask(image,high , low)
    image[mask>0] = [0,0,0]

    return image

def gray(image):
    return cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)

def prepareGradient(image):
    gray_img = cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)
    
    blurred_img = cv2.GaussianBlur(gray_img , (5,5) ,0)
    
    gradient = cv2.Canny(blurred_img , 230,250)

    return gradient

def carMask(image):
	polygons =np.array([
	[(45,250),(45,150),(215 , 150)]
	])

	polygons2 =np.array([
	[(45,250),(215,150),(215,250)]
	])
	mask =np.zeros_like(image)
	mask2 =np.zeros_like(image)
	cv2.fillPoly(mask,polygons,255)
	cv2.fillPoly(mask2,polygons2,255)
	main_mask = cv2.bitwise_or(mask2,mask)
	return main_mask

    
def sensorLineMask(image):
	polygons =np.array([
	[(55,250),(55,170),(210 , 170)]
	])

	polygons2 =np.array([
	[(55,250),(210,170),(210,250)]
	])
	mask =np.zeros_like(image)
	mask2 =np.zeros_like(image)
	cv2.fillPoly(mask,polygons,255)
	cv2.fillPoly(mask2,polygons2,255)
	main_mask = cv2.bitwise_or(mask2,mask)
	return main_mask

def roadMask(image):
    polygons3 =np.array([
    [(0,210),(255,144),(69,84)]
    ])
    polygons4 =np.array([
    [(0,210),(255,144),(250,250)]
    ])
    mask =np.zeros_like(image)
    mask2 =np.zeros_like(image)
    cv2.fillPoly(mask,polygons3,255)
    cv2.fillPoly(mask2,polygons4,255)
    return cv2.bitwise_or(mask2,mask)

def yellowLineMask(image):
    polygons3 =np.array([
    [(0,120),(0,255),(255,255)]
    ])
    polygons4 =np.array([
    [(0,120),(255,120),(255,255)]
    ])
    mask =np.zeros_like(image)
    mask2 =np.zeros_like(image)
    cv2.fillPoly(mask,polygons3,255)
    cv2.fillPoly(mask2,polygons4,255)
    return cv2.bitwise_or(mask2,mask)

def outLineMask(image):
    polygons3 =np.array([
    [(0,190),(0,255),(255,255)]
    ])
    polygons4 =np.array([
    [(0,190),(255,190),(255,255)]
    ])
    mask =np.zeros_like(image)
    mask2 =np.zeros_like(image)
    cv2.fillPoly(mask,polygons3,255)
    cv2.fillPoly(mask2,polygons4,255)
    return cv2.bitwise_or(mask2,mask)
