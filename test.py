import os
import time

i = 0
while(True):
    i_str = str(i)
    i_str = i_str.zfill(3)

    cmd ='./sendImageToFlipdots'
    for char in i_str:
        cmd = cmd + ' font/'+char+'.png'
    i = i + 1
    print cmd
    os.system(cmd)
    time.sleep(0.3)
