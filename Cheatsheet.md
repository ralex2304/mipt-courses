# Cisco Labs Cheatsheet

MIPT Computer Networks course 5 semester

## Modes

- `>` - user EXEC mode
- `#` - privileged EXEC mode
- `(config)#` - global config mode
- `(config-if)#` - interface config mode

Enter privileged EXEC mode
```
R> enable
```

Enter global config mode
```
R# configure terminal
```

Enter the interface configure mode
```
R(config)# interface <type>/number>
```

## Tips

Execute in priveleged EXEC mode:
```
do <command>
```

Exit current mode:
```
exit
```

Exit current mode and enter priveleged EXEC mode
```
end
```

Interrupt execution of current command
```
<CTRL+SHIFT+6>
```

Cancel command / delete configuration of that command
```
no <command>
```

Connect to device (router or swicth) from PC for configuration
```
PC> telnet <IP>
```

## Show commands

Configs:
```
show running-config
show startup-config
```

View available interfaces and their parameters
```
show ip interface brief
```

Routing table
```
show ip route
```

View CAM table
```
show mac-address-table
```

View STP parameters
```
show spanning-tree
```

View VLAN parameters
```
show VLAN brief
```

View VLAN's brief parameters on interfaces
```
show interface VLAN brief
```

View Time
```
show clock
```

##  Basic commands

```
R(config)# interface <type>/<number>
```

Set IP address and Mask to interface
```
R(config-if)# ip address <IP> <decimal-MASK>
```

Set IPv6 address and Mask to interface
```
R(config-if)# ipv6 address <IPv6>/<mask len>
```

Set IPv6 link local address
```
R(config-if)# ipv6 address <IPv6> link-local
```

Enable interface
```
R(config-if)# no shutdown
```

Set description
```
R(config-if)# description <text>
```

Enable IPv6 routing:
```
R(config)# ipv6 unicast-routing
```

Set hostname
```
R(config)# hostname <name>
```

Set time
```
S# clock set <hh:mm:ss Mon Dat Year>
```

Create a banner
```
R(config)# banner motd $ <text> $
```

Save running configuration
```
R# copy running-config startup-config
```

## Security

Assign privileged EXEC encrypted password
```
R(config)# enable secret <password>
```

Set console/vty password and enable login
```
R(config)# line {console|vty} <number or range>
R(config-line)# password <password>
R(config-line)# login
```

Encrypt plaintext passwords
```
R(config)# service password-encryption
```

## VLAN Configuration

Create VLAN
```
vlan <vlan-number>
```

Set VLAN name
```
name <name>
```

### MODE ACCESS (interfaces connected to end devices)

Set access mode
```
S(config-if)# swichport mode access
```

Set access VLAN
```
S(config-if)# switchport access vlan <vlan-number>
```

Enable voice
```
mls qos trust cos
switchport voice vlan <vlan-number>
```

### MODE TRUNK (interfaces connected to other switches or routers)

Set trunk mode
```
S(config-if)# switchport mode trunk
```

Disable dynamic trunking
```
S(config-if)# switchport nonegotiate
```

Enable dynamic trunking on one of the switches
```
S(config-if)# switchport mode dynamic desirable
```

Configure the trunk
```
S(config-if)# switchport trunk native vlan <vlan-number>
```

### VLAN management

```
S(config)# interface vlan <vlan-number>
```

Assign IP address and mask
```
ip address <IP> <decimal-MASK>
```

Set default gateway on switch
```
S(config)# ip default-gateway <IP address>
```

### Router on a stick

Configure subinterfaces using the 802.1Q encapsulation
```
R1(config)# interface <interface type>/<number>.<vlan-number>
R1(config-subif)# encapsulation dot1Q <vlan-number>
R1(config-subif)# ip address <IP address> <MASK>
```

Enable dot1q encapsulation for 2-3 layer switch on trunk interface
```
MLS(config-if)# switchport trunk encapsulation dot1q
```

## Etherchannel

First, enable trunk on port range
```
S(config)# interface range f0/21-22
S(config-if-range)# switchport mode trunk
```

Then, enable Etherchannel
```
S(config-if-range)# shutdown
S(config-if-range)# channel-group 1 mode {desirable, active, passive}
S(config-if-range)# no shutdown
```

- `desirable` - PAgP
- `active` - LACP
- `passive` - LACP only if LACP device is detected

## Spanning Tree Protocol (STP)

Set priority <value> of the switch for the STP for vlan
```
spanning-tree vlan <vlan-number> [priority <value]
```

## CAM Table

Set static CAM table entry
```
mac-address-table static <MAC address> [vlan <vlan-number>] interface <type>/<number>
```

Flush contents of CAM table
```
clear mac-address-table
```

## Routing configuration

Set default route
```
ip route 0.0.0.0 0.0.0.0 {<next-hop IP>|<interface>} [<administrative distance>=1]
```

Set route to the destination network
```
ip route <destination network> <destination network's mask> {<next-hop IP>|<interface>} [<administrative distance>=1]
```

IPv6
```
ipv6 route <same>...
```

## DHCP

Exclude address range from DHCP
```
R(config)# ip dhcp excluded-address <start IP> <end IP>
```

Create pool
```
R(config)# ip dhcp pool R<name>
```

Configure DHCP pool
```
R(dhcp-config)# network <network IP address> <MASK>
R(dhcp-config)# default-router <LAN router IP>
R(dhcp-config)# dns-server <dns server IP>
```

### DHCP relay

Set helper address on client router
```
R(config-if)# ip helper-address <DHCP server-router IP>
```

### Router as a DHCP client

Configure interface to recieve IP from DHCP
```
R(config-if)# ip address dhcp
R(config-if)# no shutdown
```


## Hot Standby Router Protocol (HSRP)

Set version for interface
```
R(config-if)# standby version 2
```

Enable HSRP for interface
```
R(config-if)# standby <group-id> ip <virtual gateway IP>
```

Set priority (default = 100)
```
R(config-if)# standby <group-id> priority <priority>
```

Enable preempt (router will resume its role when it becomes available again)
```
R(config-if)# standby <group-id> preempt
```

Don't forget to set default gateway for PCs to virtual gateway IP!!!

## RIP

Enter RIP configuration
```
R(config)# router rip
```

Set version and disable summarization of networks

```
R(config-router)# version 2
R(config-router)# no auto-summary
```

Add networks, that are connected to this router
```
R(config-router)# network <network IP>
```

Disable interface, that contains no routers
```
R(config-router)# passive-interface <interface type>/<number>
```

## Diagnostics

Ping:
```
S# ping <IP address>
PC> ping <IP address>
```

Traceroute:
```
S# traceroute <IP address>
PC> tracert <IP address>
```

SSH:
```
S# ssh -l admin <IP address>
```

