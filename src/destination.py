from info import info

def destination( current_info):
    sensores_result = sensores( current_info)
    if(sensores_result != 0):
        return sensores_result
    return 'R'


def sensores( current_info):
    sum_sensor=0
    count_sensor=1
    sum_deg=0
    count_deg=1
    for i in range(len(info.sensors)):
        x = info.sensors[i]
        if(x<=5):
            x=5-x
            sum_sensor+=(i+1)*max(1,x)
            count_sensor+=max(1,x)
            sum_deg+=info.sensors[i]
            count_deg+=1
    avg_deg=sum_deg/count_deg
    avg_index=sum_sensor/count_sensor
    if(avg_index>0 and avg_index<20 and avg_deg<=2):
        return 'L'
    if(avg_index>20 and avg_index<40 and avg_deg<=3.5):
        return 'L'
    if(avg_index>40 and avg_index<60 and avg_deg<=4):
        return 'L'
    if(avg_index>60 and avg_index<100 and avg_deg<=4.5):
        return 'L'
    return 0
    


def continueSensores():
    sum_sensor=0
    count_sensor=1
    sum_deg=0
    count_deg=1
    for i in range(len(info.sensors)):
        x = info.sensors[i]
        if(x<=5):
            x=5-x
            sum_sensor+=(i+1)*max(1,x)
            count_sensor+=max(1,x)
            sum_deg+=info.sensors[i]
            count_deg+=1
    avg_deg=sum_deg/count_deg
    avg_index=sum_sensor/count_sensor
    if(avg_index>0 and avg_index<20 and avg_deg<=2):
        return 'L'
    if(avg_index>20 and avg_index<40 and avg_deg<=3.5):
        return 'L'
    if(avg_index>40 and avg_index<60 and avg_deg<=4):
        return 'L'
    if(avg_index>60 and avg_index<100 and avg_deg<=4.5):
        return 'L'
    return 0
