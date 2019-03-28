from enum import IntEnum


class Params(IntEnum):
    LOCAL=0
    IP_ADDR=1
    PORT=2
    ENCRYPTION=3
    ID=4
    GUI=5
    TOTAL=6
    #maybe put sensor limits here
    
    

class PI_Conf:
    def __init__(self, file):
        self.params_arr = ["Local", "IP Address", "Port", "Encryption", "ID", "GUI"]
        self.file = file
        fd = open(file, "r")
        data = fd.readlines()
        self.data = []
        for i in range(len(data)):
            self.data.append(data[i].strip(self.params_arr[i] + ",").rstrip("\n"))
        fd.close()
         
#    def write_data(self):
#        fd = open(file, "w+")
#        for i in range (0,TOTAL):
#            if (type(data[i]) != str):
#                self.data[i] = str(self.data[i])
#            w_str = (self.params_arr[i] + "," + self.data[i])
#            fd.write(w_str)
#        fd.close()
    