import sys
import subprocess
import subprocess as sp
import time
print("If not get correct data to use maual method of baudrate")
output1 = sp.getoutput('ls /dev/tty* | grep USB | head -n 1')
print("Port is:", output1)
time.sleep(2)   
a = "stty < " + output1 + "| awk 'NR==1{print $2;exit}'"
output2 = sp.getoutput(a)
print("baudrate is:", output2)
time.sleep(2)
command = "screen " + output1 + " " + output2
return_value = subprocess.call(command, shell=True)