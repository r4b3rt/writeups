#!/bin/bash
steghide extract -sf SH.jpg -p hawking -xf flag.txt && cat flag.txt
