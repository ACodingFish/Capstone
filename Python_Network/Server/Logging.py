import datetime

logname = "log.txt"
    
def log_message(message):
    filename = datetime.datetime.today().strftime('%Y_%m_%d') + "_" + logname;
    outFile= open(filename,"a+")
    outFile.write(message)
    outFile.close()