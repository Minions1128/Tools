# VxLAN

## 特性

其全称为Virtual eXtensible Local Area Network，提供扩展的2层。
VLAN提供12 bit的标识，而VXLAN提供24 bit的标识VNID（VXLAN Network ID）
VLAN使用STP防止环路，VXLAN使用3层的方式，链路聚合、负载均衡

## 报文格式

使用MAC in UDP的封装方式

![](https://github.com/Minions1128/Tools/blob/master/img/vxlan_packet_format.jpg)

## VTEP

VXLAN使用VTEP (VXLAN Tunnel Endpoint)设备来映射，进行VLXAN的封装和解封装。每个VTEP有2个接口：一个是在本地LAN上支持本地终端通信的交换机接口，另一个是传输IP网络的IP接口。
IP接口有一个唯一的IP地址来标识VTEP设备，VTEP设备使用这个IP地址在传输网络上进行封装以太网帧并将其发送。VTPE设备也会通过此端口发现远端的VTEPs，学习到远端的MAC与VTEP的映射。

## VxLAN报文转发方式

### 点对点单播方式

![](https://github.com/Minions1128/Tools/blob/master/img/vxlan_unicast_forwarding_flow.jpg)

### 多点组播方式

![](https://github.com/Minions1128/Tools/blob/master/img/vxlan_mul_forwarding_flow.jpg)

来源：http://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-729383.html