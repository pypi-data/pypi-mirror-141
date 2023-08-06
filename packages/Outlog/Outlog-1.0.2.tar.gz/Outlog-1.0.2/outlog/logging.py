import datetime

time = datetime.datetime.now()

class logger:
    def createLogger(fileName):
        global logFile
        logFile = open(fileName, 'a+')

def save(logType, logMessage):
    logFile.write(f'[ {time.hour}:{time.minute}:{time.second} ] {logType}: {logMessage}\n')
    logFile.close()

def killLogger():
    logFile.close()