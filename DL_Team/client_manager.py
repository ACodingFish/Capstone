import sys
import os
import time

class PI_Client:
    def __init__(self, name, idnum):
        self.name = name
        self.idnum = idnum
        
class PI_Client_Monitor:
    def __init__(self):
        self.client_list = []
        
    def add_client(self, name, idnum):
        new_client = self.PI_Client(name, idnum)
        self.client_list.append(new_client)
        
    def delete_client(self, idnum):
        for i in range(0, len(self.client_list)):
            if self.client_list[i].idnum == idnum:
                pop(self.client_list[i])
    
    def search_client(self, name):
        cli_arr = []
        for client in self.client_list:
            if client.name == name:
                cli_arr.append(client.idnum)
        return cli_arr
        
    def compare_client(self, parameter)
        cli_arr = []
        for client in self.client_list;
            if parameter in client.name
                cli_arr.append(client.idnum)
        return cli_arr