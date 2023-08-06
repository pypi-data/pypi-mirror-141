from colorama import init, Fore
import datetime

init(autoreset=True)
time = datetime.datetime.now()

def debug(logMessage):
    print(f'{Fore.BLUE}[ {time.hour}:{time.minute}:{time.second} ] DEBUG: {logMessage}')

def info(logMessage):
    print(f'{Fore.BLACK}[ {time.hour}:{time.minute}:{time.second} ] INFO: {logMessage}')

def warn(logMessage):
    print(f'{Fore.YELLOW}[ {time.hour}:{time.minute}:{time.second} ] WARN: {logMessage}')

def error(logMessage):
    print(f'{Fore.LIGHTRED_EX}[ {time.hour}:{time.minute}:{time.second} ] ERROR: {logMessage}')

def critical(logMessage, status):
    print(f'{Fore.RED}[ {time.hour}:{time.minute}:{time.second} ] CRITICAL: {logMessage}')
    exit(status)