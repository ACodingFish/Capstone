if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_ADC:
    def __init__(self, num_avgs, index):
        self.channel = index
        self.num_avg = 0            #init to 0
        if (num_avgs < 1):
            num_avgs = 1):
        self.max_num_avg = num_avgs #number of times to average
        self.avg_arr = []
        self.avg = 0
        #initialize ADC
        
    def read_value(self):
        #read from ADC at index
    
    
class PI_ADC_MONITOR:
    def __init__(self):
        self.num_channels = 16
        self.adc = [] #insert class here (Somehow pass parameters? or default them?)
        start_new_thread(self.monitor_thread,())
            
    def monitor_thread(self):
        while True:
            for i in range(self.num_channels):
                value = self.adc[i].read_value()
                if (self.adc[i].num_avg < self.adc[i].max_num_avg):# initialize num avg to zero first (this is the number that have been read)
                    self.adc[i].num_avg += 1
                else:
                    #shift every array elem down 1 and remove oldest
                    #put in new elem
                    self.adc[i].avg_arr.pop(0) # shifts all elements left
                self.adc[i].avg_arr.append(value) # appends new element
                self.adc[i].avg = sum(self.adc[i].avg_arr)/self.length
    
    def get_adc_avg(self, index):
        return self.adc[i].avg #should default to 0
        