import os
import time 

while 1:
    os.system("sh ./curl.sh")
    os.system("python ./stat.py")
    time.sleep(1)
    
