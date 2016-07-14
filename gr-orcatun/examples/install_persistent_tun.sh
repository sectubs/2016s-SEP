#!/bin/bash
#title          :install_persistent_tun.sh
#description    :Configure persistent tun device using systemd
#author         :Johannes Heidtmann
#################################
NAME="tun3"
ADRESS="24.187.234.187/24"
PEER="24.187.234.188/24"
PACKET_INFO="true" # Prepend IP Packets with 4 extra bytes

NETDEV_FILE="/etc/systemd/network/tun.netdev"
NETWORK_FILE="/etc/systemd/network/static_tun.network"
#################################
#write configuration files
printf '%s\n' 					\
	'[NetDev]' 					\
	$'Name='$NAME 				\
	'Kind=tun' 					\
	'' 							\
	'[Tun]'						\
	$'PacketInfo='$PACKET_INFO 	\
	'' 							\
	 > $NETDEV_FILE

printf '%s\n' 					\
	'[Match]' 					\
	$'Name='$NAME 				\
	'' 							\
	'[Network]'					\
	$'Address='$ADRESS 			\
	$'Peer='$PEER 				\
	'' 							\
	 > $NETWORK_FILE

# make sure systemd-networkd is enabled
sudo systemctl enable systemd-networkd
# restart systemd-networkd to apply changes
sudo systemctl restart systemd-networkd