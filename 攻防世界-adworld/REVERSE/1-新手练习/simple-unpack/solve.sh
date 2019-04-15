#!/bin/bash
upx -d simple2.ori -o simple2
strings ./simple2 | grep -o "flag{\w*}"
