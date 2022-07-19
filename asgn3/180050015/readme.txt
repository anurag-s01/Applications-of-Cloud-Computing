python3 client (0:ser1.py, 1:ser2.py) - start client on host
/usr/bin/python /home/ser(1,2).py - start server on container

init.sh - adds both network namespaces and veth pairs, and creates the cgroup for limited memory

run.sh vnet(0,1) - runs the shell in the network namespace provided

Testcases
For PID: run ps
For UTS: run hostname
For Mount: run ps, proc fs, show root directory
For network ns: run two shells, server-client code, in vnet0 and vnet1
For connectivity: run the client server and show output
For cgroup: run /usr/bin/python memhungry.py and show killed