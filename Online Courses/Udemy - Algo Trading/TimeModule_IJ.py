# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 18:16:39 2020

@author: ijurkovic
"""

import time
import numpy as np

def fibonacci(n):
    ##recursive function to print nth Fibonacci number
    if n <= 1:
        return n
    else:
        return(fibonacci(n-1) + fibonacci(n-2))
    
 ##the main action to be preformed 
def main():
    num = np.random.randint(1,25)
    print("%dth fibonacci number is: %d"%(num,fibonacci(num)))
    
    
#continous execution
starttime=time.time()
timeout = time.time() + 60*2 #60 seconds times 2 meaning the script will run for 2 minutes
while time.time() <= timeout:
    try:
        main()
        time.sleep(5 - ((time.time() - starttime) % 5.0)) # 1 min interval between each new execution
    except KeyboardInterrupt:
        print('\n\nKeyboard exception recieved. Exiting.')
        exit()