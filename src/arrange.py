import numpy as np
import cv2
from info import info

def arrange(current_info , destination_info):
    outline_space = current_info["line"][2]
    middle_space = current_info["line"][1]
    line = current_info["line"][0]
    outline_ofset = abs(130 - outline_space)
    out_image=current_info["image_processed_outline"]
    mid_image=current_info["image_processed_middle"]
    out_count = np.count_nonzero(out_image >0)*2.7
    mid_count = np.count_nonzero(mid_image > 0 )*0.917
    out_hoghlines=cv2.HoughLinesP(out_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
    mid_houghlines=cv2.HoughLinesP(mid_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)

    l = []
    if out_hoghlines is not None:
        for hline in out_hoghlines:
            x1,y1,x2,y2=hline.reshape(4)
            if(line == 'R' and x1 < 125):
                x1 = x1+125-x1+125-x1
            
            if(line == 'R' and x2 < 125):
                x2 = x2+125-x2+125-x2
            l.append(x1)
            l.append(x2)
    if mid_houghlines is not None:
        for hline in mid_houghlines:
            x1,y1,x2,y2=hline.reshape(4)
            l.append(x1)
            l.append(x2)
            
    abstract_line = (sum(l)/(len(l)+1))
    abs_deg = abs(125 - abstract_line)
    d=1
    dist_dots = abs(out_count-mid_count)

        
    if (line=='R'):
        if (out_count>mid_count):
            deg=abs_deg*0.07+dist_dots/22*0.4
            deg = int(max(min(100,deg) , -100))
            Speed=int((100-deg/10))
            deg = -deg      



        else:
            deg=abs_deg*0.07+dist_dots/22*0.4
            deg = int(max(min(100,deg) , -100))
            Speed=int((100-deg/10))        


    elif (line=='L'):
        if (out_count>mid_count):
            deg=dist_dots/18
            deg = int(max(min(100,deg) , -40))
            Speed=int((100-deg/10))
          



        else:
            deg=dist_dots/18
            deg = int(max(min(100,deg) , -40))
            Speed=int((100-deg/10)) 
            deg = -deg


    degFactor = 10

    return [Speed , [deg,degFactor] ]

