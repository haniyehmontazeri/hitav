from adjust import adjust 
from current import current
from destination import destination

def drive(image):
    current_info = current(image)
    destination_info = destination( current_info)
    return adjust(current_info, destination_info )
      
