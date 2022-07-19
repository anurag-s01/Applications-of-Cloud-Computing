#include <bits/stdc++.h>
#include <unistd.h>
#include <errno.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/types.h>

// #include <cap.h>
using namespace std;

int main(int argc, char *argv[])
{
    string rootfs = argv[1];
    string hostname = argv[2];
    string netns = argv[3];
    netns = "/var/run/netns/" + netns;

    if(unshare(CLONE_NEWUTS)){  //unsharing and going into a new UTS namespace
        cerr << "Could not Unshare UTS_namespace: " << errno<< endl;
        exit(1);
    }
    if(sethostname(hostname.c_str(), hostname.length())){ //setting the hostname in the new UTS namespace
        cerr << "Coult not set hostname: " << errno << endl;
        exit(1);
    }

    pid_t pid = getpid();
    string command = "echo "+ to_string(pid)+ " | tee /sys/fs/cgroup/memory/limited/tasks";
    system(command.c_str());    //adding to the limited memory cgroup

    int fd = open(netns.c_str(), O_RDONLY);
    setns(fd, CLONE_NEWNET);    //moving to the vnet netns

    command = "unshare -p -f --mount-proc=/proc --root=" + rootfs + " /bin/bash";
    system(command.c_str());    //starting the shell

    exit(0);
}