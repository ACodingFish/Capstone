

def parse(commands):
    for command in commands.split(", "):
        index = 0
        for character in command:
            if (character.isdigit()): 
                index += 1
            elif (index>0):           
                #print("\tIndex: ",int(command[:index]),"\tString: ",command[index:])
                servo_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5}.get(command[index:], -1) 
                set_servo_position(servo_index, command[:index]) # servo_index, servo_position
                break
parse("12a, 120b, 80c")