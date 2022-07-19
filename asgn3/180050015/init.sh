#!/bin/bash

ip netns add vnet0
ip link add veth0 type veth peer name veth1
ip link set veth1 netns vnet0
ip netns exec vnet0 ip link set dev veth1 up
ip -n vnet0 link set lo up
ip netns exec vnet0 ip addr add 10.1.1.1/24 dev veth1
ip addr add 10.1.1.2/24 dev veth0
ip link set dev veth0 up

ip netns add vnet1
ip link add veth2 type veth peer name veth3
ip link set veth3 netns vnet1
ip netns exec vnet1 ip link set dev veth3 up
ip -n vnet1 link set lo up
ip netns exec vnet1 ip addr add 20.1.1.1/24 dev veth3
ip addr add 20.1.1.2/24 dev veth2
ip link set dev veth2 up

mkdir /sys/fs/cgroup/memory/limited
echo 150000000 | sudo tee /sys/fs/cgroup/memory/limited/memory.limit_in_bytes
echo 0 | sudo tee /sys/fs/cgroup/memory/limited/memory.swappiness