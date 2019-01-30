


def parse(str_in):
    commands = str_in.split(", ")
    for command in commands:
        letter_index = 0
        command_num = 0
        command_str = ""
        for letter in command:
            if (letter.isdigit()):
                letter_index +=1
            else:
                if (letter_index > 0):
                    command_num = int(command[:letter_index])
                    command_str = command[letter_index:]
                    print("Index: ", command_num, " String: ", command_str)
                    break
    
parse("12a, 120b, 80c")