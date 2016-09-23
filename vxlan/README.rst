This program will implement vxlan using Open vSwitch in Mininet.

We need to input the remote outbound ip address and the Data Center Number [1/2]

Then we can do some testing on it.

Here is a method that config ovs on 2 MVs.
The topology is as follows:
    +-------+     +-------+
    |       |     |       |
    |  VM1  |-----|  VM2  |
    |       |     |       |
    +-------+     +-------+
IP addresses:
    VM1-eth0：172.31.0.1/24
    VM2-eth0：172.31.0.2/24

We use the 2 Open vSwitch in each VM, br1 is as control plane, br0 is as data plane.

We will create br0 and br1 on VM1
    ovs-vsctl del-br br0
    ovs-vsctl add-br br0
    ovs-vsctl del-br br1
    ovs-vsctl add-br br1
Clear the eth0, assign the IP of eth0 to br1, and add the default gateway.
    ifconfig eth0 0 up
    ifconfig br1 172.31.0.1/24 up
    route add default gw 172.31.0.254
Assign port eth0 to br1
    ovs-vsctl add-port br1 eth0
Config the IP address, that the tunnel will use, to br0
    ifconfig br0 100.64.1.1/30 up
Create interface vx1, add the interface to br0
    ovs-vsctl add-port br0 vx1 -- set interface vx1 type=vxlan options:remote_ip=172.31.0.2

Do the same configure on VM2
    ovs-vsctl del-br br0
    ovs-vsctl add-br br0
    ovs-vsctl del-br br1
    ovs-vsctl add-br br1
    ifconfig eth0 0 up
    ifconfig br1 172.31.0.2/24 up
    route add default gw 172.31.0.254
    ovs-vsctl add-port br1 eth0
    ifconfig br0 100.64.1.2/30 up
    ovs-vsctl add-port br0 vx1 -- set interface vx1 type=vxlan options:remote_ip=172.31.0.1
