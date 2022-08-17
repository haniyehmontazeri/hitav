#!/usr/bin/env python
import cv2
import random as rng
import numpy as np
import time

def roadMask(image):
    polygons3 =np.array([
    [(0,500),(800,500),(800,700)]
    ])
    polygons4 =np.array([
    [(0,700),(800,700),(0,500)]
    ])
    mask =np.zeros_like(image)
    mask2 =np.zeros_like(image)
    cv2.fillPoly(mask,polygons3,255)
    cv2.fillPoly(mask2,polygons4,255)
    return cv2.bitwise_or(mask2,mask)

def perspectiveTransfrom(image):
    points1 = np.array([[100,450], [700, 450], [0, 800],[800, 800]], np.float32)
    points2 = np.array([[0,0], [800,0], [0, 800], [800, 800]], np.float32)

        
    getPrespective = cv2.getPerspectiveTransform(points1, points2)
    out = cv2.warpPerspective(image, getPrespective, (800,800))
    return out

def unPerspectiveTransfrom(image):
    points2 =np.array([[100,450], [700, 450], [0, 800],[800, 800]], np.float32)
    points1 = np.array([[0,0], [800,0], [0, 800], [800, 800]], np.float32)
    getPrespective = cv2.getPerspectiveTransform(points1, points2)
    out = cv2.warpPerspective(image, getPrespective, (800,800))
    return out

def blackBox(image):
    polygons3 =np.array([
    [(360,740),(440,740),(435,675)]
    ])
    polygons4 =np.array([
    [(435,675),(365,675),(360,740)]
    ])
    mask =np.zeros_like(image)
    mask2 =np.zeros_like(image)
    cv2.fillPoly(image,polygons3,[43,43,43])
    cv2.fillPoly(image,polygons4,[43,43,43])
    return image

def rowMask(image,number):
    polygons3 =np.array([
    [(0,440+(number*24)),(800,440+(number*24)),(800,800)]
    ])
    polygons4 =np.array([
    [(0,800),(800,800),(0,440+(number*24))]
    ])
    mask =np.zeros_like(image)
    mask2 =np.zeros_like(image)
    cv2.fillPoly(mask,polygons3,255)
    cv2.fillPoly(mask2,polygons4,255)
    return cv2.bitwise_or(mask2,mask)

def rectMask(image,rect):
    mask =np.zeros_like(image)
    if(rect==False):
        return mask
    cv2.rectangle(mask,rect[0],rect[1],255,-1)
    return mask

def doRow(image,number):
    rMask = rowMask(image,number)

def croppImg(image , mask):
    return cv2.bitwise_and(image,mask)

def raceModeImg(image):
    a=time.time()
    image = blackBox(image)
    image = perspectiveTransfrom(image)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 170, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), dtype=np.uint8)
    max_line_score=-1
    out_max_line_score=-1
    rectangle_mask=False
    out_rectangle_mask=False
    for i in range(len(contours)):
        cnt=contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        line_score=(w+h)+(abs(800-y)+abs(400-x))
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (x,y+100)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        if(line_score<1200 and line_score>150 and h>10 and w>10):
            if(w+h>max_line_score):
                max_line_score=w+h
                rectangle_mask=np.copy(cnt)
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            cv2.drawContours(image, [cnt], 0, (0,255,255), cv2.FILLED)
        elif(line_score>=1200):
            if(w+h>out_max_line_score):
                out_max_line_score=w+h
                out_rectangle_mask=[(x,y),(x+w,y+h)]
    max_y=560
    min_y=0
    if(out_rectangle_mask is not None):
        masked_thresh=croppImg(thresh,rectMask(thresh,out_rectangle_mask))
        
        blurred_img = cv2.GaussianBlur(masked_thresh , (5,5) ,0)
        
        gradient = cv2.Canny(blurred_img , 230,250)
        pass
    if(rectangle_mask is not None):
        try:
            rect = cv2.minAreaRect(rectangle_mask)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            dot1 = ((box[0][0]+box[1][0])//2,box[0][1])
            dot2 = ((box[2][0]+box[3][0])//2,box[2][1])
            if(dot2[1]<dot1[1]):
                dot2,dot1=dot1,dot2

            x_dis_org=abs(box[1][0]-box[0][0])
            y_dis_org=abs(box[1][1]-box[0][1])
            dot3_y=200
            dot3_x=dot1[0]+(abs(dot1[1]-dot3_y)/x_dis_org*y_dis_org)
            dot4_y=800
            dot4_x=dot2[0]-(abs(dot2[1]-dot4_y)/x_dis_org*y_dis_org)
            dot3=(dot3_x,dot3_y)
            dot4=(dot4_x,dot4_y)
            cv2.line(image,dot3,dot2,(0,255,255),abs(box[0][0]-box[1][0]))
            cv2.line(image,dot4,dot2,(0,255,255),abs(box[0][0]-box[1][0]))
        except:
            pass
    
    b=time.time()
    return unPerspectiveTransfrom(image)

    return image

def displayLines(image,lines):
    m=0
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(image,(x1,y1),(x2,y2),(0,0,255),15)
            m+=1
    print(m)
    return image
