

def parse(command_in):

    for command in command_in.split(", "):

        index = 0
        for number in command:
            if (number.isdigit()): 
                index += 1
            elif (index>0):
                print("\tIndex: ",int(command[:index]),"\tString: ",command[index:])
                break
                
parse("12a, 120b, 80crap, Gin, and, Rum")