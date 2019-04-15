#!/bin/bash
/bin/bash --rcfile /jail/jail -i
socat TCP-LISTEN:7001,reuseaddr,fork,nodelay EXEC:/bin/bash --rcfile /jail/jail -i,setuid=convict,stderr,pty
