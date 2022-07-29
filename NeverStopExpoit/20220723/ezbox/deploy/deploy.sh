#!/bin/bash
sudo docker build ./ -t pwn_ezbox
sudo docker run -d -p "0.0.0.0:31056:9999" -h "pwn_ezbox" -v $PWD/bin/flag:/home/ctf/flag --name="pwn_ezbox" pwn_ezbox
