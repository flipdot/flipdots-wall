import sys
import os
from printNumber import print_fd

device = '/dev/input/by-id/usb-GASIA_PS2toUSB_Adapter-event-kbd'
fp = open(device, 'rb')

counter = 0
i = 0
while True:
   buffer = fp.read(8)
   i = i + 1

   if i % 270 == 0:
       counter += 1
       print_fd(counter)
