if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
    
class PI_ADC:
    def __init__(self):
        self.num_channels = 16
        self.ADC = #insert class here (Somehow pass parameters? or default them?)
        start_new_thread(monitor_thread,())
            
    def monitor_thread(self):
        while True:
            for i in range(self.num_channels):
                value = self.ADC.adc[i].read_value()
                if (self.ADC.adc[i].num_avg < self.ADC.adc[i].max_num_avg):# initialize num avg to zero first (this is the number that have been read)
                    self.ADC.adc[i].num_avg += 1
                else:
                    #shift every array elem down 1 and remove oldest
                    #put in new elem
                    self.ADC.adc[i].avg_arr.pop(0) # shifts all elements left
                self.ADC.adc[i].avg_arr.append(value) # appends new element
                self.ADC.adc[i].avg = sum(self.ADC.adc[i].avg_arr)/self.length
    
    def get_adc_value(self, index):
        return self.ADC.adc[i].avg #should default to 0