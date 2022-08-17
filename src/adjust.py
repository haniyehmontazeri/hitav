from change import *
from arrange import arrange
import destination
def adjust(current_info, destination_info):
    print(info.data+" "+str(info.change_before))
    if((info.data=="right" or info.change_before) and destination.continueSensores()==0):
        info.change_before=False
        return goToRight(current_info , destination_info)
    elif(current_info["line"][0] != destination_info or info.data =="change"):
        info.change_before= destination.continueSensores!=0
        return change_cycle(current_info , destination_info)
    else:
        info.change_before=False
        return arrange(current_info , destination_info )

