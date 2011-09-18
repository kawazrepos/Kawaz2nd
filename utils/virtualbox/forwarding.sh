#!/bin/bash
NAME="Ubuntu 10.04 Server"

# SSH
VBoxManage setextradata "$NAME" "VBoxInternal/Devices/e1000/0/LUN#0/Config/guestssh/Protocol" TCP
VBoxManage setextradata "$NAME" "VBoxInternal/Devices/e1000/0/LUN#0/Config/guestssh/GuestPort" 22
VBoxManage setextradata "$NAME" "VBoxInternal/Devices/e1000/0/LUN#0/Config/guestssh/HostPort" 2222

# HTTP
VBoxManage setextradata "$NAME" "VBoxInternal/Devices/e1000/0/LUN#0/Config/guesthttp/Protocol" TCP
VBoxManage setextradata "$NAME" "VBoxInternal/Devices/e1000/0/LUN#0/Config/guesthttp/GuestPort" 80
VBoxManage setextradata "$NAME" "VBoxInternal/Devices/e1000/0/LUN#0/Config/guesthttp/HostPort" 8080