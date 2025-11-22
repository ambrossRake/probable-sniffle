import time
import os


textAnimSpeed = .005

def clear():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def animPrint(msg):
    for char in msg:
        if char == ".":
            time.sleep(textAnimSpeed*10)
        print(char, end='', flush=True)
        time.sleep(textAnimSpeed)
