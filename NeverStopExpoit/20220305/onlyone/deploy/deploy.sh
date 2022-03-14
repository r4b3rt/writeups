#!/bin/bash
sudo docker build ./ -t pwn_onlyone
sudo docker run -d -p "0.0.0.0:31013:9999" -h "pwn_onlyone" -v $PWD/bin/flag:/home/ctf/flag --name="pwn_onlyone" pwn_onlyone
