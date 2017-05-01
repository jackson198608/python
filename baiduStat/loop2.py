import os
import time
import random

while 1:
    times=random.randint(1,10)
    os.system("sh ./curl.sh")
    for i in range(0,times):
        os.system("python ./stat.py")
        time.sleep(1)
    
