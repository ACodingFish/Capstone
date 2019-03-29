import sys
import os
import time

class PI_Client:
    def __init__(self, name, cli):
        self.name = name
        self.cli = cli

class PI_ClientManager:
    def __init__(self):
        self.client_list = []

    def add(self, name, cli):
        new_client = PI_Client(name, cli)
        self.client_list.append(new_client)

    def remove(self, cli):
        for i in range(len(self.client_list)):
            if (self.client_list[i].cli == cli):
                self.client_list.pop(i)
                break

    def search(self, name):
        cli_arr = []
        for client in self.client_list:
            if client.name == name:
                cli_arr.append(client.cli)
        return cli_arr

    #def compare_client(self, parameter):
    #    cli_arr = []
    #    for client in self.client_list;
    #        if parameter in client.name
    #            cli_arr.append(client.cli)
    #    return cli_arr

    def p_all(self):
        print("LIST:")
        for client in self.client_list:
            print("NAM:",client.name,", CLI:",client.cli)
