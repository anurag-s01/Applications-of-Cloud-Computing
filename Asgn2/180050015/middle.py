from __future__ import print_function
import sys
import libvirt
import time
import argparse
import socket
import threading

localhost = '127.0.0.1'
localport = 5000

dom1Name = 'guest1'
dom2Name = 'guest2'


conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

dom1 = conn.lookupByName(dom1Name)
if dom1 == None:
    print('Failed to find the domain '+dom1Name, file=sys.stderr)
    exit(1)
    
dom2 = conn.lookupByName(dom2Name)

stats1 = dom1.getCPUStats(True)
curr1 = stats1[0]['cpu_time']
# stats2 = dom2.getCPUStats(True)
curr2 = 0
numhigh = 0
threshutil = 80
threshhigh = 20
numserver = 1

def create_dom():
    dom2.create()
    if dom2 == None:
        print('Failed to find the domain '+dom2Name, file=sys.stderr)
        exit(1)


th = threading.Thread(target=create_dom)

while True:
    time.sleep(0.5)
    stats1 = dom1.getCPUStats(True)
    next1 = stats1[0]['cpu_time']
    util1 = 2*(next1 - curr1) / 10000000
    curr1 = next1
    print(dom1Name + ": " + str(util1))
    state, reason = dom2.state()
    if (state == libvirt.VIR_DOMAIN_RUNNING):
        stats2 = dom2.getCPUStats(True)
        next2 = stats2[0]['cpu_time']
        util2 = 2*(next2 - curr2) / 10000000
        curr2 = next2
        print(dom2Name + ": " + str(util2) + '\n')
    else:
        print(dom2Name + ": Not running\n" )
    if (util1 > threshutil):
        numhigh += 1
        if (numhigh > threshhigh and numserver==1):
            numserver = 2
            th.start()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((localhost, localport))
                s.sendall(b'available')
    else:
        numhigh = 0        
conn.close()
th.join()
exit(0)
