#!/bin/bash

tshark -r data.pcapng -T fields -e usb.capdata | grep -E "^.{23}$" | grep -v 00:00:00:00:00:00:00:00 > usbdata.txt

